from django.urls import path
from . import views

app_name = 'reminders'

urlpatterns = [
    path('', views.reminder_list, name='list'),
    path('create/', views.reminder_create, name='create'),
    path('<int:pk>/edit/', views.reminder_update, name='update'),
    path('<int:pk>/delete/', views.reminder_delete, name='delete'),
    path('<int:pk>/toggle/', views.toggle_reminder_api, name='toggle_api'),
]
