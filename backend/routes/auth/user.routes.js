const express = require("express");
const router = express.Router();
const UserController = require("../../controllers/user.controller.js");

// Register new user
router.post("/register", UserController.register);

// Login
router.post("/login", UserController.login);

// Get profile
router.get("/me", UserController.getProfile);

module.exports = router;
