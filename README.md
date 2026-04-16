# Module 10

## Module Overview

This module builds a full FastAPI application with authentication, database integration, testing, and deployment. The goal was to understand how backend systems are developed, secured, tested, and deployed using modern tools like Docker and CI/CD pipelines.

---

## Docker Setup

I started the application using:

```bash
docker compose up --build
```

This will start:

- FastAPI application  
- PostgreSQL database  
- pgAdmin interface  

---

## Docker Hub Repository

 <https://hub.docker.com/r/bry633/module-10-assignment>

---

## Access Application

FastAPI:
<http://localhost:8000>

pgAdmin:
<http://localhost:5050>

Login (based on docker-compose):

- Email: <admin@example.com>  
- Password: admin  

---

## Database Connection

Connect to PostgreSQL using:

- Host: db  
- Username: postgres  
- Password: postgres  
- Database: fastapi_db  

---

## Authentication Features

The application includes user authentication using JWT.

### User Registration

- Users can register with:
  - first name  
  - last name  
  - email  
  - username  
  - password  

- Passwords are securely hashed using bcrypt.

---

### User Login

- Users can log in with username or email  
- A JWT token is generated upon successful authentication  
- Token is used to access protected routes  

---

## API Operations

### 1: Create User

Handled through the registration logic in the application.

---

### 2: Authenticate User

- Verifies credentials  
- Updates last login timestamp  
- Returns JWT token  

---

### 3: Protected Access

- Uses dependency injection to verify user tokens  
- Ensures only authenticated users can access certain routes  

---

## Testing

Run tests using:

```bash
pytest -q
```

Test coverage includes:

- Unit tests  
- Integration tests  
- Schema validation tests  

Results:

- 100% test coverage  
- All tests passed  

---

## CI/CD Pipeline

The project uses GitHub Actions for automation.

### Pipeline Steps

1: Run Tests  

- Install dependencies  
- Execute pytest  

2: Security Scan  

- Build Docker image  
- Scan with Trivy for vulnerabilities  

3: Deploy  

- Log in to Docker Hub  
- Build and push Docker image  

---

## Docker Image

The application is built and pushed to Docker Hub automatically through CI/CD.

Image includes:

- FastAPI application  
- Updated secure dependencies  
- PostgreSQL connection support  

---

## Security

- Passwords are hashed using bcrypt  
- JWT tokens used for authentication  
- Dependencies updated to fix vulnerabilities  
- Trivy scan ensures no high/critical issues  

---

## Documentation

- [Module10_Screenshots.pdf](./Module10_Screenshots.pdf) – Screenshots of successful execution of GitHub Actions and Docker Hub Repo with deployed application image
- [Module10_Reflection.pdf](./Module10_Reflection.pdf) – Reflection on the assignment  

---
