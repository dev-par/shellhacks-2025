const User = require("../models/user.model.js");

module.exports = async function ensureDbUser(req, res, next) {
  try {
    // Check if user is authenticated via Auth0
    if (!req.oidc.isAuthenticated()) {
      return res.status(401).json({ error: "Not authenticated" });
    }

    const { sub, email, name, picture } = req.oidc.user;

    // Find or create user in your database
    let user = await User.findOne({ auth0Id: sub });

    if (!user) {
      user = await User.create({
        auth0Id: sub,
        email,
        name,
        picture,
        createdAt: new Date(),
      });
      console.log(`New user created: ${email}`);
    } else {
      // Optionally update user info if it changed
      await User.findByIdAndUpdate(user._id, {
        email,
        name,
        picture,
        lastLogin: new Date(),
      });
    }

    req.user = user;
    next();
  } catch (error) {
    console.error("Error in ensureDbUser middleware:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
};
