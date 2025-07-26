import React, { useState } from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import HistoryPanel from './HistoryPanel';
import { useChatStore } from '../store/chatState';
import './ChatWindow.css';

const ChatWindow = () => {
  const [showHistory, setShowHistory] = useState(false);
  const { currentUser, setCurrentUser } = useChatStore();
  const [userSetup, setUserSetup] = useState({ username: '', email: '' });
  const [showUserSetup, setShowUserSetup] = useState(!currentUser);

  const handleUserSetup = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userSetup)
      });

      if (response.ok) {
        const user = await response.json();
        setCurrentUser(user);
        setShowUserSetup(false);
      }
    } catch (error) {
      console.error('Failed to create user:', error);
    }
  };

  if (showUserSetup) {
    return (
      <div className="chat-container">
        <div className="user-setup">
          <h2>🤖 Welcome to AI Assistant</h2>
          <p>Please set up your account to start chatting</p>
          <form onSubmit={handleUserSetup}>
            <input
              type="text"
              placeholder="Enter your username"
              value={userSetup.username}
              onChange={(e) => setUserSetup({...userSetup, username: e.target.value})}
              required
            />
            <input
              type="email"
              placeholder="Enter your email"
              value={userSetup.email}
              onChange={(e) => setUserSetup({...userSetup, email: e.target.value})}
              required
            />
            <button type="submit">Start Chatting</button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="header-left">
          <h1>🤖 AI Assistant</h1>
          <p>Your intelligent e-commerce companion</p>
        </div>
        <div className="header-right">
          <span className="user-info">User: {currentUser?.username}</span>
          <button 
            className="history-toggle"
            onClick={() => setShowHistory(!showHistory)}
          >
            {showHistory ? '✕' : '📋'}
          </button>
        </div>
      </div>

      <div className="chat-body">
        {showHistory && <HistoryPanel onClose={() => setShowHistory(false)} />}
        <div className="chat-main">
          <MessageList />
          <UserInput />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;