import { create } from 'zustand';
import { chatAPI } from '../api/chat';

export const useChatStore = create((set, get) => ({
  // State
  messages: [],
  conversations: [],
  currentConversationId: null,
  currentUser: null,
  isLoading: false,
  error: null,

  // Actions
  setCurrentUser: (user) => set({ currentUser: user }),

  setMessages: (messages) => set({ messages }),

  addMessage: (message) => set((state) => ({
    messages: [...state.messages, message]
  })),

  setLoading: (isLoading) => set({ isLoading }),

  setError: (error) => set({ error }),

  clearError: () => set({ error: null }),

  // Send message to AI
  sendMessage: async (content) => {
    const { currentUser, currentConversationId, addMessage, setLoading, setError } = get();
    
    if (!currentUser) {
      setError('Please set up your user account first');
      return;
    }

    setLoading(true);
    setError(null);

    // Add user message immediately
    const userMessage = {
      id: Date.now(),
      content,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    addMessage(userMessage);

    try {
      const response = await chatAPI.sendMessage({
        user_id: currentUser.id.toString(),
        message: content,
        conversation_id: currentConversationId
      });

      // Update conversation ID if new
      if (response.conversation_id !== currentConversationId) {
        set({ currentConversationId: response.conversation_id });
      }

      // Add AI response
      const aiMessage = {
        id: response.ai_response.id,
        content: response.ai_response.content,
        sender: 'ai',
        timestamp: response.ai_response.timestamp
      };
      addMessage(aiMessage);

      // Update conversations list
      get().loadConversations();

    } catch (error) {
      console.error('Failed to send message:', error);
      setError('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  },

  // Load conversation history
  loadConversation: async (conversationId) => {
    const { setLoading, setError, setMessages } = get();
    
    setLoading(true);
    setError(null);

    try {
      const messages = await chatAPI.getConversationMessages(conversationId);
      setMessages(messages);
      set({ currentConversationId: conversationId });
    } catch (error) {
      console.error('Failed to load conversation:', error);
      setError('Failed to load conversation');
    } finally {
      setLoading(false);
    }
  },

  // Load conversations list
  loadConversations: async () => {
    const { currentUser } = get();
    if (!currentUser) return;

    try {
      const conversations = await chatAPI.getUserConversations(currentUser.id);
      set({ conversations });
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  },

  // Start new conversation
  startNewConversation: () => {
    set({
      messages: [],
      currentConversationId: null
    });
  },

  // Clear all data (logout)
  clearAll: () => {
    set({
      messages: [],
      conversations: [],
      currentConversationId: null,
      currentUser: null,
      isLoading: false,
      error: null
    });
  }
}));