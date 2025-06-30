const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const { validationResult } = require('express-validator');
const User = require('../models/UserSimple');

// Create payment intent
const createPaymentIntent = async (req, res) => {
  try {
    // Check for validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }

    const { amount, currency = 'usd', description } = req.body;
    const user = req.user;

    // Ensure user has a Stripe customer ID
    let customerId = user.stripeCustomerId;
    if (!customerId) {
      const customer = await stripe.customers.create({
        email: user.email,
        name: `${user.firstName} ${user.lastName}`,
        metadata: {
          userId: user._id.toString()
        }
      });
      
      customerId = customer.id;
      
      // Update user with Stripe customer ID
      user.stripeCustomerId = customerId;
      await user.save();
    }

    // Create payment intent
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount * 100), // Convert to cents
      currency,
      customer: customerId,
      description: description || 'Payment',
      metadata: {
        userId: user._id.toString()
      }
    });

    res.status(200).json({
      success: true,
      message: 'Payment intent created successfully',
      data: {
        clientSecret: paymentIntent.client_secret,
        paymentIntentId: paymentIntent.id,
        amount: paymentIntent.amount / 100,
        currency: paymentIntent.currency
      }
    });
  } catch (error) {
    console.error('Create payment intent error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to create payment intent',
      error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
};

// Confirm payment
const confirmPayment = async (req, res) => {
  try {
    const { paymentIntentId } = req.body;
    const user = req.user;

    // Retrieve payment intent from Stripe
    const paymentIntent = await stripe.paymentIntents.retrieve(paymentIntentId);

    if (paymentIntent.status === 'succeeded') {
      // Add to user's payment history
      const paymentRecord = {
        paymentIntentId: paymentIntent.id,
        amount: paymentIntent.amount / 100,
        currency: paymentIntent.currency,
        status: paymentIntent.status,
        description: paymentIntent.description,
        createdAt: new Date()
      };

      user.paymentHistory.push(paymentRecord);
      await user.save();

      res.status(200).json({
        success: true,
        message: 'Payment confirmed successfully',
        data: {
          paymentIntent: {
            id: paymentIntent.id,
            amount: paymentIntent.amount / 100,
            currency: paymentIntent.currency,
            status: paymentIntent.status
          }
        }
      });
    } else {
      res.status(400).json({
        success: false,
        message: 'Payment not completed',
        data: {
          status: paymentIntent.status
        }
      });
    }
  } catch (error) {
    console.error('Confirm payment error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to confirm payment',
      error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
};

// Get payment history
const getPaymentHistory = async (req, res) => {
  try {
    const user = req.user;
    const { page = 1, limit = 10 } = req.query;

    // Get payment history from user object
    const paymentHistory = user.paymentHistory || [];
    const totalPayments = paymentHistory.length;
    const totalPages = Math.ceil(totalPayments / limit);
    
    // Paginate results
    const startIndex = (page - 1) * limit;
    const endIndex = startIndex + parseInt(limit);
    const paginatedPayments = paymentHistory.slice(startIndex, endIndex);

    res.status(200).json({
      success: true,
      message: 'Payment history retrieved successfully',
      data: {
        payments: paginatedPayments,
        pagination: {
          currentPage: parseInt(page),
          totalPages,
          totalPayments,
          hasNextPage: page < totalPages,
          hasPrevPage: page > 1
        }
      }
    });
  } catch (error) {
    console.error('Get payment history error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve payment history',
      error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
};

// Create subscription
const createSubscription = async (req, res) => {
  try {
    const { priceId } = req.body;
    const user = req.user;

    // Ensure user has a Stripe customer ID
    let customerId = user.stripeCustomerId;
    if (!customerId) {
      const customer = await stripe.customers.create({
        email: user.email,
        name: `${user.firstName} ${user.lastName}`,
        metadata: {
          userId: user._id.toString()
        }
      });
      
      customerId = customer.id;
      
      // Update user with Stripe customer ID
      user.stripeCustomerId = customerId;
      await user.save();
    }

    // Create subscription
    const subscription = await stripe.subscriptions.create({
      customer: customerId,
      items: [{ price: priceId }],
      payment_behavior: 'default_incomplete',
      expand: ['latest_invoice.payment_intent'],
      metadata: {
        userId: user._id.toString()
      }
    });

    res.status(200).json({
      success: true,
      message: 'Subscription created successfully',
      data: {
        subscriptionId: subscription.id,
        clientSecret: subscription.latest_invoice.payment_intent.client_secret,
        status: subscription.status
      }
    });
  } catch (error) {
    console.error('Create subscription error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to create subscription',
      error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
};

// Cancel subscription
const cancelSubscription = async (req, res) => {
  try {
    const user = req.user;
    const subscriptionId = user.subscription.subscriptionId;

    if (!subscriptionId) {
      return res.status(400).json({
        success: false,
        message: 'No active subscription found'
      });
    }

    // Cancel subscription in Stripe
    const subscription = await stripe.subscriptions.update(subscriptionId, {
      cancel_at_period_end: true
    });

    // Update user subscription status
    user.subscription.status = 'cancelled';
    await user.save();

    res.status(200).json({
      success: true,
      message: 'Subscription cancelled successfully',
      data: {
        subscription: {
          id: subscription.id,
          status: subscription.status,
          cancelAtPeriodEnd: subscription.cancel_at_period_end,
          currentPeriodEnd: new Date(subscription.current_period_end * 1000)
        }
      }
    });
  } catch (error) {
    console.error('Cancel subscription error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to cancel subscription',
      error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
};

// Stripe webhook handler
const handleWebhook = async (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  try {
    // Handle the event
    switch (event.type) {
      case 'payment_intent.succeeded':
        const paymentIntent = event.data.object;
        console.log('Payment succeeded:', paymentIntent.id);
        break;

      case 'customer.subscription.created':
      case 'customer.subscription.updated':
        const subscription = event.data.object;
        const userId = subscription.metadata.userId;
        
        if (userId) {
          const user = User.findById(userId);
          if (user) {
            user.subscription.status = subscription.status;
            user.subscription.subscriptionId = subscription.id;
            user.subscription.planId = subscription.items.data[0].price.id;
            user.subscription.currentPeriodStart = new Date(subscription.current_period_start * 1000);
            user.subscription.currentPeriodEnd = new Date(subscription.current_period_end * 1000);
            await user.save();
          }
        }
        break;

      case 'customer.subscription.deleted':
        const deletedSubscription = event.data.object;
        const userIdDeleted = deletedSubscription.metadata.userId;
        
        if (userIdDeleted) {
          const user = User.findById(userIdDeleted);
          if (user) {
            user.subscription.status = 'cancelled';
            user.subscription.subscriptionId = null;
            user.subscription.planId = null;
            user.subscription.currentPeriodStart = null;
            user.subscription.currentPeriodEnd = null;
            await user.save();
          }
        }
        break;

      case 'invoice.payment_failed':
        const failedInvoice = event.data.object;
        const userIdFailed = failedInvoice.subscription_details?.metadata?.userId;
        
        if (userIdFailed) {
          const user = User.findById(userIdFailed);
          if (user) {
            user.subscription.status = 'past_due';
            await user.save();
          }
        }
        break;

      default:
        console.log(`Unhandled event type ${event.type}`);
    }

    res.json({ received: true });
  } catch (error) {
    console.error('Webhook handler error:', error);
    res.status(500).json({ error: 'Webhook handler failed' });
  }
};

module.exports = {
  createPaymentIntent,
  confirmPayment,
  getPaymentHistory,
  createSubscription,
  cancelSubscription,
  handleWebhook
};
