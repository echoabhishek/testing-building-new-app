const fs = require('fs');
const path = require('path');

class SimpleDB {
  constructor() {
    this.dbPath = path.join(__dirname, '../data');
    this.usersFile = path.join(this.dbPath, 'users.json');
    this.init();
  }

  init() {
    // Create data directory if it doesn't exist
    if (!fs.existsSync(this.dbPath)) {
      fs.mkdirSync(this.dbPath, { recursive: true });
    }

    // Create users file if it doesn't exist
    if (!fs.existsSync(this.usersFile)) {
      fs.writeFileSync(this.usersFile, JSON.stringify([]));
    }
  }

  getUsers() {
    try {
      const data = fs.readFileSync(this.usersFile, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      console.error('Error reading users file:', error);
      return [];
    }
  }

  saveUsers(users) {
    try {
      fs.writeFileSync(this.usersFile, JSON.stringify(users, null, 2));
      return true;
    } catch (error) {
      console.error('Error saving users file:', error);
      return false;
    }
  }

  findUserByEmail(email) {
    const users = this.getUsers();
    return users.find(user => user.email.toLowerCase() === email.toLowerCase());
  }

  findUserById(id) {
    const users = this.getUsers();
    return users.find(user => user._id === id);
  }

  createUser(userData) {
    const users = this.getUsers();
    const newUser = {
      _id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
      ...userData,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    users.push(newUser);
    
    if (this.saveUsers(users)) {
      return newUser;
    }
    
    throw new Error('Failed to save user');
  }

  updateUser(id, updateData) {
    const users = this.getUsers();
    const userIndex = users.findIndex(user => user._id === id);
    
    if (userIndex === -1) {
      throw new Error('User not found');
    }
    
    users[userIndex] = {
      ...users[userIndex],
      ...updateData,
      updatedAt: new Date().toISOString()
    };
    
    if (this.saveUsers(users)) {
      return users[userIndex];
    }
    
    throw new Error('Failed to update user');
  }
}

module.exports = new SimpleDB();
