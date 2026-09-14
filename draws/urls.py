from django.urls import path

from . import views

app_name = "draws"

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("new/", views.event_create, name="event_create"),
    path("<slug:slug>/", views.board, name="board"),
    path("<slug:slug>/state/", views.board_state, name="board_state"),
    path("<slug:slug>/add/", views.board_add, name="board_add"),
    path("<slug:slug>/undo/", views.board_undo, name="board_undo"),
    path("<slug:slug>/clear/", views.board_clear, name="board_clear"),
    path("<slug:slug>/toggle/<int:call_id>/", views.board_toggle, name="board_toggle"),
]
