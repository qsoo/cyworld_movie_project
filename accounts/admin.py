from django.contrib import admin
from .models import User, SendConnect, VisitorBook


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'nickname', 'profile_img']


@admin.register(SendConnect)
class SendConnectAdmin(admin.ModelAdmin):
    list_display = ['id', 'give_user', 'take_user', 'sure']


@admin.register(VisitorBook)
class VisitorBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'writer', 'content']

