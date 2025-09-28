const express = require("express");
const router = express.Router();

// Home route
router.get("/", (req, res) => {
  console.log("Hit / route, authenticated:", req.oidc.isAuthenticated());
  res.send(req.oidc.isAuthenticated() ? "Logged in" : "Logged out");
});

// LOGIN ROUTE - Add console.log for debugging
router.get("/login", (req, res) => {
  console.log("Hit /login route, authenticated:", req.oidc.isAuthenticated());
  
  if (req.oidc.isAuthenticated()) {
    console.log("User already authenticated, redirecting to modules");
    return res.redirect('http://localhost:3000/modules');
  }
  
  console.log("User not authenticated, triggering Auth0 login");
  res.oidc.login({
    returnTo: 'http://localhost:3000/modules'
  });
});

router.get("/info", (req, res) => {
  res.send("This is a public endpoint anyone can hit.");
});

module.exports = router;