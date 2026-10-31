from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list, name='list'),
    path('upload/', views.document_upload, name='upload'),
    path('<int:pk>/edit/', views.document_edit, name='edit'),
    path('<int:pk>/delete/', views.document_delete, name='delete'),
    path('<int:pk>/download/', views.document_download, name='download'),
]
