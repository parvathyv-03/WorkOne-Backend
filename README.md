# WORKONE HRMS - Backend

---

# About

**WORKONE HRMS Backend** is a RESTful API developed using **Python, Django, and Django REST Framework** to power the WORKONE Human Resource Management System. It provides secure JWT-based authentication, role-based access control (RBAC), and APIs for managing employees, attendance, leave requests, complaints, notifications, payroll, analytics, and other core HR operations. The backend follows a modular architecture to ensure secure, scalable, and efficient communication with the React frontend.

---

# Features

## Authentication & Security

- JWT Authentication
- Role-Based Access Control (RBAC)
- Secure User Authentication

---

# 🛠 Tech Stack

Technology 

- Python
- Django 
- Django REST Framework 
- SQLite
- JWT - Authentication

---

# 📂 Project Structure

```text
backend/
│
├── accounts/
├── attendance/
├── complaint/
├── documents/
├── employees/
├── hr/
├── leave_management/
├── notification/
├── payslip/
├── recruitment/
├── reports/
├── workone/
├── manage.py
├── requirements.txt
└── db.sqlite3
```

---

# 🔑 Authentication

The backend uses **JSON Web Tokens (JWT)** for secure authentication.

### Login

```http
POST /api/login/
```

Successful authentication returns:

- Access Token
- Refresh Token

---
# 🔒 Role-Based Access Control (RBAC)

The application enforces role-based authorization to ensure users can only access resources permitted for their role.

### Employee

- View and update profile
- Upload Documents
- Change password
- View attendance and check-in
- Get Attendance Monthly Report
- Apply for leave
- Track leave status
- Submit complaints
- View notifications
- Access payslips

### HR

- Manage employee records
- Manage employee documents
- Approve or reject leave requests
- Manage attendance
- Handle complaints
- Publish notifications
- Manage payslips
- View analytics and reports
- Manage Recruitment activities

---

# API Testing

The REST APIs was tested using Postman.

---



