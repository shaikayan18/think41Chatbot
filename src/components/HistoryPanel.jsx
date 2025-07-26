import React, { useEffect, useState } from 'react';
import { useChatStore } from '../store/chatState';
import './HistoryPanel.css';

const HistoryPanel = ({ onClose }) => {
  const { 
    conversations, 
    currentConversationId, 
    loadConversations, 
    loadConversation, 
    startNewConversation 
  } = useChatStore();

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  const handleConversationClick = (conversationId) => {
    if (conversationId !== currentConversationId) {
      loadConversation(conversationId);
    }
    onClose();
  };

  const handleNewConversation = () => {
    startNewConversation();
    onClose();
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return 'Today';
    if (diffDays === 2) return 'Yesterday';
    if (diffDays <= 7) return `${diffDays - 1} days ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="history-panel">
      <div className="history-header">
        <h3>💬 Conversations</h3>
        <button className="close-button" onClick={onClose}>
          ✕
        </button>
      </div>

      <div className="history-actions">
        <button 
          className="new-conversation-btn"
          onClick={handleNewConversation}
        >
          ➕ New Conversation
        </button>
      </div>

      <div className="conversations-list">
        {conversations.length === 0 ? (
          <div className="empty-state">
            <p>No conversations yet</p>
            <span>Start chatting to see your conversation history</span>
          </div>
        ) : (
          conversations.map((conversation) => (
            <div
              key={conversation.id}
              className={`conversation-item ${
                conversation.id === currentConversationId ? 'active' : ''
              }`}
              onClick={() => handleConversationClick(conversation.id)}
            >
              <div className="conversation-info">
                <div className="conversation-title">
                  {conversation.title || `Conversation ${conversation.id}`}
                </div>
                <div className="conversation-meta">
                  <span className="message-count">
                    {conversation.message_count} messages
                  </span>
                  <span className="conversation-date">
                    {formatDate(conversation.updated_at)}
                  </span>
                </div>
              </div>
              <div className="conversation-indicator">
                {conversation.id === currentConversationId && (
                  <div className="active-indicator">●</div>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="history-footer">
        <div className="storage-info">
          <small>💾 {conversations.length} conversations stored</small>
        </div>
      </div>
    </div>
  );
};

export default HistoryPanel;