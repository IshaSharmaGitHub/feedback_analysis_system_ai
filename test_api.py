"""
Simple API test to diagnose connection issues
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import httpx

# Load environment variables
load_dotenv()

print("="*60)
print("OpenAI API Connection Test")
print("="*60)

# Check if API key exists
api_key = os.getenv('OPENAI_API_KEY')
print(f"\n1. API Key Check:")
print(f"   API Key exists: {api_key is not None}")
if api_key:
    print(f"   API Key starts with: {api_key[:10]}...")
    print(f"   API Key length: {len(api_key)} characters")
else:
    print(f"   ❌ ERROR: No API key found in .env file!")
    print(f"   Please create a .env file with OPENAI_API_KEY=your-key-here")
    exit(1)

# Test connection
print(f"\n2. Testing Connection:")
try:
    llm = ChatOpenAI(
        model="gpt-5-nano",
        temperature=0.3,
        timeout=30,
        http_client=httpx.Client(verify=False)
    )
    print(f"   ✅ LLM initialized successfully")
    
    print(f"\n3. Making Test Call:")
    response = llm.invoke("Say 'Connection successful!'")
    print(f"   ✅ API call successful!")
    print(f"   Response: {response.content}")
    
    print(f"\n" + "="*60)
    print("✅ ALL TESTS PASSED - API is working!")
    print("="*60)
    
except Exception as e:
    print(f"   ❌ Error occurred!")
    print(f"\n   Error Type: {type(e).__name__}")
    print(f"   Error Message: {str(e)}")
    print(f"\n" + "="*60)
    print("❌ TEST FAILED")
    print("="*60)
    
    # Provide specific help based on error type
    error_str = str(e).lower()
    if "api key" in error_str or "authentication" in error_str:
        print("\n💡 Solution: Your API key might be invalid or expired")
        print("   1. Go to https://platform.openai.com/api-keys")
        print("   2. Create a new API key")
        print("   3. Update your .env file with the new key")
    elif "connection" in error_str or "timeout" in error_str:
        print("\n💡 Solution: Connection issue detected")
        print("   1. Check your internet connection")
        print("   2. Check if a proxy/firewall is blocking the connection")
        print("   3. Try a different network")
    elif "rate limit" in error_str:
        print("\n💡 Solution: Rate limit exceeded")
        print("   1. Wait a few minutes and try again")
        print("   2. Check your OpenAI usage limits")
    else:
        print("\n💡 Check the error message above for more details")
