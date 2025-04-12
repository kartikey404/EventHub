from django.shortcuts import render
from django.utils import timezone
from events.models import SlotRequest


def public_events(request):
    now = timezone.now()
    events = SlotRequest.objects.filter(
        status='accepted',
        slot__start_time__gte=now
    ).select_related('slot__venue', 'artist').order_by('slot__start_time')

    return render(request, 'events/public_events.html', {'events': events})
