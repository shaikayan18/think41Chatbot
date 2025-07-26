const API_BASE_URL = 'http://localhost:8000';

export const chatAPI = {
  // Send message to AI
  sendMessage: async (data) => {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to send message');
    }

    return response.json();
  },

  // Create new user
  createUser: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/api/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create user');
    }

    return response.json();
  },

  // Get user conversations (now real API call)
  getUserConversations: async (userId) => {
    const response = await fetch(`${API_BASE_URL}/api/users/${userId}/conversations`);
    if (!response.ok) throw new Error('Failed to fetch conversations');
    return response.json();
  },

  // Get conversation messages (now real API call)
  getConversationMessages: async (conversationId) => {
    const response = await fetch(`${API_BASE_URL}/api/conversations/${conversationId}/messages`);
    if (!response.ok) throw new Error('Failed to fetch messages');
    return response.json();
  },

  // Delete conversation
  deleteConversation: async (conversationId) => {
    const response = await fetch(`${API_BASE_URL}/api/conversations/${conversationId}`, {
      method: 'DELETE'
    });
    if (!response.ok) throw new Error('Failed to delete conversation');
    return response.json();
  }
};
