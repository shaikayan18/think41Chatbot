import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check API key
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key starts with: {api_key[:10]}...")
    print(f"API Key length: {len(api_key)}")

# Test Groq import and client creation
try:
    from groq import Groq
    print("✅ Groq import successful")
    
    if api_key:
        client = Groq(api_key=api_key)
        print("✅ Groq client created successfully")
        
        # Test a simple request
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": "Hello, say hi back!"}],
            max_tokens=50
        )
        print(f"✅ Test response: {response.choices[0].message.content}")
        
    else:
        print("❌ No API key found")
        
except Exception as e:
    print(f"❌ Error: {e}")