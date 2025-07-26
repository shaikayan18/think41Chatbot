from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, ConversationSession, Message
from schemas import ChatRequest, ChatResponse
from services.llm import get_ai_response
from datetime import datetime

router = APIRouter()

@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Get or create user
        user = db.query(User).filter(User.id == int(request.user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get or create conversation
        if request.conversation_id:
            conversation = db.query(ConversationSession).filter(
                ConversationSession.id == int(request.conversation_id)
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = ConversationSession(user_id=user.id)
            db.add(conversation)
            db.flush()
        
        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            sender="user",
            content=request.message,
            timestamp=datetime.utcnow()
        )
        db.add(user_message)
        
        # Get AI response
        ai_response_content = await get_ai_response(request.message, conversation.id, db)
        
        # Save AI message
        ai_message = Message(
            conversation_id=conversation.id,
            sender="ai",
            content=ai_response_content,
            timestamp=datetime.utcnow()
        )
        db.add(ai_message)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        
        db.commit()
        
        return ChatResponse(
            conversation_id=str(conversation.id),
            user_message=user_message,
            ai_response=ai_message
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))