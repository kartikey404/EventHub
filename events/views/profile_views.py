from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from events.models import Review, UserProfile, Venue


def artist_profile(request, artist_id):
    artist = get_object_or_404(User, pk=artist_id, userprofile__user_type='artist')
    reviews = Review.objects.filter(artist=artist)
    return render(request, 'events/artist_profile.html', {'artist': artist, 'reviews': reviews})


def artist_list(request):
    artists = UserProfile.objects.filter(user_type='artist')
    return render(request, 'events/artist_list.html', {'artists': artists})


def browse_public_venues(request):
    venues = Venue.objects.all()
    return render(request, 'events/public_venue_list.html', {'venues': venues})