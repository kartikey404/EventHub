from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render


def get_room_name(user1, user2):
    # Ensure consistent room names regardless of who starts the chat
    user_ids = sorted([str(user1.id), str(user2.id)])
    return "_".join(user_ids)


# @login_required
# def chat_view(request, user_id):
#     other_user = get_object_or_404(User, id=user_id)
#     room_name = get_room_name(request.user, other_user)
#     return render(request, "events/chat.html", {
#         "receiver": other_user,
#         "room_name": room_name
#     })

from django.db.models import Q

@login_required
def chat_view(request, user_id=None):
    user = request.user
    # Users the current user has chatted with
    chat_users = User.objects.filter(
        Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
    ).distinct()

    # default receiver or selected one
    receiver = get_object_or_404(User, id=user_id) if user_id else chat_users.first()

    room_name = f"{min(user.id, receiver.id)}_{max(user.id, receiver.id)}"
    return render(request, 'events/chat.html', {
        'receiver': receiver,
        'room_name': room_name,
        'chat_users': chat_users
    })




