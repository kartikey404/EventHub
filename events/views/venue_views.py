from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from events.forms import VenueForm
from events.models import Venue, Review


@login_required
def manager_venue_list(request):
    venues = Venue.objects.filter(owner=request.user)
    return render(request, 'events/venue_list.html', {'venues': venues})

@login_required
def create_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user
            venue.save()
            return redirect('manager_venue_list')
    else:
        form = VenueForm()
    return render(request, 'events/venue_form.html', {'form': form})

@login_required
def update_venue(request, pk):
    venue = get_object_or_404(Venue, pk=pk, owner=request.user)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('manager_venue_list')
    return render(request, 'events/venue_form.html', {'form': form})

@login_required
def delete_venue(request, pk):
    venue = get_object_or_404(Venue, pk=pk, owner=request.user)
    if request.method == 'POST':
        venue.delete()
        return redirect('manager_venue_list')
    return render(request, 'events/venue_confirm_delete.html', {'venue': venue})

def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    reviews = Review.objects.filter(venue=venue)
    return render(request, 'events/venue_detail.html', {'venue': venue, 'reviews': reviews})


@login_required
def my_venues(request):
    venues = Venue.objects.filter(owner=request.user)
    return render(request, 'events/my_venues.html', {'venues': venues})
