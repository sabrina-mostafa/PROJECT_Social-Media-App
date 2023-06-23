from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount, Friend, ChatMessage
# from mychatapp.models import Friend

# Register your models here.
admin.site.register([Profile, Friend])
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(ChatMessage)
