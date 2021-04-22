from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

from .models import Player

def configuration_view(request):
    html = '<html><body><h1>Config View</h1><p>Testing the view</p></body></html'
    return HttpResponse(html)

def players(request):
    players = Player.objects.all() #.filter(name='Kaem')
    template = loader.get_template('players.j2')

    context = {
        'player_list': players
    }

    return HttpResponse(template.render(context, request))


class PlayerListView(ListView):
    model = Player