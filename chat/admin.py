from django.contrib import admin
from .models import RolePlayingRoom
from .forms import RolePlayingRoomForm


@admin.register(RolePlayingRoom) # 모델 지정
class RolePlayingRoomAdmin(admin.ModelAdmin): # ModelAdmin 상속
    form = RolePlayingRoomForm

    def save_model(self, request, obj, form, change): # admin 페이지에서도 자동 번역 기능
        if change is False and form.is_valid(): # 신규 생성, 유효성 검사 확인
            obj.user = request.user # 할당

        super().save_model(request, obj, form, change)