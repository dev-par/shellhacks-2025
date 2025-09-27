"""
Command and response models for AERTS
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class CommandType(str, Enum):
    ORDER = "order"
    QUESTION = "question"
    STATUS = "status"
    TOOL_CALL = "tool_call"
    EMERGENCY = "emergency"

class UserCommand(BaseModel):
    """Command from trainee"""
    text: str
    timestamp: datetime
    command_type: CommandType = CommandType.ORDER
    confidence: float = 1.0
    session_id: Optional[str] = None

class ToolCall(BaseModel):
    """Tool call for SBAR or Handover"""
    tool_name: str
    parameters: Dict[str, Any]
    timestamp: datetime
    session_id: str

class AgentResponse(BaseModel):
    """Response from an agent"""
    text: str
    timestamp: datetime
    agent_name: str
    priority: int = 1  # 1=normal, 2=urgent, 3=critical
    emotion: str = "neutral"  # neutral, concerned, urgent, calm, professional
    metadata: Dict[str, Any] = {}

class CoordinatorResponse(BaseModel):
    """Coordinator agent response with state management"""
    coordinator_message: str
    new_state: 'AERTSState'
    state_transition: Optional[Dict[str, Any]] = None
    nurse_intent: Optional['CoordinatorIntent'] = None
    doctor_intent: Optional['CoordinatorIntent'] = None
    clinical_warning: Optional['ClinicalWarning'] = None
    success: bool = True

class ClinicalOrderValidation(BaseModel):
    """Validation result for a clinical order"""
    is_valid: bool
    reason: Optional[str] = None
    safety_warning: Optional[str] = None
    alternative_suggestion: Optional[str] = None
    contraindications: List[str] = []

class StateTransitionResult(BaseModel):
    """Result of state transition"""
    success: bool
    from_state: str
    to_state: str
    trigger: str
    message: str
    new_state: 'AERTSState'
    coordinator_message: str
    final_debrief: Optional[Dict[str, Any]] = None

# Forward reference resolution
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .scenario import AERTSState, CoordinatorIntent, ClinicalWarning

# Update forward references
CoordinatorResponse.model_rebuild()
StateTransitionResult.model_rebuild()
