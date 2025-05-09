from main_app.models import Tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        domain = request.META.get('HTTP_X_TENANT_DOMAIN')
        request.tenant = Tenant.objects.filter(domain=domain).first()
        return self.get_response(request)
