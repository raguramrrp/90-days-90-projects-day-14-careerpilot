from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.overview, name='overview'),
    path('my-day/', views.my_day, name='my_day'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/calendar-events/', views.calendar_events_api, name='calendar_events_api'),
    path('search/', views.global_search, name='search'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
]
