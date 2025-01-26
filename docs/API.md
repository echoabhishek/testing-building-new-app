# User Management System API Documentation

## Authentication Endpoints

### Register a new user

- **URL:** `/auth/register`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword"
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:** `{ "message": "User created successfully" }`

### Login

- **URL:** `/auth/login`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "username": "existinguser",
    "password": "correctpassword"
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:** `{ "access_token": "<JWT_TOKEN>" }`

### Access Protected Route

- **URL:** `/auth/protected`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Success Response:**
  - **Code:** 200
  - **Content:** `{ "logged_in_as": "username" }`

### Admin Dashboard

- **URL:** `/auth/admin/dashboard`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>` (must be an admin user)
- **Success Response:**
  - **Code:** 200
  - **Content:** `{ "message": "Welcome to the admin dashboard" }`

### Forgot Password

- **URL:** `/auth/forgot-password`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:** `{ "message": "Password reset email sent" }`

### Reset Password

- **URL:** `/auth/reset-password/<token>`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "new_password": "newsecurepassword"
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:** `{ "message": "Password reset successful" }`

## OAuth Authentication

### Google OAuth Login

- **URL:** `/login/google`
- **Method:** `GET`
- **Description:** Redirects to Google for authentication

## Usage Examples

### Register a new user

```bash
curl -X POST http://localhost:5000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username": "newuser", "email": "newuser@example.com", "password": "securepassword"}'
```

### Login

```bash
curl -X POST http://localhost:5000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "existinguser", "password": "correctpassword"}'
```

### Access Protected Route

```bash
curl -X GET http://localhost:5000/auth/protected \
     -H "Authorization: Bearer <JWT_TOKEN>"
```

### Access Admin Dashboard

```bash
curl -X GET http://localhost:5000/auth/admin/dashboard \
     -H "Authorization: Bearer <JWT_TOKEN>"
```

### Forgot Password

```bash
curl -X POST http://localhost:5000/auth/forgot-password \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com"}'
```

### Reset Password

```bash
curl -X POST http://localhost:5000/auth/reset-password/<token> \
     -H "Content-Type: application/json" \
     -d '{"new_password": "newsecurepassword"}'
```

