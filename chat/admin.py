from django.contrib import admin

from .forms import RolePlayingRoomForm
from .models import RolePlayingRoom


# Register your models here.

@admin.register(RolePlayingRoom)
class RolePlayingRoomAdmin(admin.ModelAdmin):
    form = RolePlayingRoomForm

    def save_model(self, request, obj, form, change):
        if change is False and form.is_valid():
            obj.user = request.user

        super().save_model(request, obj, form, change)
