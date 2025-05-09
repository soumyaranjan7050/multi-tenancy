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
