from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

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
