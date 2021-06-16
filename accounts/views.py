from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

User = get_user_model()


class DeleteAccountView(LoginRequiredMixin, TemplateView):
    template_name = "account/delete.html"

    def post(self, request):
        account = User.objects.get(username=request.user)
        if account is not None:
            account.delete()
            logout(request)
            return HttpResponseRedirect("/")  # TODO : use a const/view name ?
        return render(request, self.template_name)
