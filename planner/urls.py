from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/toggle/', views.task_toggle_api, name='task_toggle_api'),
    path('goals/create/', views.goal_create, name='goal_create'),
    path('goals/<int:pk>/delete/', views.goal_delete, name='goal_delete'),
]
