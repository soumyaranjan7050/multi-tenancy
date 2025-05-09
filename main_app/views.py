from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Tenant, Organization, Department, Customer
from .serializers import *

# TenantViewSet - visible only to admin or system superusers
class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]

# Organization CRUD - filtered by request.tenant
class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(tenant=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

    def perform_update(self, serializer):
        if serializer.instance.tenant != self.request.tenant:
            raise PermissionDenied("You do not have permission to update this organization.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.tenant != self.request.tenant:
            raise PermissionDenied("You do not have permission to delete this organization.")
        instance.delete()

# Department CRUD - filtered by tenant via organization
class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Department.objects.filter(organization__tenant=self.request.tenant)

    def perform_create(self, serializer):
        if serializer.validated_data['organization'].tenant != self.request.tenant:
            raise PermissionDenied("Invalid organization for current tenant.")
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.organization.tenant != self.request.tenant:
            raise PermissionDenied("You do not have permission to update this department.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.organization.tenant != self.request.tenant:
            raise PermissionDenied("You do not have permission to delete this department.")
        instance.delete()

# Customer CRUD - filtered by tenant via department > organization
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(department__organization__tenant=self.request.tenant)

    def perform_create(self, serializer):
        if serializer.validated_data['department'].organization.tenant != self.request.tenant:
            raise PermissionDenied("Invalid department for current tenant.")
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.department.organization.tenant != self.request.tenant:
            raise PermissionDenied("You do not have permission to update this customer.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.department.organization.tenant != self.request.tenant:
            raise PermissionDenied("You do not have permission to delete this customer.")
        instance.delete()
