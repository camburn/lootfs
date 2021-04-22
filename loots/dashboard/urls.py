from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard/index.html'), name='home'),
    path('tos/', TemplateView.as_view(template_name='dashboard/tos.html'), name='tos'),
    path('config/', views.configuration_view),
    path('players/', views.PlayerListView.as_view())
]
