from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/catan/(?P<room_name>[\w\-]+)/$',
            consumers.ChatConsumer),
    # re_path(r'ws/catan2/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]