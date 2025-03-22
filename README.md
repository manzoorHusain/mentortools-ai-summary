
# 🧠 AI-Powered Online Course Summary Generator

This is a FastAPI-based backend project for **Mentortools** that allows course creators to automatically generate short summaries of their courses using the OpenAI API.

---

## 📌 Project Overview

Mentortools wants to help **course creators** save time by using AI to generate short, concise summaries of their course descriptions.

This backend service provides:

- 📬 User and course creation
- 🤖 AI-generated summaries using GPT
- 🔐 API key-based protection for summary routes
- 🚦 Rate-limiting (3 summaries per user per hour)
- ✍️ Manual editing of AI summaries after generation

---

## 🚀 Features

- ✅ Async FastAPI backend
- ✅ PostgreSQL with SQLAlchemy ORM
- ✅ OpenAI GPT-3.5 integration
- ✅ API Key authentication
- ✅ Rate-limiting logic
- ✅ Swagger documentation (`/docs`)
- ✅ Fully testable locally

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy (async)**
- **PostgreSQL**
- **OpenAI API**
- **Pydantic**
- **Uvicorn**

---

## 📸 Example Flow

> _Course creator submits a new course → hits "Generate Summary" → AI creates summary → user can optionally edit it manually before finalizing._

_(You can optionally include screenshots or Swagger UI here)_

---

## 📦 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/mentortools-ai-summary.git
cd mentortools-ai-summary
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Create a `.env` File

First, copy the example:

```bash
cp .env.example .env
```

Then open `.env` and fill in your actual credentials:
- `OPENAI_API_KEY`
- `API_KEY`
- `DATABASE_URL`

---

## 🔐 .env.example

```env
# OpenAI API key from https://platform.openai.com/account/api-keys
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Your own app’s internal API key to protect AI routes
API_KEY=secret123

# PostgreSQL Database connection string
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/your_db_name
```

---

## ▶️ Run the App

```bash
uvicorn main:app --reload
```

Then open your browser at:

```
http://localhost:8000/docs
```

Here you’ll find **interactive Swagger documentation** to test every route.

---

## 📬 API Endpoints

### 👤 Users
| Method | Endpoint          | Description         |
|--------|-------------------|---------------------|
| POST   | /users            | Create a new user   |
| GET    | /users/{id}       | Get user by ID      |
| GET    | /users            | Get all users       |
| PUT    | /users/{id}       | Update user         |
| DELETE | /users/{id}       | Delete user         |

### 📚 Courses
| Method | Endpoint                  | Description                        |
|--------|---------------------------|------------------------------------|
| POST   | /courses                  | Create a new course                |
| GET    | /courses                  | Get all courses                    |
| GET    | /courses/{id}            | Get course by ID                   |
| PUT    | /courses/{id}            | Update course                      |
| DELETE | /courses/{id}            | Delete course                      |
| POST   | /generate_summary/{id}   | 🔐 Generate summary using OpenAI   |
| PUT    | /courses/{id}/summary    | ✍️ Manually update AI summary      |

---

## 🔒 Protected Routes

- All `/generate_summary/...` endpoints are protected by an API key
- Pass it in headers:
  ```
  x-api-key: secret123
  ```

---

## 🛡️ Rate-Limiting

Each user can generate **max 3 summaries per hour**.
Further requests will return:

```json
{
  "detail": "Rate limit exceeded: You can only generate 3 summaries per hour."
}
```

---

## 📦 Optional Improvements

- ✅ Docker support
- ✅ Frontend integration
- ✅ Role-based permissions
- ✅ Admin dashboards

---

## 👨‍💻 Author

- **Asad** – Patient Care Coordinator, Health Tourism Specialist, and Full-Stack Dev in progress 🚀

---
