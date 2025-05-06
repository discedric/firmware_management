from django.urls import include, path

from utilities.urls import get_model_urls
from . import views

urlpatterns = [
    # Firmwares
    path('firmwares/', include(get_model_urls('netbox_firmware', 'firmware', detail=False))),
    path('firmwares/<int:pk>/', include(get_model_urls('netbox_firmware', 'firmware'))),
    path('firmwares/<int:pk>/changelog/', views.FirmwareChangeLogView.as_view(), name='firmware_changelog'),
    path('firmwares/<int:pk>/journal/', views.FirmwareJournalView.as_view(), name='firmware_journal'),
    
    # Assignments
    path('assignment/', include(get_model_urls('netbox_firmware','firmwareassignment',detail=False))),
    path('assignment/<int:pk>/', include(get_model_urls('netbox_firmware', 'firmwareassignment'))),
    path('assignment/<int:pk>/changelog/', views.FirmwareAssignmentChangeLogView.as_view(), name='firmwareassignment_changelog'),
    path('assignment/<int:pk>/journal/', views.FirmwareAssignmentJournalView.as_view(), name='firmwareassignment_journal'),
]