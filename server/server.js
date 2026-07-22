const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/merndb';

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose
  .connect(MONGO_URI)
  .then(() => console.log('✅ Connected to MongoDB successfully'))
  .catch((err) => {
    console.warn('⚠️  MongoDB connection error:', err.message);
    console.warn('   Ensure MongoDB is running locally or update MONGO_URI in server/.env');
  });

// Routes
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    message: '🚀 MERN Backend Server is running smoothly!',
    timestamp: new Date().toISOString(),
    dbState: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected'
  });
});

app.get('/api/test', (req, res) => {
  res.json({
    items: [
      { id: 1, name: 'MongoDB', role: 'Database' },
      { id: 2, name: 'Express', role: 'Backend Framework' },
      { id: 3, name: 'React', role: 'Frontend UI' },
      { id: 4, name: 'Node.js', role: 'Runtime Environment' }
    ]
  });
});

// Start Server
app.listen(PORT, () => {
  console.log(`📡 Server listening on http://localhost:${PORT}`);
});
