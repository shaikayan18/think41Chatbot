from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, create_tables, Base, engine
from models import User, ConversationSession, Message
from schemas import UserCreate, User as UserSchema
from routes.chat import router as chat_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Conversational AI Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "Conversational AI Backend is running!"}

@app.post("/api/users", response_model=UserSchema)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)