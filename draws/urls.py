from django.urls import path

from . import views

app_name = "draws"

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("new/", views.event_create, name="event_create"),
    path("<slug:slug>/admin/", views.event_admin, name="event_admin"),
    path("<slug:slug>/admin/call/", views.call_number, name="call_number"),
    path("<slug:slug>/admin/undo/", views.undo_last, name="undo_last"),
    path("<slug:slug>/loser-board/", views.loser_board, name="loser_board"),
    path("<slug:slug>/loser-board/fragment/", views.loser_board_fragment, name="loser_board_fragment"),
]
