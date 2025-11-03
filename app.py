#!/usr/bin/env python3
"""
Flask web application for the Data Structure Visualizer
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import random
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    """API endpoint for AI Mode queries - forwards to API server"""
    try:
        # Forward the request to the API server
        import requests
        
        data = request.get_json()
        query = data.get('question', '').strip()
        
        if not query:
            return jsonify({"response": "Please ask something about data structures or algorithms."}), 400
            
        # Forward to API server running on port 5090
        api_response = requests.post(
            'http://127.0.0.1:5090/api/ask_ai',
            json={"question": query},
            timeout=30
        )
        
        # Return the API response
        return api_response.json(), api_response.status_code
        
    except Exception as e:
        return jsonify({"error": f"Error connecting to API server: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 9080))
    app.run(host='0.0.0.0', port=port)
