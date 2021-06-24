from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<business_id>\w+)/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/admin/(?P<employee_id>\w+)/(?P<business_id>\w+)/(?P<room_name>\w+)/$', consumers.ChatAdminConsumer.as_asgi()),
]
  