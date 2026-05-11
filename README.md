# Team Task Manager

A modern collaborative task management web application built using Django.  
This platform allows teams to create projects, assign tasks, track progress, and manage collaboration efficiently through a clean and responsive interface.

---

# Features

- User Authentication System
- Team-based Project Management
- Task Creation and Assignment
- Task Status Tracking
- Dashboard Analytics
- Role-based Access
- Admin-controlled Project Completion
- Shared Task Visibility within Teams
- Responsive Modern UI
- Email-based Authentication
- Secure Login Protection using Django Axes
- PostgreSQL Database Support
- Railway Cloud Deployment

---

# Tech Stack

## Backend
- Django
- Django REST Framework

## Frontend
- HTML
- CSS
- JavaScript

## Database
- PostgreSQL

## Deployment
- Railway

---

# Project Structure
```
TeamTaskManager/
│
├── accounts/
├── dashboard/
├── projects/
├── tasks/
├── static/
├── templates/
├── taskmanager/
│
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
└── README.md
```
---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/TeamTaskManager.git
cd TeamTaskManager
```

## Create Virtual Environment
```
python -m venv venv
```

## Activate Virtual Environment
```
venv\Scripts\activate
```

## Install Dependencies
```
pip install -r requirements.txt
```

## Run Migrations
```
python manage.py migrate
```

## Create Superuser
```
python manage.py createsuperuser
```

## Run Development Server
```
python manage.py runserver
```
## Environment Variables

Create a .env file in the project root:
```
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```
---
# Railway Deployment

## Required Files :
- Procfile
- runtime.txt
- requirements.txt

## Railway Deployment Steps

- Push project to GitHub
- Create new Railway project
- Connect GitHub repository
- Add PostgreSQL database
- Add environment variables
- Deploy application
  
## Static Files Configuration
Static assets are stored inside:
```
/static
```
Django WhiteNoise is used for production static file serving.

Admin Panel

Access Django admin panel:
```
/admin
```

Example:
```
https://your-domain.up.railway.app/admin
```
---
# Security Features
- CSRF Protection
- Login Attempt Limiting using Django Axes
- Environment Variable Protection
- Secure Authentication System
---

# Future Improvements
- Real-time Notifications
- Team Chat System
- File Attachments
- Activity Logs
- Task Priority Levels
- Dark/Light Theme Toggle
---
# Author
Ashwin Raj
