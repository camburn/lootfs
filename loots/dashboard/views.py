from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
# Create your views here.

from django_tables2 import SingleTableView
import pandas
import json
import re
from django_pandas.io import read_frame

from .tables import AttendanceTable
from .forms import LootListForm, LogSubmitForm
from .models import Player, Attendance, Item, LootList
from .warcraftlogs import process_report, view_report

def configuration_view(request):
    html = '<html><body><h1>Config View</h1><p>Testing the view</p></body></html'
    return HttpResponse(html)

def players(request):
    #TODO: Add filter (or pagination)
    players = Player.objects.all() #.filter(name='Kaem')
    template = loader.get_template('players.j2')

    context = {
        'player_list': players
    }

    return HttpResponse(template.render(context, request))

class AttendanceListView(SingleTableView):
    model = Attendance
    table_class = AttendanceTable
    template_name = 'attendance_list.html'


def calculate_scores(request):
    players = Player.objects.all()

    for player in players:
        attendance = Attendance.objects.all().filter(player=player)



def attendance(request):
    template = loader.get_template('dashboard/attendance.html')

    qs = Attendance.objects.all()
    values = qs.values('amount', 'raid__dungeon__name', 'raid__start_time', 'raid__fights', 'player__name')

    if not values:
        context = {
            'table_html': '<p>There is no recorded attendance</p>'
        }
        return HttpResponse(template.render(context, request))
    
    # Format the raid names to make sense - this way isn't great but object.values is limited to
    # only fields.
    for d in values:
        d['raid'] = f"{d['raid__start_time'].date()} ({d['raid__dungeon__name']} - {d['raid__fights']} fights)"
        del d['raid__fights']
        del d['raid__dungeon__name']
        del d['raid__start_time']

    df = pandas.DataFrame(values)

    pt = pandas.pivot_table(
        df, values='amount', columns=['raid'], index='player__name',
    )
    pt = pt.fillna(0)  # Converts players who were absent for a raid to 0

    pt['Average'] = pt.groupby(level='player__name').mean().mean(axis=1)
    pt.index.name = None # Hide index name ('player_id')
    pt.columns.name = 'Player'

    classes = 'table table-striped table-bordered table-hover table-sm table-striped'

    context = {
        'table_html': pt.to_html(classes=classes, table_id='datatable')
    }
    

    return HttpResponse(template.render(context, request))

def submit_report(request):
    template = loader.get_template('dashboard/submit_logs.html')
    if request.method == "POST":
        #form = LogSubmitForm(request)
        #if form.is_valid():
        #    print(form)
        print(request.POST)
        request_url = request.POST['logsurl']
        try:
            log_id = re.search('/reports/([a-zA-Z0-9]{16})', request_url).group(1)
            print(log_id)
        except Exception:
            print('sad times')

    context = {}
    return HttpResponse(template.render(context, request))

def process_report_view(request):
    process_report('bLcRvHJDZwmrjkBP')
    process_report('d7m2MkCQ38fVcRwH')
    process_report('fy8pLqkDhnJjHcN2')
    process_report('DNwW8xbnM2qrYAJ3')
    process_report('rhc4pztRTb1FdZqQ')
    process_report('MqKhpDj71rmbytHX')
    process_report('XKjW38Pcg4ALChvG')
    process_report('t9AMHKvVCRaDXwGJ')
    process_report('AgvzcbZX9x4WPTkK')
    process_report('Z6vgVx8Y2jDhyz3G')
    process_report('kzaPDbpZqtQVdJ2w')
    process_report('7LWpA16XMQrvdKbF')
    process_report('aPgZvcjfbY8CFrG7')
    process_report('bt2Da9wA7WrQ3kdR')
    process_report('QGRdLzxFZWaDqmhP')
    process_report('QRZc9zrVa8J127f4')
    process_report('P4Fmq67zGAYk2jpN')
    process_report('WmbqaRM1KNhj4Gvd')
    process_report('mxLCBqKQNvra1YGJ')
    process_report('6gRkxZrNXDnbGhBF')
    process_report('Bgx1b6qzwdnRcJWa')
    process_report('dpMbCQzNrV8YWxB9')
    process_report('HZFTgaJcRN98y1KG')
    process_report('HgaJwRxDPp2KfVt4')
    process_report('rAZWXDGF6Kmct9xR')
    return HttpResponse('success')


class PlayerListView(ListView):
    model = Player

class ItemListView(ListView):
    model = Item

'''
def lootlist(request):
   
    if request.method == "POST":
        form = LootListForm(request.POST)
        if form.is_valid():
            #redirect to the url where you'll process the input
             return HttpResponseRedirect('/dashboard/lootlistthanks/') # insert reverse or url

    form = LootListForm()
    table_view = ItemListView()
    errors = form.errors or None # form not submitted or it has errors
    return render(request, 'dashboard/loot_list.html',{
        'form': form,
        'item_list':  table_view,
        'errors': errors,
    })
'''

def lootlist(request):
    if request.method == "POST":
        print('Received post')
        loot_list = json.loads(request.body.decode('utf-8'))
        #item_id_capture = re.compile('=([0-9]*)')
        
        #TODO: Run this in a seperate thread/background process
        
        for item in loot_list['items']:
            item_id = int(re.search('=([0-9]*)', item['url']).group(1))
            LootList.objects.get_or_create(
                player=Player.objects.filter(name='Kaem').first(),
                priority=item['index'],
                item=Item.objects.get(pk=item_id)
            )
        
        return HttpResponseRedirect('/dashboard/lootlistthanks/')

    table_data = Item.objects.all()
    return render(request, 'dashboard/list.html', {
        'item_list':  table_data,
    })


def distribution(request):
    ''' The main distribution page '''

    '''
    Distribution should be a cross section of items and the top players

    item  |  Player   |  Player 2    |
    item1 | Kaem: 62  | Mugroth: 55  |

    Player Scores

    Filter by:

    Player | Class  | Attendance score |
    Kaem   | Shaman | 83               |
    '''
    template = loader.get_template('dashboard/attendance.html')
    players = Player.objects.all()

    values = players.values(
        'name',
        'player_class__name',
        'alt',
        'weighted_score',
        'attendance_score',
        'parse_score'
    )
    df = pandas.DataFrame(values)
    classes = 'table table-striped table-bordered table-hover table-sm table-striped'

    context = {
        'table_html': df.to_html(classes=classes, table_id='datatable')
    }
    

    return HttpResponse(template.render(context, request))

    #return render(request, 'dashboard/distribution.html')