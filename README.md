# Authentication & Payment Server

A Node.js/Express server with JWT authentication and Stripe payment integration.

## Features

- **Authentication System**
  - User registration (signup)
  - User login (signin)
  - JWT token-based authentication
  - Password hashing with bcrypt
  - Protected routes with middleware
  - User profile management

- **Payment Integration**
  - Stripe payment processing
  - Payment intent creation
  - Payment confirmation
  - Payment history tracking
  - Webhook handling for payment events
  - Automatic customer creation in Stripe

- **Security Features**
  - Rate limiting
  - CORS configuration
  - Helmet security headers
  - Input validation and sanitization
  - Environment variables for sensitive data

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   Create a `.env` file with the following variables:
   ```
   PORT=5000
   NODE_ENV=development
   MONGODB_URI=mongodb://localhost:27017/auth-payment-db
   JWT_SECRET=your-super-secret-jwt-key
   JWT_EXPIRE=7d
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
   STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
   CLIENT_URL=http://localhost:3000
   ```

4. Start the server:
   ```bash
   npm start
   # or for development
   npm run dev
   ```

## API Endpoints

### Authentication

#### POST /api/auth/signup
Register a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "Password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "isEmailVerified": false
  }
}
```

#### POST /api/auth/signin
Login an existing user.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "Password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "isEmailVerified": false
  }
}
```

#### GET /api/auth/profile
Get user profile (requires authentication).

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": "user_id",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "isEmailVerified": false,
    "stripeCustomerId": "cus_stripe_id",
    "createdAt": "2023-01-01T00:00:00.000Z",
    "updatedAt": "2023-01-01T00:00:00.000Z"
  }
}
```

#### PUT /api/auth/profile
Update user profile (requires authentication).

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "name": "John Smith",
  "email": "johnsmith@example.com"
}
```

### Payments

#### POST /api/payments/create-intent
Create a payment intent (requires authentication).

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "amount": 2000,
  "currency": "usd",
  "description": "Test payment",
  "metadata": {
    "order_id": "12345"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Payment intent created successfully",
  "clientSecret": "pi_client_secret_here",
  "paymentIntentId": "pi_stripe_id",
  "payment": {
    "id": "payment_id",
    "amount": 2000,
    "currency": "usd",
    "status": "pending",
    "description": "Test payment"
  }
}
```

#### POST /api/payments/confirm
Confirm a payment (requires authentication).

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "paymentIntentId": "pi_stripe_id"
}
```

#### GET /api/payments/history
Get payment history (requires authentication).

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)

**Response:**
```json
{
  "success": true,
  "payments": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "pages": 3
  }
}
```

#### POST /api/payments/webhook
Stripe webhook endpoint for payment events.

### Health Check

#### GET /health
Check server status.

**Response:**
```json
{
  "status": "OK",
  "message": "Server is running",
  "timestamp": "2023-01-01T00:00:00.000Z"
}
```

## Database Models

### User Model
- `name`: String (required)
- `email`: String (required, unique)
- `password`: String (required, hashed)
- `role`: String (enum: 'user', 'admin')
- `isEmailVerified`: Boolean
- `stripeCustomerId`: String
- `resetPasswordToken`: String
- `resetPasswordExpire`: Date
- `emailVerificationToken`: String
- `emailVerificationExpire`: Date

### Payment Model
- `user`: ObjectId (ref: User)
- `stripePaymentIntentId`: String (required, unique)
- `amount`: Number (required)
- `currency`: String (required)
- `status`: String (enum: 'pending', 'succeeded', 'failed', 'canceled', 'refunded')
- `description`: String
- `metadata`: Map
- `refundAmount`: Number
- `refundReason`: String
- `paymentMethod`: String
- `receiptEmail`: String
- `receiptUrl`: String
- `failureReason`: String
- `processedAt`: Date
- `refundedAt`: Date

## Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "message": "Error description",
  "errors": [...] // For validation errors
}
```

## Security Considerations

1. **Environment Variables**: Store sensitive data in environment variables
2. **Rate Limiting**: Implemented to prevent abuse
3. **CORS**: Configured for specific origins
4. **Helmet**: Security headers added
5. **Input Validation**: All inputs are validated and sanitized
6. **Password Hashing**: Passwords are hashed using bcrypt
7. **JWT Tokens**: Secure token-based authentication

## Development

For development, you can use:
```bash
npm run dev
```

This will start the server with nodemon for automatic restarts on file changes.

## Testing

You can test the API endpoints using tools like:
- Postman
- curl
- Thunder Client (VS Code extension)

Example curl commands:

```bash
# Register a user
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"Password123"}'

# Login
curl -X POST http://localhost:5000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"Password123"}'

# Create payment intent
curl -X POST http://localhost:5000/api/payments/create-intent \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"amount":2000,"description":"Test payment"}'
```

## License

MIT License
