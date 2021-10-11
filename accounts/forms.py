from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from allauth.account.forms import SignupForm

from .models import ErooUser


class ErooUserCreationForm(UserCreationForm):

    class Meta:
        model = ErooUser
        fields = ('username', 'email')


class ErooUserChangeForm(UserChangeForm):

    class Meta:
        model = ErooUser
        fields = ('username', 'email')

class ErooUserSignUpForm(SignupForm):
    is_owner = forms.BooleanField(required=False)

    def save(self, request):
        user = super(ErooUserSignUpForm, self).save(request)
        user.is_owner = self.cleaned_data['is_owner']
        user.save()

        return user
