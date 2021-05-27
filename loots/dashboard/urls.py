from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard/index.html'), name='home'),
    path('tos/', TemplateView.as_view(template_name='dashboard/tos.html'), name='tos'),
    path('config/', views.configuration_view),
    path('players/', views.PlayerListView.as_view()),
    path('items/', views.ItemListView.as_view()),
    path('process/', views.process_report_view),
    path('attendance/', views.attendance),
    path('distribution/', views.distribution),
    path('lootlist/', views.lootlist),
    path('lootlistthanks/', TemplateView.as_view(template_name='dashboard/loot_list_thanks.html'), name='thanks'),
    path('attendance_list/', views.AttendanceListView.as_view())
]
