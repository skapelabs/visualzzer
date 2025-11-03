#!/usr/bin/env python3
"""
Flask web application for the Data Structure Visualizer
"""
import os
import sys
import json
import subprocess
import random
import threading
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from PyQt5.QtWidgets import QApplication

# Import our markdown display module
from ai_markdown_display import display_ai_response

# Function to check and create .env file if it doesn't exist
def ensure_env_file_exists():
    """Check if .env file exists, if not create it and prompt for API key"""
    env_path = Path('.env')
    env_exists = env_path.exists()
    
    if not env_exists:
        print("\n⚠️ No .env file found. Creating one now...")
        api_key = input("\n🔑 Please enter your OpenRouter API key (starts with 'sk-'): ")
        
        # Create basic .env file with the provided API key
        with open('.env', 'w') as f:
            f.write(f"OPENROUTER_API_KEY={api_key}\n")
            f.write("SECRET_KEY=auto_generated_secret_key\n")
            f.write("DEBUG=True\n")
            f.write("PORT=9090\n")
            f.write("API_PORT=5000\n")
        
        print("✅ .env file created successfully!")
        return True
    return False

# Ensure .env file exists before loading
env_created = ensure_env_file_exists()

# Load environment variables from .env file
load_dotenv()

# Verify API key exists and is valid
def verify_api_key():
    """Verify that a valid API key exists"""
    # Check for OpenRouter API key first, then fall back to OpenAI API key
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ No API key found. Please set OPENROUTER_API_KEY or OPENAI_API_KEY in your .env file.")
        return False, None
    
    # Check if key starts with sk-
    if not api_key.startswith("sk-"):
        print("⚠️ Warning: API key doesn't start with 'sk-'. This may not be a valid API key.")
        return False, api_key
    
    # Mask the API key for logging
    masked_key = f"{api_key[:7]}{'*' * (len(api_key) - 7)}"
    print(f"✅ API key loaded: {masked_key}")
    return True, api_key

# Initialize OpenAI client only if API key is valid
key_valid, api_key = verify_api_key()
client = None
if key_valid:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

# Print startup verification
print("\n=== Flask App Startup Verification ===")
print(f".env file found: {'✅' if os.path.exists('.env') else '❌'}")
print(f"API key loaded: {'✅' if api_key else '❌'}")
print(f"Key starts with sk-: {'✅' if api_key and api_key.startswith('sk-') else '❌'}")

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['DEBUG'] = True

def gen_random_list(n):
    """Generate random list of numbers"""
    return [random.randint(5, 100) for _ in range(n)]

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/home')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/how-to')
def how_to():
    """How-to page with instructions"""
    return render_template('how_to.html')

@app.route('/algorithms')
def algorithms():
    """Algorithms page"""
    return render_template('algorithms.html')

@app.route('/visualizer')
def visualizer():
    """Visualizer page"""
    return render_template('visualizer.html')

@app.route('/ai_mode')
def ai_mode():
    """AI Mode page"""
    return render_template('ai_mode.html')

@app.route('/api/random-numbers')
def api_random_numbers():
    """API endpoint to get random numbers"""
    count = request.args.get('count', 25, type=int)
    if count > 50:
        count = 50
    numbers = gen_random_list(count)
    return jsonify({
        'numbers': numbers,
        'count': len(numbers),
        'min': min(numbers),
        'max': max(numbers)
    })

@app.route('/api/check-dependencies')
def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        # Check for PyQt5
        import importlib.util
        pyqt_spec = importlib.util.find_spec("PyQt5")
        pyqt_available = pyqt_spec is not None
        
        # Check for pygame
        pygame_spec = importlib.util.find_spec("pygame")
        pygame_available = pygame_spec is not None
        
        return jsonify({
            "pyqt_available": pyqt_available,
            "pygame_available": pygame_available,
            "status": "ok"
        })
    except Exception as e:
        return jsonify({
            "pyqt_available": False,
            "pygame_available": False,
            "status": "error",
            "error": str(e)
        })

