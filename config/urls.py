from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('opportunities/', include('opportunities.urls', namespace='opportunities')),
    path('applications/', include('applications.urls', namespace='applications')),
    path('interviews/', include('interviews.urls', namespace='interviews')),
    path('reminders/', include('reminders.urls', namespace='reminders')),
    path('documents/', include('documents.urls', namespace='documents')),
    path('planner/', include('planner.urls', namespace='planner')),
    path('analytics/', include('analytics.urls', namespace='analytics')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('', include('core.urls', namespace='core')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
