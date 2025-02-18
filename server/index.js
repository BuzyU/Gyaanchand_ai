const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Simple in-memory storage for chat history
const chatHistory = [];

// Basic template-based response generation
function generateResponse(message) {
    message = message.toLowerCase();
    if (message.includes('hello') || message.includes('hi')) {
        return "Hello! How can I help you today?";
    } else if (message.includes('code') || message.includes('generate')) {
        return "I can help you generate code. Please specify what kind of code you need.";
    } else if (message.includes('help')) {
        return "I can help you with code generation and answer questions. What would you like to know?";
    }
    return "I understand you want to discuss something. Could you please be more specific?";
}

// Chat endpoint
app.post('/api/chat', (req, res) => {
    try {
        const { message } = req.body;
        const response = generateResponse(message);

        chatHistory.push({ message, response });

        res.json({
            status: 'success',
            response
        });
    } catch (error) {
        console.error('Error processing chat:', error);
        res.status(500).json({
            status: 'error',
            message: 'An error occurred processing your request'
        });
    }
});

// Code generation endpoint
app.post('/api/generate-code', (req, res) => {
    try {
        const { prompt } = req.body;
        let code = '// Generated code\n';

        if (prompt.toLowerCase().includes('website')) {
            code = `
<!DOCTYPE html>
<html>
<head>
    <title>Generated Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1>Hello World</h1>
    </div>
</body>
</html>`;
        } else {
            code = `console.log("Hello World!");`;
        }

        res.json({
            status: 'success',
            code
        });
    } catch (error) {
        console.error('Error generating code:', error);
        res.status(500).json({
            status: 'error',
            message: 'An error occurred generating code'
        });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        status: 'error',
        message: 'Something broke!'
    });
});

// Start server
app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on port ${port}`);
}).on('error', (err) => {
    console.error('Failed to start server:', err.message);
    process.exit(1);
});