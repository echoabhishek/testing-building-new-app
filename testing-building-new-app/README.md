# User Management System

This is a Flask-based user management system that includes user registration, login, role-based access control, and password reset functionality.

## Features

- User registration
- User login
- Role-based access control
- Password reset request
- Admin panel (protected route)

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/app.py
   ```

4. Run the tests:
   ```
   python -m pytest tests/test_user_management.py
   ```

## API Endpoints

- POST /register: Register a new user
- POST /login: Login a user
- POST /reset-password: Request a password reset
- GET /admin: Access the admin panel (requires admin role)

## Usage Examples

### Register a new user
```
curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username":"newuser", "email":"newuser@example.com", "password":"password123"}'
```

### Login
```
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username":"newuser", "password":"password123"}'
```

### Request password reset
```
curl -X POST http://localhost:5000/reset-password -H "Content-Type: application/json" -d '{"email":"newuser@example.com"}'
```

### Access admin panel (requires admin role and login)
```
curl -X GET http://localhost:5000/admin -H "Cookie: session=<session-cookie>"
```

## Note

This is a basic implementation and should be enhanced with additional security measures for production use, such as:

- Implementing HTTPS
- Adding CSRF protection
- Implementing proper password reset flow with tokens
- Adding rate limiting to prevent brute-force attacks
- Implementing email verification for new user registrations

