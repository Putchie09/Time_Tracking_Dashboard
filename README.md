# TCU Hours Registry System

## ⚠️ Disclaimer
**This is a personal prototype project and should NOT be used as a production solution in its current state.** This system demonstrates conceptual improvements to university administrative workflows but lacks the security audits, compliance features, and institutional integration required for real-world deployment. It serves as a proof-of-concept for how digital transformation could improve TCU hour tracking processes.

## 📋 Project Overview

The **TCU Hours Registry System** is a personal prototype project developed to reimagine how universities could manage Trabajo Comunal Universitario (TCU) hours tracking. Born from questioning the efficiency of my university's current manual system, this web application demonstrates how digital transformation can streamline the process of recording, reviewing, and approving community service hours through an intuitive, role-based workflow.

**Note**: This is a demonstration system only. It has not been security-hardened or compliance-verified for actual university use.

## 👥 User Roles & Workflow

### 1. **Student Role**
- **Create Requests**: Submit hour registration requests with:
  - Number of hours worked
  - Activity date
  - Detailed description of activities performed
  - Supporting evidence/files (optional)
- **View History**: Track all submitted requests and their status
- **Access**: Limited to their own requests only

### 2. **Professor Role**
- **Review Requests**: View and evaluate hour requests from students assigned to their projects
- **Approve/Reject**: Accept or decline requests with appropriate feedback
- **Add Comments**: Provide additional comments or clarification
- **Scope**: Only sees requests from projects they are responsible for

### 3. **Administrator Role**
- **Global Management**: View all requests across the entire system
- **User Management**: Create, edit, and manage user accounts (students, professors, administrators)
- **Project Management**: Set up and configure TCU projects
- **Full Oversight**: Modify any request and manage system-wide operations

## 🚀 Features

- **Secure Authentication**: Role-based access control with password encryption
- **Request Management**: Complete workflow from submission to approval
- **File Uploads**: Support for evidence/documentation upload (PDF, images, documents)
- **Real-time Validation**: Form validation with immediate feedback
- **Dashboard Analytics**: Visual statistics and recent activity overview
- **Comment System**: Structured feedback mechanism for request reviews

## 🛠️ Technical Stack

- **Backend**: Django 5.2.3 (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: 
  - *Development*: SQLite3 (for simplified setup)
  - *Original Design*: MySQL (production-ready architecture)
- **Styling**: Custom CSS with some Bootstrap Icons
- **Security**: PBKDF2 password hashing, session-based authentication

## Project setup
- Apply database migrations: python manage.py migrate
- Create initial data and users
    -  **With default password (admin123)**
        - python manage.py create_initial_data
    - **Or with custom password**
        - python manage.py create_initial_data --password yourSecurePassword
- Run the development server
    - python manage.py runserver


# 👤 Default User Credentials *(For Testing Only)*

**Warning:** These are test credentials for demonstration purposes only. Never use default passwords in production systems.

| Role           | Email                      | Password                         |
|----------------|----------------------------|----------------------------------|
| Administrator  | admin@gmail.com            | admin123 (or your custom password) |
| Professor      | profesor@example.com       | prof123                          |
| Student        | estudiante@example.com     | estu123                          |
