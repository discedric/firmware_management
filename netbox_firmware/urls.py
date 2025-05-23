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
    
    # Bios
    path('bios/', include(get_model_urls('netbox_firmware', 'bios', detail=False))),
    path('bios/<int:pk>/', include(get_model_urls('netbox_firmware', 'bios'))),
    path('bios/<int:pk>/changelog/', views.BiosChangeLogView.as_view(), name='bios_changelog'),
    path('bios/<int:pk>/journal/', views.BiosJournalView.as_view(), name='bios_journal'),
    
    # Bios Assignments
    path('biosassignment/', include(get_model_urls('netbox_firmware','biosassignment',detail=False))),
    path('biosassignment/<int:pk>/', include(get_model_urls('netbox_firmware', 'biosassignment'))),
    path('biosassignment/<int:pk>/changelog/', views.BiosAssignmentChangeLogView.as_view(), name='biosassignment_changelog'),
    path('biosassignment/<int:pk>/journal/', views.BiosAssignmentJournalView.as_view(), name='biosassignment_journal'),
]