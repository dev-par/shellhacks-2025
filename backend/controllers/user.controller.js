const User = require("../models/user.model");
const jwt = require("jsonwebtoken");

exports.register = async (req, res) => {
  try {
    const { name, staffId, role, department, employmentStatus } = req.body;

    const user = await User.create({ name, staffId, role, department, employmentStatus });
    res.status(201).json({ message: "User registered", userId: user._id });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
};

exports.login = async (req, res) => {
  try {
    const { name, staffId } = req.body;
    const user = await User.findOne({ staffId });

    if (!user) return res.status(404).json({ error: "User not found" });

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: "1h" });
    res.json({ message: "Login successful", token });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

exports.getProfile = async (req, res) => {
  try {
    // In real apps you'd decode JWT here
    const user = await User.findById(req.user.id).select("-staffId");
    res.json(user);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
