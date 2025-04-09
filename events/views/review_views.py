## Views: Add & Show Reviews
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from events.forms import ReviewForm
from events.models import Venue, Review
from events.views.auth_views import role_redirect


@login_required
def review_venue(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.venue = venue
            review.save()
            return redirect('venue_detail', venue_id=venue.id)
    else:
        form = ReviewForm()
    return render(request, 'events/review_form.html', {'form': form, 'target': venue.name})


@login_required
def review_artist(request, artist_id):
    artist = get_object_or_404(User, pk=artist_id, userprofile__user_type='artist')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.artist = artist
            review.save()
            return redirect('artist_profile', artist_id=artist.id)
    else:
        form = ReviewForm()
    return render(request, 'events/review_form.html', {'form': form, 'target': artist.username})


@login_required
def submit_review(request, review_type, target_id):
    if request.user.userprofile.user_type != 'guest':
        messages.error(request, "Only guests can submit reviews.")
        return role_redirect(request)

    if review_type == 'venue':
        venue = get_object_or_404(Venue, id=target_id)
        existing = Review.objects.filter(reviewer=request.user, venue=venue).first()
        if existing:
            messages.warning(request, "You’ve already reviewed this venue.")
            return role_redirect(request)

        target = venue
        context_type = 'venue'

    elif review_type == 'artist':
        artist = get_object_or_404(User, id=target_id)
        existing = Review.objects.filter(reviewer=request.user, artist=artist).first()
        if existing:
            messages.warning(request, "You’ve already reviewed this artist.")
            return role_redirect(request)

        target = artist
        context_type = 'artist'

    else:
        return HttpResponseBadRequest("Invalid review type.")

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            if context_type == 'venue':
                review.venue = venue
            else:
                review.artist = artist
            review.save()
            messages.success(request, "Thank you for your review!")
            return role_redirect(request)
    else:
        form = ReviewForm()

    return render(request, 'events/submit_review.html', {'form': form, 'target': target, 'type': context_type})
