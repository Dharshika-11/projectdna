from django.contrib import admin
from .models import ChatMessage, Notification, DiscussionTopic, DiscussionReply

admin.site.register(ChatMessage)
admin.site.register(Notification)
admin.site.register(DiscussionTopic)
admin.site.register(DiscussionReply)
