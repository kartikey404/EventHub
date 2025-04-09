##Create Dashboard Views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from events.models import Venue, Review, Message


@login_required
def artist_dashboard(request):
    user = request.user
    venues = Venue.objects.filter(owner=user)
    reviews = Review.objects.filter(reviewer=user)
    inbox = Message.objects.filter(recipient=user, is_read=False)
    return render(request, 'events/artist_dashboard.html',{
        'venues': venues,
        'reviews': reviews,
        'inbox_count': inbox.count(),
        'profile': user.userprofile
    })

@login_required
def manager_dashboard(request):
    user = request.user
    venues = Venue.objects.filter(owner=user)
    reviews = Review.objects.filter(reviewer=user)
    inbox = Message.objects.filter(recipient=user, is_read=False)
    return render(request, 'events/manager_dashboard.html', {
        'venues': venues,
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
