const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 5002;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/docs', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    message: 'Documentation server is running',
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`📚 Documentation server running at http://localhost:${PORT}`);
  console.log(`🌐 Access docs at: http://localhost:${PORT}/docs`);
}); 