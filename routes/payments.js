const express = require('express');
const { body } = require('express-validator');
const { auth } = require('../middleware/auth');
const {
  createPaymentIntent,
  confirmPayment,
  getPaymentHistory,
  handleWebhook
} = require('../controllers/paymentController');

const router = express.Router();

// Validation rules
const createPaymentValidation = [
  body('amount')
    .isNumeric()
    .isFloat({ min: 0.50 })
    .withMessage('Amount must be at least $0.50'),
  body('currency')
    .optional()
    .isLength({ min: 3, max: 3 })
    .withMessage('Currency must be a 3-letter code'),
  body('description')
    .optional()
    .trim()
    .isLength({ max: 200 })
    .withMessage('Description cannot exceed 200 characters')
];

const confirmPaymentValidation = [
  body('paymentIntentId')
    .notEmpty()
    .withMessage('Payment intent ID is required')
];

// Routes
router.post('/create-intent', auth, createPaymentValidation, createPaymentIntent);
router.post('/confirm', auth, confirmPaymentValidation, confirmPayment);
router.get('/history', auth, getPaymentHistory);

// Webhook endpoint (no auth middleware as it's verified by Stripe)
router.post('/webhook', express.raw({ type: 'application/json' }), handleWebhook);

module.exports = router;
