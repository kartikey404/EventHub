from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from events.forms import AvailableSlotForm
from events.models import Venue, AvailableSlot, SlotRequest, EventRequest


# Manager adds slot
@login_required
def create_slot(request):
    if request.user.userprofile.user_type != 'manager':
        return redirect('dashboard')

    form = AvailableSlotForm(request.POST or None)
    form.fields['venue'].queryset = Venue.objects.filter(owner=request.user)

    if form.is_valid():
        slot = form.save(commit=False)
        slot.created_by = request.user
        slot.save()
        return redirect('available_slots')

    return render(request, 'calendar/create_slot.html', {'form': form})


# Manager/Artist view all slots
@login_required
def available_slots(request):
    slots = AvailableSlot.objects.filter(is_booked=False)
    return render(request, 'calendar/available_slots.html', {'slots': slots})


# Artist requests a slot
@login_required
def request_slot(request, slot_id):
    slot = get_object_or_404(AvailableSlot, pk=slot_id)

    if request.user.userprofile.user_type != 'artist':
        return redirect('dashboard')

    if request.method == 'POST':
        SlotRequest.objects.create(
            slot=slot,
            artist=request.user,
            requested_by=request.user
        )
        return redirect('available_slots')

    return render(request, 'calendar/request_slot.html', {'slot': slot})


# Manager views slot requests
@login_required
def my_slot_requests(request):
    if request.user.userprofile.user_type != 'manager':
        return redirect('dashboard')  # only for manager

    requests = SlotRequest.objects.filter(slot__created_by=request.user)

    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action')
        slot_request = get_object_or_404(SlotRequest, id=req_id, slot__created_by=request.user)
        print(req_id, action, slot_request)

        if action == 'accept':
            slot_request.status = 'accepted'
        elif action == 'decline':
            slot_request.status = 'declined'
        slot_request.save()

        return redirect('my_slot_requests')
    return render(request, 'calendar/slot_requests.html', {'requests': requests, 'user': request.user})


# Manager approves/rejects
@login_required
def respond_to_request(request, request_id, action):
    print(request_id, action)
    slot_request = get_object_or_404(SlotRequest, pk=request_id, slot__created_by=request.user)
    if action == 'accept':
        slot_request.status = 'accepted'
        slot_request.slot.is_booked = True
        slot_request.slot.save()
    elif action == 'reject':
        slot_request.status = 'rejected'
    slot_request.save()
    return redirect('my_slot_requests')


@login_required
def request_artist_slot(request, artist_id):
    artist = get_object_or_404(User, pk=artist_id, userprofile__user_type='artist')
    venues = Venue.objects.filter(owner=request.user)
    slots = AvailableSlot.objects.filter(venue__in=venues)

    if request.method == 'POST':
        slot_id = request.POST.get('slot')
        slot = get_object_or_404(AvailableSlot, id=slot_id)

        if request.method == 'POST':
            SlotRequest.objects.create(
                slot=slot,
                artist=artist,
                requested_by=request.user
            )
            return redirect('dashboard')

    return render(request, 'calendar/request_artist.html', {
        'artist': artist,
        'venues': venues,
        'slots': slots
    })

@login_required
def artist_requests(request):
    if request.user.userprofile.user_type != 'artist':
        return redirect('dashboard')  # only for artists

    requests = SlotRequest.objects.filter(artist=request.user)

    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action')
        slot_request = get_object_or_404(SlotRequest, id=req_id, artist=request.user)

        if action == 'accept':
            slot_request.status = 'accepted'
        elif action == 'decline':
            slot_request.status = 'declined'
        slot_request.save()

        return redirect('artist_requests')

    return render(request, 'calendar/artist_requests.html', {'requests': requests})
