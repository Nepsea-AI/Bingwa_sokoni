from django.contrib import admin

# Register your models here.
from settings.models import UserProfile, Message

admin.site.register(UserProfile)
admin.site.register(Message)