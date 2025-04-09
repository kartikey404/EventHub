from django.shortcuts import render

from events.models import ConfirmedEvent


def public_events(request):
    events = ConfirmedEvent.objects.all().order_by('date')
    return render(request, 'events/public_events.html', {'events': events})

