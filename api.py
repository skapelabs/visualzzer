#!/usr/bin/env python3
"""
API server for Data Structure Visualizer - Handles AI requests via OpenRouter
"""
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import os
import json
import requests

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Simple route to check if server is running"""
    return "API Server running ✅"

@app.route('/api/ask_ai', methods=['POST'])
def ask_ai():
    """API endpoint for AI queries using OpenRouter"""
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"response": "Please provide a question."}), 400

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return jsonify({
                "response": "API key not configured. Please set OPENROUTER_API_KEY in .env file.",
                "error": "Missing API key"
            }), 500

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Referer": "http://localhost:5090",
            "X-Title": "Visualizer App"
        }

        payload = {
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an AI tutor for Data Structures and Algorithms. The Answer should be in a simple text format without any images"
                        "If the user asks something unrelated, reply exactly with: "
                        "'This bot only answers questions related to Data Structures and Computer Science.' "
                        "No markdown, no tables, no bold/italic, no emojis, no symbols like | or ##. "
                        "Just plain text paragraphs with short line breaks."
                    )
                },
                {"role": "user", "content": question}
            ],
            "max_tokens": 250,
            "temperature": 0.5
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            import re
            reply = re.sub(r"[*_#>`|~]+", "", reply)         # kill markdown symbols
            reply = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", reply)  # remove markdown links
            reply = re.sub(r"(?m)^\s*[-*]\s+", "", reply)    # remove bullet points
            reply = re.sub(r"(?m)^\s*\d+\.\s+", "", reply)   # remove numbered lists
            reply = re.sub(r"```.*?```", "", reply, flags=re.S)  # remove code blocks
            reply = re.sub(r"\n{2,}", "\n\n", reply)         # normalize newlines
            reply = re.sub(r"\s{2,}", " ", reply)            # collapse extra spaces
            reply = "\n".join(line.strip() for line in reply.splitlines() if line.strip())
            # send clean reply back to frontend
            return jsonify({"response": reply})
        else:
            print(f"AI request error: {response.status_code} - {response.text}")
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
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
