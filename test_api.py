#!/usr/bin/env python3
"""
Test script for the API server
Sends a sample request to the API server and prints the response
"""

import requests
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_connection():
    """Test if the API server is running"""
    try:
        response = requests.get('http://127.0.0.1:5090/')
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server. Is it running?")
        return False

def test_api_endpoint():
    """Test the /api/ask_ai endpoint"""
    print("\nTesting /api/ask_ai endpoint...")
    
    # Sample question
    payload = {
        "question": "What is the meaning of life?"
    }
    
    try:
        # Send request to API
        response = requests.post(
            'http://127.0.0.1:5090/api/ask_ai',
            json=payload,
            timeout=30
        )
        
        # Print response details
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nAPI Response:")
            print("-" * 50)
            print(data.get('response', 'No response found'))
            print("-" * 50)
            return True
        else:
            print("\nError Response:")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("API Test Script")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("⚠️  Warning: OPENROUTER_API_KEY not set in .env file")
    
    # Test API connection
    if test_api_connection():
        # Test API endpoint
        test_api_endpoint()
    else:
        print("\nPlease start the API server with: python api.py")
        sys.exit(1)