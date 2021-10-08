from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ErooUserCreationForm, ErooUserChangeForm
from .models import ErooUser


# class ErooUserAdmin(UserAdmin):
#     # add_form = ErooUserCreationForm
#     # form = ErooUserChangeForm
#     model = ErooUser
#     list_display = ['email', 'username', ]


# admin.site.register(ErooUser, ErooUserAdmin)
