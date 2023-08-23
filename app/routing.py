from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/location/(?P<room_name>[\w-]+)/$', consumers.LocationConsumer.as_asgi()),
]
