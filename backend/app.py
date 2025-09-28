from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv, find_dotenv
# from emergency_room_agent.agent import root_agent  # Temporarily disabled

# Load environment variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
else:
    load_dotenv()

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes with specific frontend origin
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# Configuration
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['PORT'] = int(os.getenv('FLASK_PORT', 8000))  # Default to 8000

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Emergency Room Agent API",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/ping')
def ping():
    """Simple ping endpoint to check if server is running"""
    return jsonify({
        "status": "pong",
        "message": "Server is running!",
        "timestamp": "2024-01-01T00:00:00Z"  # You can add actual timestamp if needed
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "emergency-room-agent",
        "uptime": "running"
    })

# Auth0 Authentication Routes (simplified for now)
@app.route("/auth/user")
def get_user():
    """Get current user info - simplified for testing"""
    return jsonify({
        "status": "authenticated",
        "user": {
            "sub": "test-user-123",
            "email": "test@example.com",
            "name": "Test User",
            "picture": "https://via.placeholder.com/150"
        }
    })

# Protected API Routes (simplified for now)
@app.route('/api/protected')
def protected():
    """Protected endpoint - simplified for testing"""
    return jsonify({
        "status": "success",
        "message": "This is a protected endpoint",
        "user": {
            "sub": "test-user-123",
            "email": "test@example.com",
            "name": "Test User"
        }
    })

# Agent Communication Endpoints
@app.route('/api/agent/message', methods=['POST'])
def agent_message():
    """Send a message to the emergency room agent"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({
                "status": "error",
                "message": "No message provided"
            }), 400
        
        # For now, return a mock response
        # TODO: Integrate with actual agent
        response = {
            "status": "success",
            "response": f"Agent received: {message}",
            "agent_type": "emergency_room_agent"
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Agent communication failed: {str(e)}"
        }), 500

@app.route('/api/agent/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech audio to text"""
    try:
        # TODO: Implement actual speech-to-text using Google Cloud Speech
        # For now, return mock transcription
        return jsonify({
            "status": "success",
            "transcript": "Mock transcription from speech-to-text",
            "confidence": 0.95
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Speech-to-text failed: {str(e)}"
        }), 500

@app.route('/api/agent/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech audio"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                "status": "error",
                "message": "No text provided"
            }), 400
        
        # TODO: Implement actual text-to-speech using Google Cloud Text-to-Speech
        # For now, return mock audio data
        return jsonify({
            "status": "success",
            "audio_url": f"/api/agent/audio/mock-{hash(text)}.wav",
            "text": text
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Text-to-speech failed: {str(e)}"
        }), 500

if __name__ == '__main__':
    import subprocess
    import time
    
    # Kill any process on port 8000 before starting
    print("🧹 Cleaning up port 8000...")
    try:
        result = subprocess.run(['lsof', '-ti', ':8000'], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid.strip():
                    subprocess.run(['kill', '-9', pid.strip()], check=False)
                    print(f"✅ Killed process {pid.strip()} on port 8000")
        else:
            print("✅ Port 8000 is already free")
    except Exception as e:
        print(f"⚠️  Could not clean up port 8000: {e}")
    
    time.sleep(1)  # Give processes time to die
    
    print(f"🚀 Starting Emergency Room Agent API on port {app.config['PORT']}")
    print(f"📡 Ping endpoint: http://localhost:{app.config['PORT']}/ping")
    print(f"🏠 Home endpoint: http://localhost:{app.config['PORT']}/")
    print(f"💚 Health check: http://localhost:{app.config['PORT']}/health")
    print(f"🔐 Auth login: http://localhost:{app.config['PORT']}/auth/login")
    print(f"👤 User info: http://localhost:{app.config['PORT']}/auth/user")
    print(f"🔒 Protected API: http://localhost:{app.config['PORT']}/api/protected")
    
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
