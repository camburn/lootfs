from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
# Create your views here.

from django_tables2 import SingleTableView
import pandas
import json
from django_pandas.io import read_frame

from .tables import AttendanceTable
from .forms import LootListForm
from .models import Player, Attendance, Item
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
    pt.index.name = None # Hide idnex name ('player_id')
    pt.columns.name = 'Player'

    classes = 'table table-striped table-bordered table-hover table-sm table-striped'

    context = {
        'table_html': pt.to_html(classes=classes, table_id='datatable')
    }
    

    return HttpResponse(template.render(context, request))

def process_report_view(request):
    process_report('bLcRvHJDZwmrjkBP')
    process_report('d7m2MkCQ38fVcRwH')
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
        print(json.loads(request.body.decode('utf-8')))
        return HttpResponseRedirect('/dashboard/lootlistthanks/')

    table_data = Item.objects.all()
    return render(request, 'dashboard/list.html', {
        'item_list':  table_data,
    })


