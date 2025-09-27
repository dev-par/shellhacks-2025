"""
Adaptive Emergency Response Training Simulator (AERTS)
STEMI Protocol Workflow Backend
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import uuid

from agents.coordinator import CoordinatorAgent
from agents.nurse import NurseAgent
from agents.doctor import DoctorAgent
from agents.evaluator import EvaluatorAgent
from models.scenario import AERTSState, PatientVitals, ClinicalOrder
from models.commands import UserCommand, AgentResponse, ToolCall
from services.voice_service import VoiceService
from services.a2a_client import A2AClient
from services.gemini_service import GeminiService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AERTS - STEMI Protocol", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state management
active_sessions: Dict[str, Dict] = {}

# Initialize services
voice_service = VoiceService()
a2a_client = A2AClient()
gemini_service = GeminiService()

@app.on_event("startup")
async def startup_event():
    """Initialize the AERTS system"""
    logger.info("Starting AERTS - STEMI Protocol Backend...")
    await gemini_service.initialize()
    logger.info("AERTS Backend ready!")

@app.post("/api/session/start")
async def start_session():
    """Start a new AERTS simulation session"""
    session_id = str(uuid.uuid4())
    
    # Initialize agents
    coordinator = CoordinatorAgent()
    nurse = NurseAgent(gemini_service)
    doctor = DoctorAgent(gemini_service)
    evaluator = EvaluatorAgent()
    
    # Create initial AERTS state (S1: INITIAL_STABILIZATION)
    initial_state = AERTSState(
        session_id=session_id,
        current_state="S1_INITIAL_STABILIZATION",
        patient_vitals=PatientVitals(
            bp="140/90",
            hr=95,
            rr=18,
            temp=98.6,
            o2_sat=96,
            pain_level=8,
            diaphoresis=True
        ),
        orders_given=[],
        asa_administered=False,
        ecg_ordered=False,
        ecg_completed=False,
        iv_access=False,
        oxygen_started=False,
        nitro_ordered=False,
        morphine_ordered=False,
        sbar_consulted=False,
        senior_handover_completed=False,
        start_time=datetime.now()
    )
    
    # Create session state
    session_state = {
        "session_id": session_id,
        "aerts_state": initial_state,
        "agents": {
            "coordinator": coordinator,
            "nurse": nurse,
            "doctor": doctor,
            "evaluator": evaluator
        },
        "is_active": True
    }
    
    active_sessions[session_id] = session_state
    
    # Start the scenario
    await coordinator.start_scenario(initial_state)
    
    return {
        "session_id": session_id,
        "current_state": initial_state.current_state,
        "patient": {
            "age": 55,
            "gender": "male",
            "chief_complaint": "crushing substernal chest pain",
            "pain_level": 8,
            "vitals": initial_state.patient_vitals.dict()
        },
        "message": "AERTS STEMI simulation started. State: S1 - Initial Stabilization"
    }

@app.post("/api/session/{session_id}/command")
async def process_command(session_id: str, command: UserCommand):
    """Process a user command and return agent responses"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    if not session["is_active"]:
        raise HTTPException(status_code=400, detail="Session is not active")
    
    try:
        # Process command through coordinator
        coordinator = session["agents"]["coordinator"]
        nurse = session["agents"]["nurse"]
        doctor = session["agents"]["doctor"]
        
        # Get current state
        current_state = session["aerts_state"]
        
        # Process command and check for state transitions
        response = await coordinator.process_command(command, current_state)
        
        # Update state
        session["aerts_state"] = response.new_state
        
        # Get nurse response based on coordinator intent
        nurse_response = await nurse.process_intent(response.nurse_intent, response.new_state)
        
        # Get doctor response if needed
        doctor_response = None
        if response.doctor_intent:
            doctor_response = await doctor.process_intent(response.doctor_intent, response.new_state)
        
        return {
            "coordinator": {
                "text": response.coordinator_message,
                "state_transition": response.state_transition,
                "new_state": response.new_state.current_state
            },
            "nurse": nurse_response,
            "doctor": doctor_response,
            "aerts_state": response.new_state.dict(),
            "clinical_warning": response.clinical_warning
        }
        
    except Exception as e:
        logger.error(f"Error processing command: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/session/{session_id}/tool/sbar_consult")
