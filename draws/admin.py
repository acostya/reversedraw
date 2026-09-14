from django.contrib import admin

from .models import CalledNumber, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "called_count", "prize_interval", "created_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CalledNumber)
class CalledNumberAdmin(admin.ModelAdmin):
    list_display = ("event", "number", "position", "manual_winner", "called_at")
    list_filter = ("event",)
    search_fields = ("number",)
