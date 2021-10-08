from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from customers.models import CustomerSpace

@admin.register(CustomerSpace)
class CustomerSpaceAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('name',)
