from django.db import transaction
from django.db.models import Max

from .models import CalledNumber


def add_number(event, number):
    number = number.strip()
    if not number:
        raise ValueError("Enter a ticket number.")
    if event.calls.filter(number=number).exists():
        raise ValueError(f"#{number} has already been called.")
    with transaction.atomic():
        last_position = event.calls.aggregate(m=Max("position"))["m"] or 0
        return CalledNumber.objects.create(event=event, number=number, position=last_position + 1)


def undo_last(event):
    call = event.calls.order_by("-position").first()
    if not call:
        raise ValueError("No calls to undo.")
    call.delete()
    return call


def clear_all(event):
    event.calls.all().delete()


def is_auto_winner(event, position):
    if not event.prize_interval:
        return False
    return (position - 1) % event.prize_interval == 0


def effective_winner(event, call):
    if call.manual_winner is not None:
        return call.manual_winner
    return is_auto_winner(event, call.position)


def toggle_winner(event, call):
    call.manual_winner = not effective_winner(event, call)
    call.save(update_fields=["manual_winner"])
    return call
