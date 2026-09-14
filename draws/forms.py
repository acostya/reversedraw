from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name"]


class CallNumberForm(forms.Form):
    number = forms.CharField(max_length=20, label="Ticket number")
