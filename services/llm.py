import os
from groq import Groq
from sqlalchemy.orm import Session
from database import Product, Customer, Order
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Debug: Check if API key is loaded
api_key = os.getenv("GROQ_API_KEY")
print(f"Debug: API key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"Debug: API key starts with: {api_key[:10]}...")

# Initialize Groq client with error handling
try:
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    client = Groq(api_key=api_key)
    print("✅ Groq client initialized successfully")
except Exception as e:
    print(f"❌ Groq client initialization failed: {e}")
    client = None

async def get_ai_response(user_message: str, conversation_id: int, db: Session) -> str:
    try:
        if not client:
            return "I apologize, but the AI service is currently unavailable. Please check your API configuration."
        
        # Check if message is e-commerce related
        ecommerce_keywords = ["product", "order", "buy", "purchase", "price", "stock", "customer"]
        is_ecommerce_query = any(keyword in user_message.lower() for keyword in ecommerce_keywords)
        
        system_prompt = """You are a helpful AI assistant for an e-commerce platform. 
        You can help users with product information, orders, and general questions.
        If you need more information to provide a helpful answer, ask clarifying questions.
        Be concise and friendly in your responses."""
        
        context = ""
        if is_ecommerce_query:
            context = get_ecommerce_context(user_message, db)
            if context:
                system_prompt += f"\n\nHere's relevant information from our database:\n{context}"
        
        print(f"Debug: Sending request to Groq with message: {user_message[:50]}...")
        
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        print(f"Debug: Received response from Groq: {ai_response[:50]}...")
        return ai_response
        
    except Exception as e:
        print(f"Debug: Error in get_ai_response: {e}")
        return f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}"

def get_ecommerce_context(message: str, db: Session) -> str:
    """Get relevant e-commerce data based on user message"""
    context_parts = []
    
    # Search for products
    if any(word in message.lower() for word in ["product", "item", "buy", "price"]):
        products = db.query(Product).limit(5).all()
        if products:
            context_parts.append("Available products:")
            for product in products:
                context_parts.append(f"- {product.name}: ${product.price} ({product.stock_quantity} in stock)")
    
    # Search for order information
    if "order" in message.lower():
        recent_orders = db.query(Order).limit(3).all()
        if recent_orders:
            context_parts.append("\nRecent orders:")
            for order in recent_orders:
                context_parts.append(f"- Order #{order.id}: {order.quantity} items, ${order.total_amount}")
    
    return "\n".join(context_parts)

