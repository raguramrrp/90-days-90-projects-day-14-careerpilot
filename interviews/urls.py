from django.urls import path
from . import views

app_name = 'interviews'

urlpatterns = [
    path('', views.interview_list, name='list'),
    path('create/', views.interview_create, name='create'),
    path('preparation-notes/', views.preparation_notes_list, name='preparation_notes'),
    path('<int:pk>/', views.interview_detail, name='detail'),
    path('<int:pk>/edit/', views.interview_update, name='update'),
    path('<int:pk>/delete/', views.interview_delete, name='delete'),
    path('<int:pk>/add-checklist-item/', views.add_checklist_item, name='add_checklist_item'),
    path('api/checklist/<int:item_id>/toggle/', views.toggle_checklist_api, name='toggle_checklist_api'),
]
