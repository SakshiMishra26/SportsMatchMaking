from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from .models import FriendRequest, Message

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    sent_requests = FriendRequest.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)
    received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    accepted_friends = FriendRequest.objects.filter(
        models.Q(from_user=request.user, status='accepted') | 
        models.Q(to_user=request.user, status='accepted')
    ).values_list('to_user_id', flat=True).distinct()
    return render(request, 'chat/user_list.html', {
        'users': users,
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'accepted_friends': accepted_friends,
    })

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if request.user == to_user:
        messages.error(request, "You cannot send a friend request to yourself.")
        return redirect('chat:user_list')
    if not FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status='pending').exists():
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, f"Friend request sent to {to_user.username}.")
    return redirect('chat:user_list')

@login_required
def manage_friend_requests(request):
    received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    return render(request, 'chat/manage_friend_requests.html', {'requests': received_requests})

@login_required
def respond_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            friend_request.status = 'accepted'
            messages.success(request, f"Friend request from {friend_request.from_user.username} accepted.")
        elif action == 'reject':
            friend_request.status = 'rejected'
            messages.success(request, f"Friend request from {friend_request.from_user.username} rejected.")
        friend_request.save()
        return redirect('chat:manage_friend_requests')
    return render(request, 'chat/respond_friend_request.html', {'request': friend_request})

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        receiver = get_object_or_404(User, id=receiver_id)
        if FriendRequest.objects.filter(from_user=request.user, to_user=receiver, status='accepted').exists() or \
           FriendRequest.objects.filter(from_user=receiver, to_user=request.user, status='accepted').exists():
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'You are not friends with this user.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def get_messages(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if FriendRequest.objects.filter(from_user=request.user, to_user=receiver, status='accepted').exists() or \
       FriendRequest.objects.filter(from_user=receiver, to_user=request.user, status='accepted').exists():
        messages = Message.objects.filter(
            (models.Q(sender=request.user) & models.Q(receiver=receiver)) |
            (models.Q(sender=receiver) & models.Q(receiver=request.user))
        ).order_by('timestamp')
        print("Messages:", messages)  # Debug output
        messages.update(is_read=True)
        return render(request, 'chat/messages.html', {'messages': messages, 'receiver': receiver})
    messages.error(request, "You can only chat with friends.")
    return redirect('chat:user_list')

@login_required
def friends_list(request):
    friends = User.objects.filter(
        models.Q(sent_requests__to_user=request.user, sent_requests__status='accepted') |
        models.Q(received_requests__from_user=request.user, received_requests__status='accepted')
    ).distinct()
    return render(request, 'chat/friends_list.html', {'friends': friends})