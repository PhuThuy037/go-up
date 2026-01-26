# 🚀 Go-Up Backend (FastAPI)

> **Go-Up** is a learning-oriented backend project built to practice **modern backend development** with FastAPI.
> The goal of this phase is simple: **build real, practical backend features while keeping the codebase clean and scalable.**

---

## ✨ Features Implemented

### 👤 User Management

* Create user
* Get user by ID / username
* Update user information (PATCH)
* Delete user

---

### 📁 Project Management

* Create project
* Add members to a project
* List projects a user belongs to
* Basic role separation (Owner / Member – logic-ready)

---

### ✅ Task Management

* Create tasks
* Update tasks (partial update)
* Mark task as done / undone
* List tasks by project

---

### 💬 Comment System

* Add comments to tasks
* List comments by task
* User-based comment ownership

---

### 🔐 Authentication (In Progress / Planned)

* Password hashing
* JWT-based authentication (planned)
* Route protection by user role (planned)

---

### 🗄️ Database

* PostgreSQL
* Schema versioning with Alembic
* Relational modeling (User ↔ Project ↔ Task ↔ Comment)

---

### 🐳 Development Environment

* Docker Compose for local development
* PostgreSQL container
* pgAdmin for DB inspection

---

## 🧭 Phase Scope (Go-Up)

This phase intentionally focuses on:

* Core CRUD features
* Clear data relationships
* Clean API contracts
* Realistic backend workflows

Out of scope for this phase:

* Microservices
* Advanced async optimization
* Heavy caching
* Over-engineered abstractions

---

## 🛣️ Next Steps

* JWT Authentication
* Role-based access control
* Pagination (Keyset)
* Background tasks
* Basic test coverage

---

## 👨‍💻 Author

Built as a **skill-up backend project** to move from legacy systems toward modern backend architecture.

> This project favors clarity and correctness over premature optimization.
