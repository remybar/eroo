from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django_tenants.models import DomainMixin

from tenant_users.tenants.models import TenantBase

class CustomerSpace(TenantBase):
    """
    A customer space on the Eroo platform, implements as a tenant.
    """
    name = models.CharField(max_length=100)

    def get_base_url(self, request):
        """
        Returns the base URL of this tenant.
        """
        http_type = 'https://' if request.is_secure() else 'http://'
        port = request.get_port()
        domain = get_current_site(request).domain
        return ''.join((http_type, self.slug, '.', domain, f":{port}" if port else ""))

class Domain(DomainMixin):
    pass
