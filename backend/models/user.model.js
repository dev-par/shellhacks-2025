const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({

  name: { type: String, required: true },
  staffId: { type: Number, required: true, unique: true },
  role: { type: String, required: true },
  department: { type: String, required: true },
  employmentStatus: { type: String, required: true }

}, { timestamps: true });

module.exports = mongoose.model("User", userSchema);
