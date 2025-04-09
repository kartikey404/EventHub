## Message Sending View
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404

from events.forms import MessageForm
from events.models import Message


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('inbox')  # You'll create this view too
    else:
        # Artist can send to manger and wise versa

        if request.user.userprofile.user_type == 'artist':
            recipient = User.objects.filter(userprofile__user_type='manager')
        else:
            recipient = User.objects.filter(userprofile__user_type='artist')
        form = MessageForm()
        form.fields['recipient'].queryset = recipient

    return render(request, 'events/send_message.html', {'form': form})


@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-sent_at')
    messages.update(is_read=True)
    return render(request, 'events/inbox.html', {'messages': messages})


@login_required
def send_message_to(request, recipient_id):
    recipient = get_object_or_404(User, pk=recipient_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = recipient
            msg.save()
            messages.success(request, "Message sent!")
            return redirect('inbox')
    else:
        form = MessageForm(initial={'recipient': recipient})

    # Hide recipient dropdown
    form.fields['recipient'].widget = forms.HiddenInput()

    return render(request, 'events/send_message.html', {'form': form, 'recipient': recipient})


from django.contrib.auth.decorators import login_required

@login_required
def sent_messages(request):
    messages_sent = Message.objects.filter(sender=request.user).order_by('-sent_at')
    return render(request, 'events/sent_messages.html', {'messages': messages_sent})


@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)

    # Security: Make sure the user is part of the thread
    if request.user != message.sender and request.user != message.recipient:
        return redirect('inbox')

    replies = message.replies.all().order_by('sent_at')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.recipient = message.sender if message.sender != request.user else message.recipient
            reply.parent = message
            reply.save()
            messages.success(request, "Reply sent!")
            return redirect('message_detail', pk=message.pk)
    else:
        form = MessageForm()

    return render(request, 'events/message_detail.html', {
        'message': message,
        'replies': replies,
        'form': form
    })
