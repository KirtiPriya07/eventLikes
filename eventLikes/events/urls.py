from django.urls import path

from .views import (
    home_view, 
    event_action_view,
    event_delete_view,
    event_detail_view, 
    event_list_view,
    event_create_view,
)
'''
CLIENT
Base ENDPOINT /api/events/
'''
urlpatterns = [
    path('', event_list_view),
    path('action/', event_action_view),
    path('create/', event_create_view),
    path('<int:event_id>/', event_detail_view),
    path('<int:event_id>/delete/', event_delete_view),
]