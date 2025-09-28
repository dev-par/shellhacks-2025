const express = require("express");
const ensureDbUser = require("../middleware/auth.middleware.js");
const { requiresAuth } = require("express-openid-connect");

const router = express.Router();

router.use(requiresAuth());

router.get("/profile", ensureDbUser, (req, res) => {
  res.json({
    user: req.user,
    auth0User: req.oidc.user
  });
});

router.get("/modules", ensureDbUser, (req, res) => {
  res.json({ 
    msg: "Only logged-in users see this.",
    user: req.user 
  });
});

module.exports = router;