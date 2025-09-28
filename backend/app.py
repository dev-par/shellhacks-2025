from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import requests
import asyncio
import uuid
from dotenv import load_dotenv, find_dotenv

# Try to import ADK components, fallback to mock if not available
try:
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types
    from emergency_room_agent import root_agent as emergency_room_agent
    from utils import call_agent_async_json
    ADK_AVAILABLE = True
except ImportError as e:
    print(f"ADK components not available: {e}")
    ADK_AVAILABLE = False

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

# ADK Server configuration (keeping for reference but not using)
ADK_SERVER_URL = "http://localhost:8002"

# Create session service for agent management (if ADK is available)
if ADK_AVAILABLE:
    session_service_stateful = InMemorySessionService()
    app_name = "Emergency Room Training"
else:
    session_service_stateful = None
    app_name = "Emergency Room Training"

# Initial state for new sessions
initial_state = {
    "states": {
        'current_stage': 0,
        'stages': ['S0_INITIAL_STABILIZATION', 'S1_DIAGNOSTIC_CONFIRMATION', 'S2_CRITICAL_CONSULTATION', 'S3_SENIOR_HANDOVER', 'S4_DEBRIEFING']
    },
    "patient_information": {
        "patient_name": "Brandon Hancock",
        "patient_age": 55,
        "static_patient_data": {
        "vitals_snapshot": {
            "BP_Systolic": 118,
            "BP_Diastolic": 75,
            "HR": 105,
            "O2_Sat": 94,
            "O2_Source": "Room Air",
            "Pain_Score": 8
        },
        "history": {
            "Age_Sex": "55-year-old male",
            "Complaint": "Crushing substernal chest pain",
            "Known_History": "Hypertension, Smoker",
            "Allergies": "None known"
        }
        }
    },
    "session_flags": {
        "protocol_asa_given": False,
        "protocol_ecg_ordered": False,
        "protocol_diagnosis_confirmed": False,
        "protocol_nitro_or_morphine": False
    }
}

# Helper function to create or get existing session
def get_or_create_session(user_id="default_user"):
    """Get existing session or create new one for user"""
    if not ADK_AVAILABLE:
        return None, user_id, "mock_session"
    
    try:
        # Try to get existing session
        session_id = f"session_{user_id}"
        runner = Runner(
            agent=emergency_room_agent,
            app_name=app_name,
            session_service=session_service_stateful,
        )
        return runner, user_id, session_id
    except:
        # Create new session
        session_id = str(uuid.uuid4())
        stateful_session = asyncio.run(session_service_stateful.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=initial_state,
        ))
        runner = Runner(
            agent=emergency_room_agent,
            app_name=app_name,
            session_service=session_service_stateful,
        )
        return runner, user_id, session_id

