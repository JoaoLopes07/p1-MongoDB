const User = require('../models/User');

class UserRepository {
  static async findByEmail(email) {
    return await User.findOne({ email });
  }

  static async create(usuarioData) {
    const user = new User(userData);
    return await user.save();
  }
}

module.exports = new UserRepository();