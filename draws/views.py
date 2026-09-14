from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from . import services
from .forms import CallNumberForm, EventForm
from .models import Event


@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, "draws/event_list.html", {"events": events})


@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f"Event '{event.name}' created.")
            return redirect("draws:event_admin", slug=event.slug)
    else:
        form = EventForm()
    return render(request, "draws/event_form.html", {"form": form})


@login_required
def event_admin(request, slug):
    event = get_object_or_404(Event, slug=slug)
    form = CallNumberForm()
    return render(
        request,
        "draws/event_admin.html",
        {"event": event, "form": form, "calls": event.calls.order_by("-position")},
    )


@login_required
@require_POST
def call_number(request, slug):
    event = get_object_or_404(Event, slug=slug)
    form = CallNumberForm(request.POST)
    if form.is_valid():
        try:
            call = services.add_number(event, form.cleaned_data["number"])
            messages.success(request, f"Called #{call.number}.")
        except ValueError as exc:
            messages.error(request, str(exc))
    else:
        messages.error(request, "Enter a valid ticket number.")
    return redirect("draws:event_admin", slug=slug)


@login_required
@require_POST
def undo_last(request, slug):
    event = get_object_or_404(Event, slug=slug)
    try:
        call = services.undo_last(event)
        messages.success(request, f"Undid call for #{call.number}.")
    except ValueError as exc:
        messages.error(request, str(exc))
    return redirect("draws:event_admin", slug=slug)


def loser_board(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, "draws/loser_board.html", {"event": event, "calls": event.called_numbers})


def loser_board_fragment(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, "draws/_loser_board_fragment.html", {"event": event, "calls": event.called_numbers})
