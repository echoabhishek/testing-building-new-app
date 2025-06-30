const express = require('express');
const { body } = require('express-validator');
const { authenticateToken } = require('../middleware/auth');
const {
  createPaymentIntent,
  confirmPayment,
  getPaymentHistory,
  createSubscription,
  cancelSubscription,
  handleWebhook
} = require('../controllers/paymentController');

const router = express.Router();

// Validation rules
const paymentIntentValidation = [
  body('amount')
    .isFloat({ min: 0.50 })
    .withMessage('Amount must be at least $0.50'),
  body('currency')
    .optional()
    .isIn(['usd', 'eur', 'gbp'])
    .withMessage('Currency must be usd, eur, or gbp'),
  body('description')
    .optional()
    .trim()
    .isLength({ max: 200 })
    .withMessage('Description must be less than 200 characters')
];

const confirmPaymentValidation = [
  body('paymentIntentId')
    .notEmpty()
    .withMessage('Payment intent ID is required')
];

const subscriptionValidation = [
  body('priceId')
    .notEmpty()
    .withMessage('Price ID is required')
];

// Payment routes
router.post('/create-payment-intent', 
  authenticateToken, 
  paymentIntentValidation, 
  createPaymentIntent
);

router.post('/confirm-payment', 
  authenticateToken, 
  confirmPaymentValidation, 
  confirmPayment
);

router.get('/history', 
  authenticateToken, 
  getPaymentHistory
);

// Subscription routes
router.post('/create-subscription', 
  authenticateToken, 
  subscriptionValidation, 
  createSubscription
);

router.post('/cancel-subscription', 
  authenticateToken, 
  cancelSubscription
);

// Webhook route (no authentication required)
router.post('/webhook', handleWebhook);

// Get subscription status
router.get('/subscription', authenticateToken, (req, res) => {
  try {
    const user = req.user;
    
    res.status(200).json({
      success: true,
      message: 'Subscription status retrieved successfully',
      data: {
        subscription: user.subscription
      }
    });
  } catch (error) {
    console.error('Get subscription error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve subscription status',
      error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
});

module.exports = router;
