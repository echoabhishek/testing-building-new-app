const bcrypt = require('bcryptjs');
const simpleDB = require('../config/simpleDB');

class User {
  constructor(userData) {
    this._id = userData._id;
    this.email = userData.email;
    this.password = userData.password;
    this.firstName = userData.firstName;
    this.lastName = userData.lastName;
    this.isEmailVerified = userData.isEmailVerified || false;
    this.emailVerificationToken = userData.emailVerificationToken || null;
    this.resetPasswordToken = userData.resetPasswordToken || null;
    this.resetPasswordExpires = userData.resetPasswordExpires || null;
    this.stripeCustomerId = userData.stripeCustomerId || null;
    this.subscription = userData.subscription || {
      status: 'inactive',
      subscriptionId: null,
      planId: null,
      currentPeriodStart: null,
      currentPeriodEnd: null
    };
    this.paymentHistory = userData.paymentHistory || [];
    this.role = userData.role || 'user';
    this.isActive = userData.isActive !== undefined ? userData.isActive : true;
    this.lastLogin = userData.lastLogin || null;
    this.createdAt = userData.createdAt;
    this.updatedAt = userData.updatedAt;
  }

  // Hash password before saving
  static async hashPassword(password) {
    return bcrypt.hash(password, 12);
  }

  // Instance method to check password
  async comparePassword(candidatePassword) {
    return bcrypt.compare(candidatePassword, this.password);
  }

  // Instance method to get public profile
  getPublicProfile() {
    const userObject = { ...this };
    delete userObject.password;
    delete userObject.emailVerificationToken;
    delete userObject.resetPasswordToken;
    delete userObject.resetPasswordExpires;
    return userObject;
  }

  // Save user to database
  async save() {
    if (this._id) {
      // Update existing user
      const updatedUser = simpleDB.updateUser(this._id, this);
      Object.assign(this, updatedUser);
      return this;
    } else {
      // Create new user
      if (this.password && !this.password.startsWith('$2a$')) {
        this.password = await User.hashPassword(this.password);
      }
      
      const newUser = simpleDB.createUser(this);
      Object.assign(this, newUser);
      return this;
    }
  }

  // Static method to find user by email
  static findByEmail(email) {
    const userData = simpleDB.findUserByEmail(email);
    return userData ? new User(userData) : null;
  }

  // Static method to find user by ID
  static findById(id) {
    const userData = simpleDB.findUserById(id);
    return userData ? new User(userData) : null;
  }

  // Static method to find user by ID and update
  static findByIdAndUpdate(id, updateData, options = {}) {
    try {
      const updatedUserData = simpleDB.updateUser(id, updateData);
      return new User(updatedUserData);
    } catch (error) {
      if (options.new) {
        throw error;
      }
      return null;
    }
  }
}

module.exports = User;
