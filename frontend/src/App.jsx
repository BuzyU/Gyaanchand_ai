import { useState } from 'react'
import './App.css'

// Get the API URL based on environment
const API_URL = import.meta.env.PROD 
  ? '/api' 
  : 'http://localhost:5000/api';

function App() {
  const [messages, setMessages] = useState([
    { type: 'system', text: "Hello! I'm Gyaanchand. How can I help you today?" }
  ]);
  const [input, setInput] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    setMessages(prev => [...prev, { type: 'user', text: input }]);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();

      if (data.status === 'success') {
        setMessages(prev => [...prev, { type: 'assistant', text: data.response }]);
      } else {
        setMessages(prev => [...prev, { type: 'system', text: 'Sorry, I encountered an error.' }]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { type: 'system', text: 'Sorry, I encountered an error.' }]);
    }

    setInput('');
  };

  return (
    <div className="container">
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.type}`}>
              {msg.text}
            </div>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="form-control"
          />
          <button type="submit" className="btn btn-primary">Send</button>
        </form>
      </div>
    </div>
  )
}

export default App