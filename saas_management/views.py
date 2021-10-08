from django.shortcuts import redirect

from customers.selectors import get_customer_space

def homepage(request):
    if request.user.is_authenticated:
        if request.user.is_owner:
            customer_space = get_customer_space(request.user)
            return redirect(f"{customer_space.get_base_url(request)}/")
        else:
            raise Exception("Not yet implemented") # TODO: redirect to user page
    return redirect("account_signup")
