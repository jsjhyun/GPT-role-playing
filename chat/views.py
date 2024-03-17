from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
)
from gtts import gTTS

from .models import RolePlayingRoom
from .forms import RolePlayingRoomForm


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomListView(ListView):
    model = RolePlayingRoom

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


role_playing_room_list = RolePlayingRoomListView.as_view()


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomDetailView(DetailView):
    model = RolePlayingRoom

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


role_playing_room_detail = RolePlayingRoomDetailView.as_view()


@method_decorator(staff_member_required, name="dispatch") # 장고 admin 기능 사용 : 로그인 여부 확인
class RolePlayingRoomCreateView(CreateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm

    def form_valid(self, form): # 유저 입력 요청 유효성 검사 통과 시 db 저장
        role_playing_room = form.save(commit=False)
        role_playing_room.user = self.request.user # 유저 필드 직접 할당
        return super().form_valid(form) # 부모 호출하여 save : db 저장


role_playing_room_new = RolePlayingRoomCreateView.as_view()


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomUpdateView(UpdateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user) # 본인이 생성한 것만 조회
        return qs


role_playing_room_edit = RolePlayingRoomUpdateView.as_view() # 함수 view 생성 -> url 매핑에 적용


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomDeleteView(DeleteView):
    model = RolePlayingRoom
    success_url = reverse_lazy("role_playing_room_list") # 삭제 성공 시 list 페이지로 이동

    def get_queryset(self): # 본인이 생성한 채팅방 확인
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def form_valid(self, form): # 삭제 성공 메세지
        response = super().form_valid(form)
        messages.success(self.request, "채팅방을 삭제했습니다.")
        return response


role_playing_room_delete = RolePlayingRoomDeleteView.as_view()


# @staff_member_required
# def make_voice(request):
#     lang = request.GET.get("lang", "en")
#     message = request.GET.get("message")
#
#     response = HttpResponse()
#     gTTS(message, lang=lang).write_to_fp(response)
#     response["Content-Type"] = "audio/mpeg"
#
#     return response