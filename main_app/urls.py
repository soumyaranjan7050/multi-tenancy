from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'tenants', TenantViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
