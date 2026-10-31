from django.urls import path
from . import views

app_name = 'opportunities'

urlpatterns = [
    path('', views.opportunity_list, name='list'),
    path('saved/', views.saved_jobs_list, name='saved'),
    path('create/', views.opportunity_create, name='create'),
    path('<int:pk>/', views.opportunity_detail, name='detail'),
    path('<int:pk>/edit/', views.opportunity_update, name='update'),
    path('<int:pk>/delete/', views.opportunity_delete, name='delete'),
    path('<int:pk>/toggle-status/', views.opportunity_toggle_status, name='toggle_status'),
    path('api/check-duplicate/', views.check_duplicate_api, name='check_duplicate_api'),
]
