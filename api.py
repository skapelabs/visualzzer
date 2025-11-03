#!/usr/bin/env python3
"""
API server for Data Structure Visualizer - Handles AI requests via OpenRouter
"""

from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Root route for simple testing
@app.route('/')
def index():
    """Simple route to check if server is running"""
    return "API Server running ✅"

@app.route('/api/ask_ai', methods=['POST'])
def ask_ai():
    """API endpoint for AI queries using OpenRouter"""
    try:
        # Get request data
        data = request.get_json()
        question = data.get("question", "").strip()
        
        if not question:
            return jsonify({"response": "Please provide a question."}), 400
            
        # Check if API key is available
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return jsonify({
                "response": "API key not configured. Please set OPENROUTER_API_KEY in .env file.",
                "error": "Missing API key"
            }), 500
        
        # Initialize OpenAI client with OpenRouter base URL
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        # Make request to OpenRouter - real implementation
        try:
            # Real API call to OpenRouter
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "http://localhost:5090",
                    "X-Title": "Visualizer App"
                },
                model="openai/gpt-oss-20b:free",
                    messages=[
        {
            "role": "system",
            "content": (
                "You are an AI tutor who explains topics in Data Structures and Algorithms like a knowledgeable friend — "
                "simple, clear, and slightly conversational but still professional. "
                "Only answer questions related to Data Structures, Algorithms, or Computer Science fundamentals. "
                "If the user asks something unrelated, reply exactly with: "
                "'This bot only answers questions related to Data Structures and Computer Science.' "
                "Keep answers concise and easy to read — ideally in short points or small paragraphs, no markdown symbols like ** or ##. "
                "When giving code examples, always use C language syntax with proper indentation, short explanation, "
                "and avoid unnecessary comments or long intros. "
                "Focus on clarity, understanding, and real-world intuition over theory dumps."
            )
        },
        {"role": "user", "content": question}
    ],
    max_tokens=350,
    temperature=0.6,
)
            
            # Extract and return response
            reply = completion.choices[0].message.content
            return jsonify({"response": reply})
            
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({"error": str(e)}), 400
        
        # This code is unreachable - removing redundant block
        # The response is already handled in the try block above
        
    except Exception as e:
        # Handle different types of errors
        error_type = type(e).__name__
        error_message = str(e)
        
        if "Unauthorized" in error_message or "Invalid API key" in error_message:
            return jsonify({
                "response": "Authentication failed. Please check your API key.",
                "error": error_message
            }), 401
        elif "not found" in error_message.lower() or "404" in error_message:
            return jsonify({
                "response": "The requested AI model is not available.",
                "error": error_message
            }), 404
        elif "timeout" in error_message.lower():
            return jsonify({
                "response": "The request timed out. Please try again later.",
                "error": error_message
            }), 504
        else:
            return jsonify({
                "response": "An error occurred while processing your request.",
                "error": f"{error_type}: {error_message}"
            }), 500

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5090))
    app.run(host='0.0.0.0', port=port, debug=True)
