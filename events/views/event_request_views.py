from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from events.forms import EventRequestForm
from events.models import Venue, EventRequest, ConfirmedEvent


@login_required
def send_request(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)

    if request.method == 'POST':
        form = EventRequestForm(request.POST)
        if form.is_valid():
            event_request = form.save(commit=False)
            event_request.venue = venue
            event_request.artist = request.user
            event_request.save()
            return redirect('browse_venues')
    else:
        form = EventRequestForm(initial={'venue': venue})

    return render(request, 'events/send_request.html', {'form': form, 'venue': venue})


##Manager: View & Respond to Requests
@login_required
def manage_requests(request):
    requests = EventRequest.objects.filter(venue__owner=request.user)
    return render(request, 'events/manage_requests.html', {'requests': requests})


@login_required
def update_request_status(request, request_id, action):
    req = get_object_or_404(EventRequest, pk=request_id, venue__owner=request.user)
    if action == 'accept':
        req.status = 'accepted'
    elif action == 'reject':
        req.status = 'rejected'
    req.save()
    return redirect('manage_requests')


@login_required
def send_event_request(request):
    if request.method == 'POST':
        form = EventRequestForm(request.POST)
        if form.is_valid():
            event_request = form.save(commit=False)
            event_request.manager = request.user
            event_request.save()
            messages.success(request, 'Request sent to artist!')
            return redirect('my_requests')
    else:
        form = EventRequestForm()
        # Show only venues owned by current user
        form.fields['venue'].queryset = Venue.objects.filter(owner=request.user)
        # Only show artists
        form.fields['artist'].queryset = User.objects.filter(userprofile__user_type='artist')

    return render(request, 'events/send_event_request.html', {'form': form})


@login_required
def my_requests(request):
    if request.user.userprofile.user_type == 'artist':
        requests = EventRequest.objects.filter(artist=request.user)
    else:
        requests = EventRequest.objects.filter(manager=request.user)
    return render(request, 'events/my_requests.html', {'requests': requests})


@login_required
def decline_request(request, request_id):
    event_request = get_object_or_404(EventRequest, id=request_id, artist=request.user)
    event_request.status = 'declined'
    event_request.save()
    messages.info(request, "You have declined the event invitation.")
    return redirect('my_requests')


@login_required
def accept_request(request, request_id):
    event_request = get_object_or_404(EventRequest, id=request_id, artist=request.user)
    event_request.status = 'accepted'
    event_request.save()

    # Create ConfirmedEvent
    ConfirmedEvent.objects.create(
        venue=event_request.venue,
        artist=event_request.artist,
        date=event_request.date,
        created_from=event_request
    )

    messages.success(request, "You have accepted the event invitation.")
    return redirect('my_requests')
