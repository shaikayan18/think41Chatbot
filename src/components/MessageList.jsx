import React, { useEffect, useRef } from 'react';
import Message from './Message';
import { useChatStore } from '../store/chatState';
import './MessageList.css';

const MessageList = () => {
  const { messages, isLoading } = useChatStore();
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="welcome-message">
          <div className="welcome-content">
            <h3>👋 Welcome!</h3>
            <p>Start a conversation by typing a message below.</p>
            <div className="suggestions">
              <span>Try asking about:</span>
              <div className="suggestion-chips">
                <span className="chip">Products</span>
                <span className="chip">Orders</span>
                <span className="chip">Help</span>
              </div>
            </div>
          </div>
        </div>
      ) : (
        messages.map((message) => (
          <Message key={message.id} message={message} />
        ))
      )}
      
      {isLoading && (
        <div className="typing-indicator">
          <div className="typing-content">
            <div className="avatar ai-avatar">🤖</div>
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;