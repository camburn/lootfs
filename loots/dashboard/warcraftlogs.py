import os
from dataclasses import dataclass, field
import datetime
import requests
import json
import typing
import yaml

from dashboard.models import Player, PlayerClass, Raid, Dungeon, Attendance

#from django_pandas.managers import DataFrameManager
from django_pandas.io import read_frame

AUTH_URL = 'https://www.warcraftlogs.com/oauth/token'
API_URL = 'https://www.warcraftlogs.com/api/v2/client'

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

CACHE = {'token': None}

def token():
    if not CACHE['token']:
        raise 'TOKEN ERROR'

    return CACHE['token']

class Token:
    def __init__(self, token_type, expires_in, access_token):
        self.token_type = token_type
        self.expires_in = expires_in
        self.access_token = access_token

    def bearer(self):
        return f'Bearer {self.access_token}'

@dataclass
class Actor:
    name: str
    id: int
    actor_class: str

@dataclass
class Fight:
    name: str
    kill: bool
    players: typing.List[Actor] = field(default_factory=list)

@dataclass
class LogsRaid:
    name: str
    report_id: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    fights: typing.List[Fight] = field(default_factory=list)

def connect():
    if os.path.isfile('token'):
        print('LOADING TOKEN FROM FILE')
        with open('token', 'r') as token_file:
            data = token_file.read()
            CACHE['token'] = Token(**json.loads(data))

    else:
        if CLIENT_ID is None or CLIENT_SECRET is None:
            print('WARNING: Warcraftlogs CLIENT_ID or CLIENT_SECRET not set - functionality disabled.')
            raise ConnectionError('Connection credentials not set')
        print('REQUESTING NEW TOKEN')
        r = requests.post(AUTH_URL, data={'grant_type': 'client_credentials'}, auth=(CLIENT_ID, CLIENT_SECRET))

        with open('token', 'w') as token_file:
            token_file.write(r.text)

        if r.status_code == 200:
            CACHE['token'] = Token(**r.json())


def query(query_string, variables):
    headers={
        'Authorization': token().bearer(),
        'accept': 'application/json',
    }

    r  = requests.post(API_URL, headers=headers, 
        json={'query': query_string, 'variables': variables}
    )
    data = r.json()
    if 'errors' in data:
        error_string = ''
        for error in data['errors']:
            error_string = error_string + error['message']
        raise Exception('Query Error - query syntax incorrect: error_string', error_string)
    return data


def player_list(actors, player_list):
    data = []
    for player in player_list:
        data.append(actors[player])
    return data

def query_report(report_id):

    query_variables = {'report_id': report_id}

    query_string = '''query($report_id: String!){
        reportData{
            report(code: $report_id) {
                zone{
                    name
                }
            }
        }
    }'''
    raid_name = query(query_string, query_variables)['data']['reportData']['report']['zone']['name']
    

    query_string = '''query($report_id: String!){
        reportData{
            report(code: $report_id) {
                startTime, endTime
            }
        }
    }'''

    times = query(query_string, query_variables)['data']['reportData']['report']
    print(times)
    start_time = datetime.datetime.utcfromtimestamp(times['startTime']//1000).strftime('%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.utcfromtimestamp(times['endTime']//1000).strftime('%Y-%m-%d %H:%M:%S')
    raid = LogsRaid(raid_name, report_id, start_time, end_time)

    query_string = '''query($report_id: String!){
        reportData{
            report(code: $report_id) {
                masterData{
                    actors(type: "player"){
                    name, type, id, subType
                    }
                }
            }
        } 
    }'''

    # Get Players (names)
    players = query(query_string, query_variables)['data']['reportData']['report']['masterData']['actors']
    actors = []
    actors_ids = {}
    for player in players:
        actor = Actor(player['name'], player['id'], player['subType'])
        actors.append(actor)
        actors_ids[actor.id] = actor

    # get fights
    query_string = '''query($report_id: String!){
        reportData{
            report(code: $report_id) {
                fights {
                    name, kill, friendlyPlayers
                }
            }
        }
    }'''
    fights = query(query_string, query_variables)['data']['reportData']['report']['fights']

    for fight in fights:
        if fight['kill'] != None:
            raid.fights.append(Fight(fight['name'], fight['kill'], player_list(actors_ids, fight['friendlyPlayers'])))

    print(raid)
    print('Number of players', len(actors))
    print('finished')
    return raid


def load_report_attendance(logs_raid: LogsRaid):
    dungeon, craeted = Dungeon.objects.get_or_create(name=logs_raid.name)
    no_of_fights = len(logs_raid.fights)
    raid, created = Raid.objects.get_or_create(
        dungeon=dungeon, 
        report_id=logs_raid.report_id, 
        start_time=logs_raid.start_time, 
        end_time=logs_raid.end_time,
        fights=no_of_fights
    )

    player_fight_count = {}

    for fight in logs_raid.fights:
        for actor in fight.players:
            #t = player.objects.create()
            try:
                p, created = Player.objects.get_or_create(
                    name=actor.name, player_class=PlayerClass.objects.get(name=actor.actor_class))
            except Exception:
                print('MISSING CLASS:', actor.actor_class)

            if created:
                print(f'creating {actor.name}, {actor.actor_class}')

            player_name = p.name
            if p.alt:
                player_name = p.main.name
            
            if player_name in player_fight_count:
                player_fight_count[player_name] += 1
            else:
                player_fight_count[player_name] = 1

    for player, fight_count in player_fight_count.items():
        record, created = Attendance.objects.get_or_create(
            raid=raid,
            player=Player.objects.get(name=player)
        )

        record.amount=int((fight_count/no_of_fights) * 100)
        record.consume_uptime=0
        record.raid_parse_average=0
        record.save()
    print(player_fight_count)



def process_report(report_id):
    try:
        connect()
    except ConnectionError:
        print(f'Error connecting to Warcraftlogs: Cannot process {report_id}')
    fight_attendance = query_report(report_id)
    load_report_attendance(fight_attendance)


def report_attendance():
    query = Attendance.objects.all()
    #df = read_frame(query)

    pt = qs.to_pivot_table(values='value_col_d', rows=rows, cols=cols)

    df = read_frame(query, fieldnames=['raid', 'player', 'amount'],
        coerce_float=False, verbose=True)
    return df


def view_report(report_id):
    report_id = 'bLcRvHJDZwmrjkBP'
    return report_attendance()