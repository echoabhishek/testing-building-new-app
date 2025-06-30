# Authentication & Payment Server

A complete Node.js/Express server with user authentication and Stripe payment integration.

## Features

### Authentication
- User registration with email validation
- Secure login with JWT tokens
- Password hashing with bcrypt
- Profile management
- Password change functionality
- Token-based authentication middleware

### Payment Processing
- Stripe payment integration
- One-time payments with Payment Intents
- Subscription management
- Payment history tracking
- Webhook handling for real-time updates
- Customer management

### Security
- Rate limiting
- CORS protection
- Helmet security headers
- Input validation
- Password strength requirements

## API Endpoints

### Authentication Routes (`/api/auth`)

#### POST `/api/auth/register`
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "firstName": "John",
  "lastName": "Doe"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": { ... },
    "token": "jwt_token_here"
  }
}
```

#### POST `/api/auth/login`
Login with existing credentials.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

#### GET `/api/auth/profile`
Get current user profile (requires authentication).

**Headers:**
```
Authorization: Bearer <jwt_token>
```

#### PUT `/api/auth/profile`
Update user profile (requires authentication).

#### PUT `/api/auth/change-password`
Change user password (requires authentication).

#### GET `/api/auth/verify`
Verify JWT token validity.

### Payment Routes (`/api/payment`)

#### POST `/api/payment/create-payment-intent`
Create a new payment intent for one-time payments.

**Request Body:**
```json
{
  "amount": 29.99,
  "currency": "usd",
  "description": "Product purchase"
}
```

#### POST `/api/payment/confirm-payment`
Confirm a completed payment.

**Request Body:**
```json
{
  "paymentIntentId": "pi_1234567890"
}
```

#### GET `/api/payment/history`
Get user's payment history (supports pagination).

#### POST `/api/payment/create-subscription`
Create a new subscription.

**Request Body:**
```json
{
  "priceId": "price_1234567890"
}
```

#### POST `/api/payment/cancel-subscription`
Cancel current subscription.

#### GET `/api/payment/subscription`
Get current subscription status.

#### POST `/api/payment/webhook`
Stripe webhook endpoint for real-time updates.

## Setup Instructions

### 1. Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required environment variables:
- `MONGODB_URI`: MongoDB connection string
- `JWT_SECRET`: Secret key for JWT tokens
- `STRIPE_SECRET_KEY`: Stripe secret key
- `STRIPE_PUBLISHABLE_KEY`: Stripe publishable key
- `STRIPE_WEBHOOK_SECRET`: Stripe webhook secret

### 2. Database Setup
Ensure MongoDB is running and accessible via the connection string in your `.env` file.

### 3. Stripe Setup
1. Create a Stripe account at https://stripe.com
2. Get your API keys from the Stripe dashboard
3. Set up webhook endpoints for real-time payment updates
4. Configure webhook secret in your environment variables

### 4. Install Dependencies
```bash
npm install
```

### 5. Start the Server
```bash
# Development mode
npm run dev

# Production mode
npm start
```

The server will start on the port specified in your `.env` file (default: 3000).

## Testing the API

### Health Check
```bash
curl http://localhost:3000/health
```

### Register a User
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123",
    "firstName": "Test",
    "lastName": "User"
  }'
```

### Login
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

### Create Payment Intent
```bash
curl -X POST http://localhost:3000/api/payment/create-payment-intent \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -d '{
    "amount": 29.99,
    "currency": "usd",
    "description": "Test payment"
  }'
```

## Project Structure

```
├── controllers/
│   ├── authController.js      # Authentication logic
│   └── paymentController.js   # Payment processing logic
├── middleware/
│   └── auth.js               # Authentication middleware
├── models/
│   └── User.js               # User data model
├── routes/
│   ├── auth.js               # Authentication routes
│   └── payment.js            # Payment routes
├── .env.example              # Environment variables template
├── .env                      # Environment variables (create this)
├── package.json              # Project dependencies
├── server.js                 # Main server file
└── README.md                 # This file
```

## Security Considerations

1. **Environment Variables**: Never commit `.env` files to version control
2. **JWT Secret**: Use a strong, random secret key for JWT tokens
3. **Password Requirements**: Enforced strong password requirements
4. **Rate Limiting**: Implemented to prevent abuse
5. **Input Validation**: All inputs are validated and sanitized
6. **HTTPS**: Use HTTPS in production environments
7. **Database Security**: Secure your MongoDB instance

## Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "message": "Error description",
  "errors": [...] // Validation errors if applicable
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
