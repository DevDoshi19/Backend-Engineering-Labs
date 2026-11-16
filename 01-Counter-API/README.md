**Project 01 — Counter API**

Beginner

Python · FastAPI · SQLAlchemy · PostgreSQL

We're not going to make this unnecessarily complicated.

### **Problem statement**

Build a simple counter service where users can create counters, increment them, decrement them and retrieve their current values.

### **Requirements**

| Method | Endpoint                   | Responsibility           |
| ------ | -------------------------- | ------------------------ |
| POST   | `/counters`                | Create a counter         |
| GET    | `/counters`                | Get all counters         |
| GET    | `/counters/{id}`           | Get a particular counter |
| PATCH  | `/counters/{id}/increment` | Increment by 1           |
| PATCH  | `/counters/{id}/decrement` | Decrement by 1           |
| DELETE | `/counters/{id}`           | Delete a counter         |

### **Concepts you'll learn**

1. HTTP methods and status codes.
2. FastAPI routing.
3. Request validation using Pydantic.
4. SQLAlchemy models.
5. Database sessions.
6. CRUD operations.
7. Exception handling.
8. PostgreSQL integration.
9. Project structure and separation of concerns.

Later, we'll revisit this same counter problem to introduce race conditions and database locking. That's where things get interesting!

# **6. Your first assignment**

Assignment 01

**Create the project folder&#x20;**`01-counter-api`**.**

Your first task is only to:

1. Initialize a Python virtual environment.
2. Install FastAPI and Uvicorn.
3. Create a basic FastAPI application.
4. Implement a `GET /` endpoint.
5. Return:

```
{
    "message": "Counter API is running"
}
```

6\. Run the server and test it through `/docs`.

**Don't implement the database or counter functionality yet.** We'll build incrementally.

One last thing: I want you to approach these projects as an engineer, not someone completing tutorials.
