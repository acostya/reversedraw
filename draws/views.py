import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from . import services
from .forms import EventForm
from .models import CalledNumber, Event


def serialize_state(event):
    calls = [
        {
            "id": call.id,
            "number": call.number,
            "position": call.position,
            "is_winner": services.effective_winner(event, call),
        }
        for call in event.called_numbers
    ]
    return {"calls": calls, "total": len(calls)}


def event_list(request):
    events = Event.objects.all()
    return render(request, "draws/event_list.html", {"events": events})


def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f"Event '{event.name}' created.")
            return redirect("draws:board", slug=event.slug)
    else:
        form = EventForm()
    return render(request, "draws/event_form.html", {"form": form})


def board(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(
        request,
        "draws/board.html",
        {"event": event, "state_json": json.dumps(serialize_state(event))},
    )


@require_GET
def board_state(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return JsonResponse(serialize_state(event))


@require_POST
def board_add(request, slug):
    event = get_object_or_404(Event, slug=slug)
    try:
        services.add_number(event, request.POST.get("number", ""))
    except ValueError as exc:
        return JsonResponse({**serialize_state(event), "error": str(exc)})
    return JsonResponse(serialize_state(event))


@require_POST
def board_undo(request, slug):
    event = get_object_or_404(Event, slug=slug)
    try:
        services.undo_last(event)
    except ValueError as exc:
        return JsonResponse({**serialize_state(event), "error": str(exc)})
    return JsonResponse(serialize_state(event))


@require_POST
def board_clear(request, slug):
    event = get_object_or_404(Event, slug=slug)
    services.clear_all(event)
    return JsonResponse(serialize_state(event))


@require_POST
def board_toggle(request, slug, call_id):
    event = get_object_or_404(Event, slug=slug)
    call = get_object_or_404(CalledNumber, event=event, pk=call_id)
    services.toggle_winner(event, call)
    return JsonResponse(serialize_state(event))
