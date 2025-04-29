# 🛠️ Hudoor - Backend
## 📦 Project Description

Hudoorr is a full-stack attendance tracking system designed for schools and educational institutions. The backend, built with Django and Django REST Framework, handles authentication, attendance logic, and database interactions. It supports three main user roles:

- **Student**: Can view their own attendance records.
- **Teacher**: Can review attendance reports.
- **Attendance Officer**: Can manage and record daily attendance, trigger absence notifications, and export data.

This backend serves as the core API service for the React.js frontend client.

---

## 🧰 Tech Stack

## Tech Stack
- **Django** - Web framework for building the backend.
- **Django REST Framework (DRF)** - API framework to build RESTful APIs.
- **PostgreSQL** - Database to store the user and attendance data.
- **JWT Authentication** - Secure user authentication using JSON Web Tokens.
- **Django CORS Headers** - To enable Cross-Origin Resource Sharing (CORS).
- **Djoser** - For handling JWT authentication with Django.

---

## Frontend Repo Link
[Hudoorr Frontend Repo]()

---

## Link to Deployed Site
[Link to Deployed Backend]()

---

## 👥 User Roles and Permissions

| Role                | Permissions |
|---------------------|-------------|
| Attendance Officer   | Full CRUD access to classrooms, users, attendance, and reports. |
| Teacher              | Read-only access to their assigned classrooms and students’ attendance. |
| Student              | Read-only access to their personal attendance summary and notifications. |

---

## 🛣️ Routing Table

### 1. User Routes
| Route                   | Method | Description                   | Role Required      |
|--------------------------|--------|-------------------------------|--------------------|
| `/api/users`             | GET    | Get all users                 | Officer            |
| `/api/users/:id`         | GET    | Get user by ID                | Officer, Teacher   |
| `/api/users`             | POST   | Create new user               | Officer            |
| `/api/users/:id`         | PUT    | Update user                   | Officer, Self-update |
| `/api/users/:id`         | DELETE | Delete user                   | Officer            |

---

### 2. RoleModel Routes
| Route                   | Method | Description                   | Role Required      |
|--------------------------|--------|-------------------------------|--------------------|
| `/api/roles`             | GET    | Get all roles                 | Officer            |
| `/api/roles/:id`         | GET    | Get role by ID                | Officer            |
| `/api/roles`             | POST   | Create new role               | Officer            |
| `/api/roles/:id`         | PUT    | Update role                   | Officer            |
| `/api/roles/:id`         | DELETE | Delete role                   | Officer            |

> **Note:** There are only 3 role types: Officer, Teacher, Student.

---

### 3. ClassRoom Routes
| Route                   | Method | Description                   | Role Required      |
|--------------------------|--------|-------------------------------|--------------------|
| `/api/classrooms`        | GET    | Get all classrooms            | Officer, Teacher   |
| `/api/classrooms/:id`    | GET    | Get classroom by ID           | Officer, Teacher   |
| `/api/classrooms`        | POST   | Create new classroom          | Officer            |
| `/api/classrooms/:id`    | PUT    | Update classroom              | Officer            |
| `/api/classrooms/:id`    | DELETE | Delete classroom              | Officer            |

---

### 4. AttendanceProcess Routes
| Route                   | Method | Description                          | Role Required      |
|--------------------------|--------|--------------------------------------|--------------------|
| `/api/attendance`        | GET    | Get all attendance records          | Officer, Teacher   |
| `/api/attendance/:id`    | GET    | Get attendance record by ID          | Officer, Teacher   |
| `/api/attendance`        | POST   | Mark attendance for a classroom      | Officer            |
| `/api/attendance/:id`    | PUT    | Update attendance status             | Officer            |
| `/api/attendance/:id`    | DELETE | Delete attendance record             | Officer            |

---

### 5. Report Routes
| Route                   | Method | Description                   | Role Required      |
|--------------------------|--------|-------------------------------|--------------------|
| `/api/reports`           | GET    | Get all reports               | Officer, Teacher   |
| `/api/reports/:id`       | GET    | Get report by ID              | Officer, Teacher   |
| `/api/reports`           | POST   | Create new report             | Officer            |
| `/api/reports/:id`       | DELETE | Delete report                 | Officer            |

---

## ERD Diagram
![ERD Diagram](/AttendanceProject/description_backend/ERD.png)
