# 🏢 Multi-Tenant Django Application

This Django prototype demonstrates a **multi-tenant architecture** with four organizational levels:

> **Tenant → Organization → Department → Customer**

---

## 🚀 Features

- Isolated tenant environments
- RESTful APIs for CRUD operations at every level
- Token-based authentication (DRF TokenAuth)
- Tenant recognition via custom middleware (`X-Tenant-Domain` header)
- Optional PostgreSQL + Docker support
- Unit tests for isolation and permission enforcement

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/multi-tenancy.git
cd multi-tenancy
2. Set Up Virtual Environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Apply Migrations
python manage.py migrate
5. Create a Superuser
python manage.py createsuperuser
6. Run the Server
python manage.py runserver
🏗️ Architecture Overview
📌 Organizational Structure:

Tenant
  └── Organization (FK → Tenant)
        └── Department (FK → Organization)
              └── Customer (FK → Department)
Every request is filtered based on the Tenant context.

Users can only access or modify data belonging to their tenant.

A custom middleware sets request.tenant from the X-Tenant-Domain request header.

🔐 Authentication & Authorization
Uses Django's built-in User model with DRF Token Authentication.

All API endpoints are protected — only authenticated users can access them.

Example Header:
makefile
Authorization: Token <your-token>
X-Tenant-Domain: tenant1.com
📡 API Endpoints
Resource	Endpoint	Method	Description
Tenant	/api/tenants/	GET	List all tenants
/api/tenants/	POST	Create a new tenant
/api/tenants/{id}/	GET	Get tenant details
Organization	/api/organizations/	GET	List organizations (by tenant)
/api/organizations/	POST	Create organization under tenant
/api/organizations/{id}/	GET	Get organization details
Department	/api/departments/	GET	List departments (by org + tenant)
/api/departments/	POST	Create department under organization
/api/departments/{id}/	GET	Get department details
Customer	/api/customers/	GET	List customers (by dept + tenant)
/api/customers/	POST	Create customer under department
/api/customers/{id}/	GET	Get customer details

🧠 Middleware: Tenant Context
Middleware extracts the tenant domain from the request header:

X-Tenant-Domain: tenant1.com
It sets request.tenant, and all views filter data accordingly via get_queryset() and perform_create() overrides.

✅ Testing
Run unit tests:
python manage.py test main_app
Tests include:

✅ Tenant isolation

✅ Permission enforcement

✅ Full CRUD on organizations, departments, and customers

🐳 Docker (Optional)
If using Docker and PostgreSQL:
docker-compose up --build
Ensure you have a .env file with:

env

POSTGRES_DB=multi_tenancy
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
📁 Project Structure
multi_tenancy/
├── main_app/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── middleware.py
│   ├── tests.py
│   └── urls.py
├── multi_tenancy/
│   └── settings.py
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── README.md
