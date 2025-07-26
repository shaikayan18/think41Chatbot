from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    sender: str
    content: str

class MessageCreate(MessageBase):
    conversation_id: int

class Message(MessageBase):
    id: int
    conversation_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ConversationSessionBase(BaseModel):
    title: Optional[str] = "New Conversation"

class ConversationSessionCreate(ConversationSessionBase):
    user_id: int

class ConversationSession(ConversationSessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    conversation_id: str
    user_message: Message
    ai_response: Message