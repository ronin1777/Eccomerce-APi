from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.admin import UserAdmin

from shop.auths.users.models import User, Profile


# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile


class DjshopUserAdmin(UserAdmin):
    list_display = ('id', "username", "email", "first_name", "last_name", "is_staff", "verified_email")


UserAdmin.inlines = [ProfileInline]
admin.site.register(User, DjshopUserAdmin)
