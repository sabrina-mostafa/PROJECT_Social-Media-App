from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.models import Profile, FollowersCount, Friend, ChatMessage
from .forms import ChatMessageForm
from django.http import JsonResponse
from itertools import chain
import random, json

# Create your view here...
def index(request):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)
    
    user_following_list = []
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    ffriends_list = [x for x in list(all_users) if (x in list(user_following_all))]

    current_user = User.objects.filter(username=request.user.username)
    ffinal_friends_list = [x for x in list(ffriends_list) if ( x not in list(current_user))]
    # random.shuffle(ffinal_friends_list)

    ff_username_profile = []
    ff_username_profile_list = []

    for ffrnds in ffinal_friends_list:
        ff_username_profile.append(ffrnds.id)

    for ff_ids in ff_username_profile:
        ff_profile_lists = Profile.objects.filter(id_user=ff_ids)
        ff_username_profile_list.append(ff_profile_lists)

    ffriends_username_profile_list = list(chain(*ff_username_profile_list))
    
    context = {"user": user, "ffriends": ffriends_username_profile_list, 'user_profile': user_profile}
    return render (request, 'mychatapp/index.html', context)


def detail(request, pk):
    friend = Profile.objects.get(id_user=pk) #this

    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)            #sender
    profile = Profile.objects.get(id_user=friend.id_user)    # receiver
    
    chats = ChatMessage.objects.all()
    rec_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user_profile)
    rec_chats.update(seen=True)

    form = ChatMessageForm()
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user_profile
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect("detail", pk=friend.id_user)
    context = {"friend": friend, "form": form, "user_profile": user_profile, "profile": profile, "chats": chats, "num": rec_chats.count()}
    return render(request, "mychatapp/detail.html", context)


def sentMessages(request, pk):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)            #sender
    friend = Profile.objects.get(id_user=pk)
    profile = Profile.objects.get(id_user=friend.id_user)    # receiver
    
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user_profile, msg_receiver=profile, seen=False)
    print(new_chat)
    return JsonResponse(new_chat_message.body, safe=False)


def receivedMessages(request, pk):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)            #sender
    friend = Profile.objects.get(id_user=pk)
    profile = Profile.objects.get(id_user=friend.id_user)    # receiver
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user_profile)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)


def chatNotification(request):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)
    
    user_following_list = []
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    ffriends_list = [x for x in list(all_users) if (x in list(user_following_all))]

    current_user = User.objects.filter(username=request.user.username)
    ffinal_friends_list = [x for x in list(ffriends_list) if ( x not in list(current_user))]
    # random.shuffle(ffinal_friends_list)

    ff_username_profile = []
    ff_username_profile_list = []

    for ffrnds in ffinal_friends_list:
        ff_username_profile.append(ffrnds.id)

    for ff_ids in ff_username_profile:
        ff_profile_lists = Profile.objects.filter(id_user=ff_ids)
        ff_username_profile_list.append(ff_profile_lists)

    ffriends_username_profile_list = list(chain(*ff_username_profile_list))
    arr = []
    for friend in ffriends_username_profile_list:
        profile = Profile.objects.get(id_user=friend.id_user)
        chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user_profile, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)