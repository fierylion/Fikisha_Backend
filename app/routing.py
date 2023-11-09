from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/location/(?P<room_name>[\w-]+)/$', consumers.LocationConsumer.as_asgi()),
    re_path(r'ws/order/drivers_group/', consumers.OrderConsumer.as_asgi()),
    re_path(r'ws/orders/user/(?P<user_id>[\w-]+)/$', consumers.UserOrderConsumer.as_asgi()),

]
