from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Tenant, Organization, Department, Customer

class MultiTenantTests(APITestCase):
    def setUp(self):
        # Create Tenants
        self.tenant1 = Tenant.objects.create(name="Tenant One", domain="tenant1.com")
        self.tenant2 = Tenant.objects.create(name="Tenant Two", domain="tenant2.com")

        # Create Users
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        # Assign Tokens
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

        # Create Organization under Tenant1
        self.org1 = Organization.objects.create(name="Org A", tenant=self.tenant1)
        self.org2 = Organization.objects.create(name="Org B", tenant=self.tenant2)

        # Create Department under Tenant1's Org
        self.dept1 = Department.objects.create(name="Dept A", organization=self.org1)

        # Create Customer under Dept1
        self.customer1 = Customer.objects.create(name="Cust A", department=self.dept1)

        self.client = APIClient()

    def test_unauthorized_access(self):
        response = self.client.get("/api/organizations/")
        self.assertEqual(response.status_code, 401)

    def test_organization_list_only_shows_tenant_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}",
                                HTTP_X_TENANT_DOMAIN="tenant1.com")
        response = self.client.get("/api/organizations/")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Org A")

    def test_prevent_cross_tenant_access(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}",
                                HTTP_X_TENANT_DOMAIN="tenant1.com")
        # Try accessing Tenant2's org
        response = self.client.get(f"/api/organizations/{self.org2.id}/")
        self.assertEqual(response.status_code, 404)

    def test_create_department(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}",
                                HTTP_X_TENANT_DOMAIN="tenant1.com")
        data = {"name": "New Dept", "organization": self.org1.id}
        response = self.client.post("/api/departments/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "New Dept")

    def test_cross_tenant_department_create_blocked(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}",
                                HTTP_X_TENANT_DOMAIN="tenant1.com")
        data = {"name": "Invalid Dept", "organization": self.org2.id}
        response = self.client.post("/api/departments/", data)
        self.assertEqual(response.status_code, 403)

    def test_delete_customer(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}",
                                HTTP_X_TENANT_DOMAIN="tenant1.com")
        response = self.client.delete(f"/api/customers/{self.customer1.id}/")
        self.assertEqual(response.status_code, 204)

    def test_tenant_isolation_on_customer_read(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}",
                                HTTP_X_TENANT_DOMAIN="tenant2.com")
        response = self.client.get(f"/api/customers/{self.customer1.id}/")
        self.assertEqual(response.status_code, 404)
