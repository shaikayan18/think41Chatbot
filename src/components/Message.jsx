import React from 'react';
import './Message.css';

const Message = ({ message }) => {
  const isUser = message.sender === 'user';
  const timestamp = new Date(message.timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });

  return (
    <div className={`message ${isUser ? 'user' : 'ai'}`}>
      <div className="message-wrapper">
        <div className={`avatar ${isUser ? 'user-avatar' : 'ai-avatar'}`}>
          {isUser ? '👤' : '🤖'}
        </div>
        <div className="message-content">
          <div className="message-text">
            {message.content}
          </div>
          <div className="message-time">
            {timestamp}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Message;