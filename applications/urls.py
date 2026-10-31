from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.application_list, name='list'),
    path('pipeline/', views.application_kanban, name='kanban'),
    path('create/', views.application_create, name='create'),
    path('<int:pk>/', views.application_detail, name='detail'),
    path('<int:pk>/edit/', views.application_update, name='update'),
    path('<int:pk>/delete/', views.application_delete, name='delete'),
    path('<int:pk>/update-status/', views.update_status_api, name='update_status_api'),
    path('<int:pk>/add-note/', views.add_note, name='add_note'),
]
