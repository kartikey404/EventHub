##Create Dashboard Views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import render

from events.models import Venue, Review, Message, EventRequest, SlotRequest


def _get_venues_interacted_with(user: User) -> QuerySet:
    """
    Get venues the artist has interacted with (excluding rejected slots).
    """
    # Filter for valid slot requests (excluding rejected ones)
    slot_requests = SlotRequest.objects.filter(artist=user).exclude(status='rejected')

    # Fetch all distinct venues linked via the slot relationship
    return Venue.objects.filter(id__in=slot_requests.values_list('slot__venue', flat=True)).distinct()



@login_required
def artist_dashboard(request):
    user = request.user
    venues = Venue.objects.filter(owner=user)
    interacted_venues = _get_venues_interacted_with(user)
    reviews = Review.objects.filter(artist=user)
    inbox = Message.objects.filter(recipient=user, is_read=False)

    return render(request, 'events/artist_dashboard.html', {
        'user': user,
        'venues': venues,
        'venues_interacted_with': interacted_venues,
        'reviews': reviews,
        'inbox_count': inbox.count(),
        'profile': user.userprofile
    })



@login_required
def manager_dashboard(request):
    user = request.user
    venues = Venue.objects.filter(owner=user)
    reviews = Review.objects.filter(venue__owner=user)
    inbox = Message.objects.filter(recipient=user, is_read=False)

    # Extracted helper function for slot requests and booked artists
    unique_artists_booked = _get_manager_slot_requests_and_artists(user)

    return render(request, 'events/manager_dashboard.html', {
        'user': user,
        'venues': venues,
        'artists_booked': unique_artists_booked,
        'reviews': reviews,
        'inbox_count': inbox.count(),
        'profile': user.userprofile
    })


def _get_manager_slot_requests_and_artists(user):
    """
    Retrieves non-rejected slot requests and unique artists booked
    by the manager (user).
    """
    non_rejected_slot_requests = SlotRequest.objects.filter(
        slot__venue__owner=user
    ).exclude(status='rejected')

    unique_artists_booked = User.objects.filter(
        id__in=non_rejected_slot_requests.values_list('artist_id', flat=True)
    ).distinct()

    return unique_artists_booked



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
