from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_center, name='center'),
    path('export/applications/csv/', views.export_applications_csv, name='export_applications_csv'),
    path('export/applications/excel/', views.export_applications_excel, name='export_applications_excel'),
    path('export/opportunities/csv/', views.export_opportunities_csv, name='export_opportunities_csv'),
    path('export/opportunities/excel/', views.export_opportunities_excel, name='export_opportunities_excel'),
    path('export/interviews/csv/', views.export_interviews_csv, name='export_interviews_csv'),
]
