// Load environment variables FIRST
require("dotenv").config();

const express = require("express");
const cors = require("cors");
const auth = require("./config/auth"); // Now this will have access to env vars

const app = express();

app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));

app.use(express.json());
app.use(auth);

// Public routes
const publicRoutes = require("./routes/public.routes");
app.use("/", publicRoutes);

// Protected routes
const privateRoutes = require("./routes/private.routes");
app.use("/api", privateRoutes);

module.exports = app;