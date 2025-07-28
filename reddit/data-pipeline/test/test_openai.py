# test_openai.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def test_openai_connection():
    """Test if OpenAI API is working"""
    try:
        # Check if API key exists
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("No OPENAI_API_KEY found in .env file")
            return False
        
        print(f"API key found: {api_key[:10]}...")
        
        # Test API connection
        client = OpenAI(api_key=api_key)
        
        print("Testing API connection...")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Say 'Hello, API is working!'"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"API Response: {result}")
        
        return True
        
    except Exception as e:
        print(f"API Error: {e}")
        return False

def test_json_classification():
    """Test classification with simple example"""
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        prompt = """
Analyze this project and return ONLY a JSON object:

Title: Chrome extension for productivity
Description: A tool to block distracting websites

Return only this JSON structure:
{
    "main_category": "Browser Extensions",
    "sub_niche": "Productivity",
    "tech_stack": ["JavaScript", "Chrome API"],
    "confidence": "high"
}
"""
        
        print("Testing JSON classification...")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a JSON-only classifier. Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=200
        )
        
        raw_response = response.choices[0].message.content
        print(f"Raw response: {raw_response}")
        
        # Try to parse JSON
        import json
        parsed = json.loads(raw_response)
        print(f"Parsed JSON: {parsed}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        print(f"Raw response was: {raw_response}")
        return False
    except Exception as e:
        print(f"API Error: {e}")
        return False

if __name__ == "__main__":
    print("OpenAI API Testing")
    print("="*30)
    
    # Test 1: Basic connection
    if test_openai_connection():
        print("\n" + "="*30)
        # Test 2: JSON classification
        test_json_classification()
    else:
        print("\nFix API connection first!")
        print("\nChecklist:")
        print("1. Add OPENAI_API_KEY to your .env file")
        print("2. Make sure you have OpenAI credits")
        print("3. Check if API key is valid")