##Create Dashboard Views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from events.models import Venue, Review, Message, EventRequest


@login_required
def artist_dashboard(request):
    user = request.user
    venues = Venue.objects.filter(owner=user)

    # Get venues that the artist has been booked for
    event_requests = EventRequest.objects.filter(artist=user, status='accepted')
    venues_interacted_with = Venue.objects.filter(id__in=event_requests.values_list('venue_id', flat=True)).distinct()

    reviews = Review.objects.filter(reviewer=user)
    inbox = Message.objects.filter(recipient=user, is_read=False)

    return render(request, 'events/artist_dashboard.html', {
        'user': user,
        'venues': venues,
        'venues_interacted_with': venues_interacted_with,
        'reviews': reviews,
        'inbox_count': inbox.count(),
        'profile': user.userprofile
    })


@login_required
def manager_dashboard(request):
    user = request.user
    venues = Venue.objects.filter(owner=user)

    # Get accepted event requests sent by this manager
    event_requests = EventRequest.objects.filter(manager=user, status='accepted')

    # Get unique artists the manager has interacted with
    artists_booked = User.objects.filter(id__in=event_requests.values_list('artist_id', flat=True)).distinct()

    reviews = Review.objects.filter(reviewer=user)
    inbox = Message.objects.filter(recipient=user, is_read=False)

    return render(request, 'events/manager_dashboard.html', {
        'user': user,
        'venues': venues,
        'artists_booked': artists_booked,
        'reviews': reviews,
        'inbox_count': inbox.count(),
        'profile': user.userprofile
    })


@login_required
def guest_dashboard(request):
    user = request.user
    venues = Venue.objects.filter(owner=user)
    reviews = Review.objects.filter(reviewer=user)
    inbox = Message.objects.filter(recipient=user, is_read=False)
    return render(request, 'events/guest_dashboard.html', {
        'venues': venues,
        'reviews': reviews,
        'inbox_count': inbox.count(),
        'profile': user.userprofile
    })

@login_required
def dashboard(request):
    user = request.user
    venues = Venue.objects.filter(owner=user)
    reviews = Review.objects.filter(reviewer=user)
    inbox = Message.objects.filter(recipient=user, is_read=False)

    return render(request, 'events/dashboard.html', {
        'venues': venues,
        'reviews': reviews,
        'inbox_count': inbox.count(),
        'profile': user.userprofile
    })
