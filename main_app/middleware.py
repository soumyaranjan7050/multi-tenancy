from django.utils.deprecation import MiddlewareMixin
from .models import Tenant

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        domain = request.META.get('HTTP_X_TENANT_DOMAIN')  # custom header
        if domain:
            try:
                tenant = Tenant.objects.get(domain=domain)
                request.tenant = tenant
            except Tenant.DoesNotExist:
                request.tenant = None
        else:
            request.tenant = None