@app.route('/api/validate-numbers', methods=['POST'])
def validate_numbers():
    """Validate custom numbers input"""
    try:
        data = request.get_json()
        input_text = data.get('numbers', '').strip()
        
        # Split by any whitespace (spaces, tabs, newlines)
        number_strings = input_text.split()
        
        # Try to convert each string to an integer
        try:
            numbers = [int(num) for num in number_strings]
        except ValueError:
            return jsonify({
                "valid": False,
                "error": "Invalid input. Please enter only integers separated by spaces."
            })
        
        # Check if we have at least 2 numbers
        if len(numbers) < 2:
            return jsonify({
                "valid": False,
                "error": "Please enter at least 2 numbers."
            })
            
        # Check if we have too many numbers
        if len(numbers) > 100:
            return jsonify({
                "valid": False,
                "error": "Too many numbers. Please enter at most 100 numbers."
            })
        
        # Success case
        return jsonify({
            "valid": True,
            "numbers": numbers,
            "count": len(numbers),
            "min": min(numbers),
            "max": max(numbers)
        })
        
    except Exception as e:
        return jsonify({
            "valid": False,
            "error": f"Error validating numbers: {str(e)}"
        })

@app.route('/run-visualizer', methods=['POST', 'GET'])
def run_visualizer():
    """Launch the Pygame visualizer application"""
    try:
        # For GET requests, use default random numbers
        if request.method == 'GET':
            numbers = gen_random_list(25)
        else:
            # For POST requests, use provided numbers
            data = request.get_json()
            if data and 'numbers' in data:
                # If numbers is already a list, use it directly
                if isinstance(data['numbers'], list):
                    numbers = data['numbers']
                else:
                    # Otherwise, generate random numbers
                    numbers = gen_random_list(25)
            else:
                numbers = gen_random_list(25)
        
        # Save numbers to a temporary file
        import tempfile
        import subprocess
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
        json.dump({"numbers": numbers}, temp_file)
        temp_file.close()
        
        # Launch the visualizer in a separate process - use visualiser.py (Pygame) instead of visualiser_pyqt5.py
        subprocess.Popen(['python', 'visualiser.py', temp_file.name])
        
        return jsonify({"success": True, "message": "Visualizer launched successfully"})
    except Exception as e:
        print(f"Error launching visualizer: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/ask_ai', methods=['POST'])
def ask_ai():
    """API endpoint to ask AI a question about data structures and algorithms"""
    try:
        # Check if client is properly initialized
        if client is None:
            print("❌ AI request failed: OpenAI client not initialized")
            return jsonify({"response": "AI unavailable. Please check your API key or network."}), 503
        
        data = request.get_json()
        question = data.get("question", "")
        display_in_pyqt = data.get("display_in_pyqt", False)
        
        if not question:
            return jsonify({"response": "Please provide a question."}), 400
        
        # Mask API key in logs
        masked_key = f"{api_key[:7]}{'*' * (len(api_key) - 7)}" if api_key else "None"
        print(f"Making AI request with key: {masked_key}")
        
        # Make the API request with proper error handling
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b:free",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that explains data structures and algorithms simply and visually."},
                    {"role": "user", "content": question}
                ],
                extra_headers={
                    "HTTP-Referer": f"http://localhost:{port}",  # your site url
                    "X-Title": "Data Structure Visualizer",  # app name
                }
            )
            
            answer = completion.choices[0].message.content
            
            # If display_in_pyqt flag is set, show the response in a PyQt window
            if display_in_pyqt:
                # Launch in a separate thread to avoid blocking the Flask server
                threading.Thread(target=lambda: display_ai_response(answer, f"AI Response: {question[:30]}...")).start()
            
            return jsonify({"response": answer})
            
        except Exception as api_error:
            print(f"❌ OpenRouter API error: {str(api_error)}")
            # Keep the app running but return a friendly error message
            return jsonify({"response": "AI unavailable. Please check your key or network."}), 503

    except Exception as e:
        print(f"❌ General error in ask_ai endpoint: {str(e)}")
        return jsonify({"response": "Something went wrong. Please try again later."}), 500



if __name__ == '__main__':
    # Get port from environment variables with fallback
    port = int(os.getenv('PORT', 9090))
    
    # Print final verification message
    print(f"Flask app running at port: ✅ {port}")
    print("=== Server Starting ===\n")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port)

