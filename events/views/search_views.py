from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from events.models import Venue, UserProfile


@login_required
def browse_venues(request):
    venues = Venue.objects.all()

    # Optional: search by name
    query = request.GET.get('q')
    if query:
        venues = venues.filter(Q(name__icontains=query) | Q(address__icontains=query))

    return render(request, 'events/browse_venues.html', {'venues': venues})


def search(request):
    query = request.GET.get('q')
    venue_results = []
    artist_results = []

    if query:
        venue_results = Venue.objects.filter(
            Q(name__icontains=query) | Q(address__icontains=query) | Q(type__icontains=query)
        )

        artist_results = UserProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(location__icontains=query) |
            Q(genre__icontains=query),
            user_type='artist'
        )

    return render(request, 'events/search_results.html', {
        'query': query,
        'venue_results': venue_results,
        'artist_results': artist_results
    })

