from allauth.account.forms import SignupForm

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ErooUser

class ErooUserCreationForm(UserCreationForm):

    class Meta:
        model = ErooUser
        fields = ('email',)


class ErooUserChangeForm(UserChangeForm):

    class Meta:
        model = ErooUser
        fields = ('email',)


class ErooUserSignUpForm(SignupForm):
    is_owner = forms.BooleanField(required=False)
    spacename = forms.CharField(max_length=32)

    def save(self, request):
        user = super(ErooUserSignUpForm, self).save(request)
        user.is_owner = self.cleaned_data['is_owner']
        user.spacename = self.cleaned_data['spacename']
        user.save()

        return user
