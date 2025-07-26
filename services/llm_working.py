import os
from sqlalchemy.orm import Session
from database import Product, Customer, Order
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Try to use Groq, fallback to mock
try:
    from groq import Groq
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        client = Groq(api_key=api_key)
        USE_GROQ = True
        print("✅ Using Groq AI")
    else:
        USE_GROQ = False
        print("⚠️ No API key, using mock responses")
except Exception as e:
    USE_GROQ = False
    print(f"⚠️ Groq failed, using mock responses: {e}")

async def get_ai_response(user_message: str, conversation_id: int, db: Session) -> str:
    try:
        if USE_GROQ and 'client' in globals():
            # Use real Groq
            ecommerce_keywords = ["product", "order", "buy", "purchase", "price", "stock", "customer"]
            is_ecommerce_query = any(keyword in user_message.lower() for keyword in ecommerce_keywords)
            
            system_prompt = """You are a helpful AI assistant for an e-commerce platform. 
            You can help users with product information, orders, and general questions.
            Be concise and friendly in your responses."""
            
            context = ""
            if is_ecommerce_query:
                context = get_ecommerce_context(user_message, db)
                if context:
                    system_prompt += f"\n\nHere's relevant information from our database:\n{context}"
            
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        else:
            # Use mock response
            return get_mock_response(user_message, db)
            
    except Exception as e:
        print(f"Error in AI response: {e}")
        return get_mock_response(user_message, db)

def get_mock_response(user_message: str, db: Session) -> str:
    """Smart mock responses based on user input"""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ["product", "item", "buy", "price"]):
        context = get_ecommerce_context(user_message, db)
        return f"Here are our available products:\n\n{context}\n\nWould you like more details about any specific product? (Note: Using mock AI - Groq will be connected soon!)"
    
    elif "order" in message_lower:
        context = get_ecommerce_context(user_message, db)
        return f"Here's information about orders:\n\n{context}\n\nWhat would you like to know about orders? (Note: Using mock AI)"
    
    elif any(word in message_lower for word in ["hello", "hi", "hey"]):
        return "Hello! 👋 I'm your e-commerce AI assistant. I can help you with:\n\n• Product information\n• Order details\n• General questions\n\nWhat would you like to know? (Note: Using mock AI - Groq will be connected soon!)"
    
    else:
        return f"I understand you're asking about: '{user_message}'\n\nI'm your e-commerce assistant and I can help with products, orders, and general questions. Could you be more specific about what you'd like to know? (Note: Using mock AI - Groq will be connected soon!)"

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