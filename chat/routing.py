from django.urls import path
from . import consumers

websocket_urlpatterns = [
# /ws/chat/10/ 과 같은 주소로 웹소켓 연결을 받을 수 있습니다. 채팅방 연결
    path("ws/chat/<int:room_pk>/", consumers.RolePlayingRoomConsumer.as_asgi()),
]