# User Management System API Documentation

## Endpoints

### 1. Register
- **URL:** `/register`
- **Method:** POST
- **Description:** Register a new user
- **Parameters:**
  - username (string): User's username
  - email (string): User's email address
  - password (string): User's password
  - password2 (string): Password confirmation
- **Example:**
  ```
  POST /register
  {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "securepassword",
    "password2": "securepassword"
  }
  ```

### 2. Login
- **URL:** `/login`
- **Method:** POST
- **Description:** Authenticate a user
- **Parameters:**
  - email (string): User's email address
  - password (string): User's password
- **Example:**
  ```
  POST /login
  {
    "email": "johndoe@example.com",
    "password": "securepassword"
  }
  ```

### 3. Logout
- **URL:** `/logout`
- **Method:** GET
- **Description:** Log out the current user

### 4. Reset Password Request
- **URL:** `/reset_password_request`
- **Method:** POST
- **Description:** Request a password reset
- **Parameters:**
  - email (string): User's email address
- **Example:**
  ```
  POST /reset_password_request
  {
    "email": "johndoe@example.com"
  }
  ```

### 5. Reset Password
- **URL:** `/reset_password/<token>`
- **Method:** POST
- **Description:** Reset user's password using a token
- **Parameters:**
  - token (string): Password reset token (in URL)
  - password (string): New password
  - password2 (string): New password confirmation
- **Example:**
  ```
  POST /reset_password/abcdef123456
  {
    "password": "newpassword",
    "password2": "newpassword"
  }
  ```

### 6. Google Login
- **URL:** `/login/google`
- **Method:** GET
- **Description:** Initiate Google OAuth login process

### 7. Admin Panel
- **URL:** `/admin`
- **Method:** GET
- **Description:** Access the admin panel (requires 'admin' role)

## Authentication

Most endpoints require authentication. After successful login, the server will set a session cookie that should be included in subsequent requests.

## Error Handling

All endpoints will return appropriate HTTP status codes and error messages in case of failure.