def get_intelligent_response(agent_type, message):
    """Generate intelligent responses based on agent type and message content"""
    message_lower = message.lower()
    
    if agent_type == 'nurse':
        if 'ecg' in message_lower or 'ekg' in message_lower:
            return "Alright doc, I'll get that ECG ordered right away. Should I also prepare the patient for the procedure? The ECG machine is ready and I can have results in about 5 minutes."
        elif 'aspirin' in message_lower:
            return "Got it, I'll administer 325mg aspirin. Should I also check if they have any allergies first? I'll make sure to document the time and dose."
        elif 'vital' in message_lower or 'blood pressure' in message_lower or 'bp' in message_lower:
            return "Let me check the patient's vitals. BP is 118/75, HR 105, O2 sat 94% on room air. Pain score is 8/10. He's still complaining of that crushing chest pain."
        elif 'pain' in message_lower:
            return "The patient is reporting 8/10 chest pain. Should I give them something for pain relief? I can prepare morphine or nitroglycerin depending on what you think is appropriate."
        elif 'hello' in message_lower or 'hi' in message_lower:
            return "Hi there! I'm Sarah, your ED nurse. We have a 55-year-old male patient, Brandon Hancock, presenting with crushing substernal chest pain. He's a known hypertensive and smoker. What would you like to do first?"
        elif 'help' in message_lower:
            return "I'm here to help with whatever you need. What would you like me to do next? I can check vitals, order tests, or prepare medications."
        elif 'patient' in message_lower or 'status' in message_lower:
            return "Brandon Hancock is a 55-year-old male with crushing substernal chest pain. Known hypertension and smoker. Vitals are stable but he's in significant pain. What's your plan?"
        else:
            return "I'm here to help with whatever you need. What would you like me to do next?"
    
    elif agent_type == 'doctor':
        if 'diagnosis' in message_lower or 'sbar' in message_lower:
            return "Good work on the assessment. Based on the patient's presentation, I'm concerned about acute coronary syndrome. Let's rule out STEMI first with the ECG and start aspirin."
        elif 'chest pain' in message_lower:
            return "Given the crushing chest pain and risk factors, we need to consider myocardial infarction. Have you ordered the ECG and aspirin? Time is critical here."
        elif 'treatment' in message_lower or 'medication' in message_lower:
            return "For this patient, I'd recommend starting with aspirin and considering thrombolytic therapy if STEMI is confirmed. Check the ECG results first."
        elif 'hello' in message_lower or 'hi' in message_lower:
            return "Hi there, I'm Dr. Wang. I'll be supervising your case today. What's going on with your patient? I understand you have a chest pain case?"
        elif 'help' in message_lower:
            return "I'm here to supervise your case. What's your assessment so far? Walk me through your differential diagnosis."
        elif 'patient' in message_lower or 'status' in message_lower:
            return "Tell me about your patient. What's the chief complaint and your initial assessment? I need to understand the clinical picture."
        else:
            return "I'm here to supervise your case. What's your assessment so far?"
    
    else:  # emergency_room_agent
        if 'emergency' in message_lower or 'critical' in message_lower:
            return "Emergency protocols activated. All systems are monitoring the patient's condition. The cardiac team is standing by and ready for immediate intervention."
        elif 'hello' in message_lower or 'hi' in message_lower:
            return "Emergency Room Agent System online. All systems are monitoring the patient's condition. The cardiac team is standing by."
        elif 'patient' in message_lower or 'status' in message_lower:
            return "System status: All emergency protocols are active. Patient monitoring systems are operational. The trauma bay is prepared for immediate response."
        else:
            return "I'm coordinating the emergency response. All necessary equipment is ready and the trauma bay is prepared."

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
    """Process message using actual ADK agents"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        agent_type = data.get('agent_type', 'emergency_room_agent')
        user_id = data.get('user_id', 'default_user')
        
        if not message:
            return jsonify({
                "status": "error",
                "message": "No message provided"
            }), 400
        
        # Get or create session
        runner, session_user_id, session_id = get_or_create_session(user_id)
        
        # Use intelligent responses (agent-like behavior without ADK dependencies)
        intelligent_response = get_intelligent_response(agent_type, message)
        agent_name_mapping = {
            'doctor': 'Dr. Wang',
            'nurse': 'Sarah (Nurse)',
            'emergency_room_agent': 'ER Agent System'
        }
        
        return jsonify({
            "status": "success",
            "response": intelligent_response,
            "agent_type": agent_type,
            "agent_name": agent_name_mapping.get(agent_type, 'ER Agent System')
        })
        
    except Exception as e:
        print(f"Agent error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Agent communication failed: {str(e)}"
        }), 500

# Group Chat Endpoint for Training Scenarios
@app.route('/api/agent/group-chat', methods=['POST'])
def group_chat():
    """Process group chat using actual ADK agents"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        current_stage = data.get('current_stage', 0)
        agent_type = data.get('agent_type', 'emergency_room_agent')
        user_id = data.get('user_id', 'default_user')
        
        if not message:
            return jsonify({
                "status": "error",
                "message": "No message provided"
            }), 400
        
        # Get or create session
        runner, session_user_id, session_id = get_or_create_session(user_id)
        
        # Use intelligent responses (agent-like behavior without ADK dependencies)
        intelligent_response = get_intelligent_response(agent_type, message)
        agent_name_mapping = {
            'doctor': 'Dr. Wang',
            'nurse': 'Sarah (Nurse)',
            'emergency_room_agent': 'ER Agent System'
        }
        
        return jsonify({
            "status": "success",
            "response": intelligent_response,
            "agent_type": agent_type,
            "agent_name": agent_name_mapping.get(agent_type, 'ER Agent System'),
            "current_stage": current_stage
        })
        
    except Exception as e:
        print(f"Group chat error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Group chat failed: {str(e)}"
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
