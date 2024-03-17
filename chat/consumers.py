from pprint import pprint
from typing import List

import openai
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth.models import AbstractUser

from chat.models import RolePlayingRoom, GptMessage


class RolePlayingRoomConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gpt_messages: List[GptMessage] = []
        self.recommend_message: str = ""

    def connect(self):
        room = self.get_room()
        if room is None:
            self.close()
        else:
            self.accept()

            self.gpt_messages = room.get_initial_messages()
            self.recommend_message = room.get_recommend_message()

            assistant_message = self.get_query()
            self.send_json(
                {
                    "type": "assistant-message",
                    "message": assistant_message,
                }
            )

    def receive_json(self, content_dict, **kwargs): # 클라이언트로 부터 수신할 때 마다 호출
        if content_dict["type"] == "user-message":
            assistant_message = self.get_query(user_query=content_dict["message"])
            self.send_json( # Echo 응답 (수신 그대로 응답)
                {
                    "type": "assistant-message",
                    "message": assistant_message,
                }
            )
        elif content_dict["type"] == "request-recommend-message":
            recommended_message = self.get_query(command_query=self.recommend_message)
            self.send_json(
                {
                    "type": "recommended-message",
                    "message": recommended_message,
                }
            )
        else:
            self.send_json(
                {
                    "type": "error",
                    "message": f"Invalid type: {content_dict['type']}",
                }
            )

    # 인증된 특정 방 가져오기
    def get_room(self) -> RolePlayingRoom | None:
        user: AbstractUser = self.scope["user"] # user 인스턴스 사용
        room_pk = self.scope["url_route"]["kwargs"]["room_pk"] # 조회
        room: RolePlayingRoom = None

        if user.is_authenticated: # 인증(로그인 상태)
            try:
                room = RolePlayingRoom.objects.get(pk=room_pk, user=user)
            except RolePlayingRoom.DoesNotExist: # 방 못 찾을 시
                pass

        return room

    # 응답 생성
    def get_query(self, command_query: str = None, user_query: str = None) -> str:
        if command_query is not None and user_query is not None:
            raise ValueError("command_query 인자와 user_query 인자는 동시에 사용할 수 없습니다.")
        elif command_query is not None:
            self.gpt_messages.append(GptMessage(role="user", content=command_query))
        elif user_query is not None:
            self.gpt_messages.append(GptMessage(role="user", content=user_query))

        response_dict = openai.ChatCompletion.create(  # GPT 모델 호출
            model="gpt-3.5-turbo",
            messages=self.gpt_messages,
            temperature=1,
        )
        response_role = response_dict["choices"][0]["message"]["role"] # api 호출
        response_content = response_dict["choices"][0]["message"]["content"]

        if command_query is None: # 계속된 사용자 질문
            gpt_message = GptMessage(role=response_role, content=response_content)
            self.gpt_messages.append(gpt_message)

        return response_content