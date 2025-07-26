import os
from groq import Groq
from sqlalchemy.orm import Session
from database import Product, Customer, Order
from typing import Optional

# Initialize Groq client with error handling
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    print(f"Warning: Groq client initialization failed: {e}")
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
        
    except Exception as e:
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









import os
from groq import Groq
from sqlalchemy.orm import Session
from database import Product, Customer, Order
from typing import Optional

# Initialize Groq client with error handling
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    print(f"Warning: Groq client initialization failed: {e}")
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
        
    except Exception as e:
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









