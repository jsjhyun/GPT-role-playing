from django.shortcuts import render
from django.views.generic import CreateView
from .models import RolePlayingRoom
from .forms import RolePlayingRoomForm


class RolePlayingRoomCreateForm(CreateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm


role_playing_room_new = RolePlayingRoomCreateForm.as_view()
