from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from .models import Tenant, Organization, Department, Customer
from .serializers import *

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(tenant=self.request.tenant)

    def perform_create(self, serializer):
        try:
            serializer.save(tenant=self.request.tenant)
        except Exception as e:
            raise PermissionDenied(f"Could not create organization: {str(e)}")

    def perform_update(self, serializer):
        try:
            if serializer.instance.tenant != self.request.tenant:
                raise PermissionDenied("You do not have permission to update this organization.")
            serializer.save()
        except Organization.DoesNotExist:
            raise NotFound("Organization not found.")

    def perform_destroy(self, instance):
        if instance.tenant != self.request.tenant:
            raise PermissionDenied("You do not have permission to delete this organization.")
        instance.delete()


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Department.objects.filter(organization__tenant=self.request.tenant)

    def perform_create(self, serializer):
        try:
            org = serializer.validated_data['organization']
            if org.tenant != self.request.tenant:
                raise PermissionDenied("Invalid organization for current tenant.")
            serializer.save()
        except KeyError:
            raise PermissionDenied("Organization is required.")
        except Exception as e:
            raise PermissionDenied(f"Could not create department: {str(e)}")

    def perform_update(self, serializer):
        try:
            if serializer.instance.organization.tenant != self.request.tenant:
                raise PermissionDenied("You do not have permission to update this department.")
            serializer.save()
        except Department.DoesNotExist:
            raise NotFound("Department not found.")

    def perform_destroy(self, instance):
        if instance.organization.tenant != self.request.tenant:
            raise PermissionDenied("You do not have permission to delete this department.")
        instance.delete()


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(department__organization__tenant=self.request.tenant)

    def perform_create(self, serializer):
        try:
            dept = serializer.validated_data['department']
            if dept.organization.tenant != self.request.tenant:
                raise PermissionDenied("Invalid department for current tenant.")
            serializer.save()
        except KeyError:
            raise PermissionDenied("Department is required.")
        except Exception as e:
            raise PermissionDenied(f"Could not create customer: {str(e)}")

    def perform_update(self, serializer):
        try:
            if serializer.instance.department.organization.tenant != self.request.tenant:
                raise PermissionDenied("You do not have permission to update this customer.")
            serializer.save()
        except Customer.DoesNotExist:
            raise NotFound("Customer not found.")

    def perform_destroy(self, instance):
        if instance.department.organization.tenant != self.request.tenant:
            raise PermissionDenied("You do not have permission to delete this customer.")
        instance.delete()
