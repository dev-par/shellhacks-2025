"""
AERTS Scenario Models - STEMI Protocol
"""

from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class PatientVitals(BaseModel):
    """Patient vital signs for STEMI case"""
    bp: str  # Blood pressure
    hr: int  # Heart rate
    rr: int  # Respiratory rate
    temp: float  # Temperature
    o2_sat: int  # Oxygen saturation
    pain_level: int  # Pain scale 1-10
    diaphoresis: bool  # Sweating

class ClinicalOrder(BaseModel):
    """Clinical order given by trainee"""
    order_id: str
    order_type: str
    description: str
    timestamp: datetime
    status: str = "pending"  # pending, completed, failed
    result: Optional[str] = None

class AERTSState(BaseModel):
    """AERTS simulation state following the 5-state machine"""
    session_id: str
    current_state: str  # S1, S2, S3, S4, S5
    patient_vitals: PatientVitals
    orders_given: List[ClinicalOrder] = []
    
    # S1 - Initial Stabilization flags
    asa_administered: bool = False
    ecg_ordered: bool = False
    ecg_completed: bool = False
    iv_access: bool = False
    oxygen_started: bool = False
    
    # S2 - Diagnostic Confirmation flags
    nitro_ordered: bool = False
    morphine_ordered: bool = False
    
    # S3 - Critical Consultation flags
    sbar_consulted: bool = False
    sbar_response: Optional[Dict[str, Any]] = None
    
    # S4 - Senior Handover flags
    senior_handover_completed: bool = False
    handover_evaluation: Optional[Dict[str, Any]] = None
    
    # S5 - Debriefing flags
    final_debrief_generated: bool = False
    
    # Timing
    start_time: datetime
    state_transitions: List[Dict[str, Any]] = []
    
    # Clinical safety flags
    clinical_warnings: List[str] = []
    
    class Config:
        use_enum_values = True

class StateTransition(BaseModel):
    """State transition result"""
    from_state: str
    to_state: str
    trigger: str
    timestamp: datetime
    success: bool
    message: str

class CoordinatorIntent(BaseModel):
    """Intent published by Coordinator to other agents"""
    target_agent: str
    intent_type: str
    data: Dict[str, Any]
    priority: int = 1

class NurseResponse(BaseModel):
    """Nurse agent response"""
    text: str
    timestamp: datetime
    intent_processed: str
    clinical_update: Optional[Dict[str, Any]] = None

class DoctorResponse(BaseModel):
    """Doctor agent response"""
    text: str
    timestamp: datetime
    approval_status: Optional[str] = None
    feedback: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None

class ClinicalWarning(BaseModel):
    """Clinical safety warning"""
    warning_type: str
    message: str
    severity: str  # low, medium, high, critical
    recommendation: str
    timestamp: datetime

class SBARData(BaseModel):
    """SBAR (Situation, Background, Assessment, Recommendation) data"""
    situation: str
    background: str
    assessment: str
    recommendation: str
    timestamp: datetime
    trainee_id: Optional[str] = None

class HandoverData(BaseModel):
    """Senior Doctor handover data"""
    patient_summary: str
    current_status: str
    interventions_performed: List[str]
    pending_actions: List[str]
    critical_concerns: List[str]
    timestamp: datetime
    trainee_id: Optional[str] = None

class EvaluationResult(BaseModel):
    """Evaluation result for handover or overall performance"""
    overall_score: float
    sbar_completeness: float
    clinical_accuracy: float
    communication_quality: float
    timing_efficiency: float
    feedback: str
    recommendations: List[str]
    timestamp: datetime
