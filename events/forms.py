from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, Venue, Message


class CustomUserCreationForm(UserCreationForm):
    USER_TYPES = [
        ('artist', 'Artist'),
        ('manager', 'Event Manager'),
        ('guest', 'Guest'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPES, label='I am a...')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'description', 'capacity']


from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect,
            'comment': forms.Textarea(attrs={'rows': 3}),
        }



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']


from .models import EventRequest

class EventRequestForm(forms.ModelForm):
    class Meta:
        model = EventRequest
        fields = ['venue', 'artist', 'date', 'message']



from django import forms
from .models import AvailableSlot, SlotRequest

class AvailableSlotForm(forms.ModelForm):
    class Meta:
        model = AvailableSlot
        fields = ['venue', 'start_time', 'end_time']

        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SlotRequestForm(forms.ModelForm):
    class Meta:
        model = SlotRequest
        fields = ['slot']