async def sbar_consult_tool(session_id: str, sbar_data: dict):
    """Execute SBAR consultation tool"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    current_state = session["aerts_state"]
    
    try:
        # Use A2A client to send SBAR to remote Doctor Agent
        doctor_response = await a2a_client.send_sbar_consult(sbar_data, current_state)
        
        # Update state
        current_state.sbar_consulted = True
        current_state.sbar_response = doctor_response
        
        # Check if we should transition to S4 (Senior Handover)
        if doctor_response.get("approval") == "APPROVED":
            coordinator = session["agents"]["coordinator"]
            transition_result = await coordinator.transition_to_s4(current_state)
            session["aerts_state"] = transition_result.new_state
            
            return {
                "success": True,
                "doctor_response": doctor_response,
                "state_transition": "S3 → S4",
                "new_state": transition_result.new_state.current_state,
                "coordinator_message": transition_result.coordinator_message
            }
        else:
            return {
                "success": False,
                "doctor_response": doctor_response,
                "message": "SBAR consultation completed but requires improvement"
            }
            
    except Exception as e:
        logger.error(f"Error in SBAR consult: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/session/{session_id}/tool/handover")
async def handover_tool(session_id: str, handover_data: dict):
    """Execute handover tool for Senior Doctor"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    current_state = session["aerts_state"]
    
    try:
        doctor = session["agents"]["doctor"]
        evaluator = session["agents"]["evaluator"]
        
        # Process handover with Doctor Agent (acting as Senior Doctor)
        handover_response = await doctor.process_handover(handover_data, current_state)
        
        # Evaluate the handover quality
        evaluation = await evaluator.evaluate_handover(handover_data, current_state)
        
        # Update state
        current_state.senior_handover_completed = True
        current_state.handover_evaluation = evaluation
        
        # Transition to S5 (Debriefing)
        coordinator = session["agents"]["coordinator"]
        transition_result = await coordinator.transition_to_s5(current_state)
        session["aerts_state"] = transition_result.new_state
        
        return {
            "success": True,
            "doctor_response": handover_response,
            "evaluation": evaluation,
            "state_transition": "S4 → S5",
            "new_state": transition_result.new_state.current_state,
            "final_debrief": transition_result.final_debrief
        }
        
    except Exception as e:
        logger.error(f"Error in handover: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/{session_id}/status")
async def get_session_status(session_id: str):
    """Get current session status"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    current_state = session["aerts_state"]
    
    return {
        "session_id": session_id,
        "current_state": current_state.current_state,
        "aerts_state": current_state.dict(),
        "is_active": session["is_active"],
        "elapsed_time": (datetime.now() - current_state.start_time).total_seconds()
    }

@app.post("/api/session/{session_id}/end")
async def end_session(session_id: str):
    """End the simulation session and get final debrief"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    session["is_active"] = False
    
    # Calculate final score and debrief
    evaluator = session["agents"]["evaluator"]
    final_debrief = await evaluator.generate_final_debrief(session["aerts_state"])
    
    return {
        "session_id": session_id,
        "final_debrief": final_debrief,
        "aerts_state": session["aerts_state"].dict(),
        "total_time": (datetime.now() - session["aerts_state"].start_time).total_seconds()
    }

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time voice communication"""
    await websocket.accept()
    
    if session_id not in active_sessions:
        await websocket.close(code=1008, reason="Session not found")
        return
    
    try:
        while True:
            # Receive audio data
            data = await websocket.receive_bytes()
            
            # Process voice command
            text = await voice_service.speech_to_text(data)
            command = UserCommand(text=text, timestamp=datetime.now())
            
            # Process command
            response = await process_command(session_id, command)
            
            # Convert responses to speech
            audio_responses = {}
            for agent, agent_response in response.items():
                if isinstance(agent_response, dict) and "text" in agent_response:
                    audio_data = await voice_service.text_to_speech(
                        agent_response["text"], 
                        "professional"
                    )
                    audio_responses[agent] = audio_data
            
            # Send response back
            await websocket.send_json({
                "text_responses": response,
                "audio_responses": audio_responses
            })
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1011, reason="Internal error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
