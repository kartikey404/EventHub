from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    USER_TYPES = [
        ('artist', 'Artist'),
        ('manager', 'Event Manager'),
        ('guest', 'Guest'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    bio = models.TextField(blank=True)
    genre = models.CharField(max_length=100, blank=True)  # Only if artist
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"


class Venue(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='venues')
    name = models.CharField(max_length=255)
    address = models.TextField()
    type = models.CharField(max_length=50)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EventRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'userprofile__user_type': 'artist'})
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    date = models.DateField(default=None)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.venue.name} - {self.artist.username} - {self.status}"



class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1–5 stars

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True, blank=True)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='artist_reviews')
    comment = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.venue.name if self.venue else self.artist.username
        return f"{self.reviewer.username} → {target} ({self.rating})"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')


    def __str__(self):
        return f"From {self.sender} to {self.recipient}: {self.subject}"



class ConfirmedEvent(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'userprofile__user_type': 'artist'})
    date = models.DateField()
    created_from = models.OneToOneField('EventRequest', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.artist.username} at {self.venue.name} on {self.date}"

