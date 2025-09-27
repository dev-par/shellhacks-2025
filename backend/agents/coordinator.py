"""
Coordinator Agent - Manages the 5-state AERTS machine
S1: INITIAL_STABILIZATION → S2: DIAGNOSTIC_CONFIRMATION → S3: CRITICAL_CONSULTATION → S4: SENIOR_HANDOVER → S5: DEBRIEFING
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from models.scenario import AERTSState, ClinicalOrder, StateTransition, CoordinatorIntent, ClinicalWarning
from models.commands import UserCommand, CoordinatorResponse, StateTransitionResult

logger = logging.getLogger(__name__)

class CoordinatorAgent:
    """Coordinator Agent managing the 5-state AERTS machine"""
    
    def __init__(self):
        self.state_transitions = {
            "S1_INITIAL_STABILIZATION": {
                "triggers": ["asa_administered", "ecg_ordered"],
                "next_state": "S2_DIAGNOSTIC_CONFIRMATION",
                "required_conditions": ["asa_administered", "ecg_ordered"]
            },
            "S2_DIAGNOSTIC_CONFIRMATION": {
                "triggers": ["ecg_completed", "nitro_ordered", "morphine_ordered"],
                "next_state": "S3_CRITICAL_CONSULTATION",
                "required_conditions": ["ecg_completed"]
            },
            "S3_CRITICAL_CONSULTATION": {
                "triggers": ["sbar_consulted"],
                "next_state": "S4_SENIOR_HANDOVER",
                "required_conditions": ["sbar_consulted", "sbar_approved"]
            },
            "S4_SENIOR_HANDOVER": {
                "triggers": ["senior_handover_completed"],
                "next_state": "S5_DEBRIEFING",
                "required_conditions": ["senior_handover_completed"]
            }
        }
        
    async def start_scenario(self, initial_state: AERTSState):
        """Initialize the AERTS scenario"""
        logger.info(f"Starting AERTS scenario in state: {initial_state.current_state}")
        
    async def process_command(self, command: UserCommand, current_state: AERTSState) -> CoordinatorResponse:
        """Process trainee command and manage state transitions"""
        command_text = command.text.lower().strip()
        
        # Parse command and determine action
        action_result = await self._parse_command(command_text, current_state)
        
        if not action_result["success"]:
            return CoordinatorResponse(
                coordinator_message=action_result["message"],
                new_state=current_state,
                success=False
            )
        
        # Update state based on action
        new_state = await self._update_state_from_action(action_result, current_state)
        
        # Check for state transitions
        transition_result = await self._check_state_transition(new_state)
        
        # Generate intents for other agents
        nurse_intent, doctor_intent = await self._generate_agent_intents(
            action_result, new_state, transition_result
        )
        
        # Check for clinical safety issues
        clinical_warning = await self._check_clinical_safety(action_result, new_state)
        
        return CoordinatorResponse(
            coordinator_message=action_result["coordinator_message"],
            new_state=new_state,
            state_transition=transition_result,
            nurse_intent=nurse_intent,
            doctor_intent=doctor_intent,
            clinical_warning=clinical_warning,
            success=True
        )
    
    async def _parse_command(self, command_text: str, current_state: AERTSState) -> Dict[str, Any]:
        """Parse trainee command and determine action"""
        
        # S1 - Initial Stabilization commands
        if current_state.current_state == "S1_INITIAL_STABILIZATION":
            if any(word in command_text for word in ["aspirin", "asa", "325"]):
                return {
                    "success": True,
                    "action": "administer_asa",
                    "message": "Aspirin order received",
                    "coordinator_message": "Order received: Aspirin 325mg"
                }
            elif any(word in command_text for word in ["ecg", "ekg", "electrocardiogram", "12-lead"]):
                return {
                    "success": True,
                    "action": "order_ecg",
                    "message": "ECG order received",
                    "coordinator_message": "Order received: 12-lead ECG"
                }
            elif any(word in command_text for word in ["iv", "intravenous", "access"]):
                return {
                    "success": True,
                    "action": "establish_iv",
                    "message": "IV access order received",
                    "coordinator_message": "Order received: IV access"
                }
            elif any(word in command_text for word in ["oxygen", "o2"]):
                return {
                    "success": True,
                    "action": "start_oxygen",
                    "message": "Oxygen order received",
                    "coordinator_message": "Order received: Oxygen therapy"
                }
        
        # S2 - Diagnostic Confirmation commands
        elif current_state.current_state == "S2_DIAGNOSTIC_CONFIRMATION":
            if any(word in command_text for word in ["nitro", "nitroglycerin", "0.4"]):
                return {
                    "success": True,
                    "action": "order_nitro",
                    "message": "Nitroglycerin order received",
                    "coordinator_message": "Order received: Nitroglycerin 0.4mg SL"
                }
            elif any(word in command_text for word in ["morphine", "pain", "analgesia"]):
                return {
                    "success": True,
                    "action": "order_morphine",
                    "message": "Morphine order received",
                    "coordinator_message": "Order received: Morphine for pain management"
                }
            elif any(word in command_text for word in ["vitals", "status", "how is"]):
                return {
                    "success": True,
                    "action": "request_vitals",
                    "message": "Vitals request received",
                    "coordinator_message": "Requesting current vital signs"
                }
        
        # S3 - Critical Consultation commands
        elif current_state.current_state == "S3_CRITICAL_CONSULTATION":
            if any(word in command_text for word in ["sbar", "consult", "doctor", "cardiology"]):
                return {
                    "success": True,
                    "action": "sbar_consult",
                    "message": "SBAR consultation requested",
                    "coordinator_message": "Initiating SBAR consultation with Doctor Agent"
                }
        
        # S4 - Senior Handover commands
        elif current_state.current_state == "S4_SENIOR_HANDOVER":
            if any(word in command_text for word in ["handover", "report", "summary", "brief"]):
                return {
                    "success": True,
                    "action": "senior_handover",
                    "message": "Senior handover requested",
                    "coordinator_message": "Initiating handover to Senior Doctor"
                }
        
        # Default response
        return {
            "success": False,
            "message": "Command not recognized for current state",
            "coordinator_message": f"Command not applicable in {current_state.current_state} phase"
        }
    
    async def _update_state_from_action(self, action_result: Dict[str, Any], current_state: AERTSState) -> AERTSState:
        """Update state based on action result"""
        new_state = current_state.model_copy()
        
        action = action_result["action"]
        
        if action == "administer_asa":
            new_state.asa_administered = True
            new_state.orders_given.append(ClinicalOrder(
                order_id=str(uuid.uuid4()),
                order_type="Aspirin 325mg",
                description="Chewable aspirin for antiplatelet therapy",
                timestamp=datetime.now(),
                status="completed"
            ))
        
        elif action == "order_ecg":
            new_state.ecg_ordered = True
            new_state.orders_given.append(ClinicalOrder(
                order_id=str(uuid.uuid4()),
                order_type="12-lead ECG",
                description="Electrocardiogram for STEMI diagnosis",
                timestamp=datetime.now(),
                status="in_progress"
            ))
            # Simulate ECG completion after 5 seconds
            asyncio.create_task(self._complete_ecg_after_delay(new_state))
        
        elif action == "establish_iv":
            new_state.iv_access = True
            new_state.orders_given.append(ClinicalOrder(
                order_id=str(uuid.uuid4()),
                order_type="IV Access",
                description="Peripheral IV line establishment",
                timestamp=datetime.now(),
                status="completed"
            ))
        
        elif action == "start_oxygen":
            new_state.oxygen_started = True
            new_state.orders_given.append(ClinicalOrder(
                order_id=str(uuid.uuid4()),
                order_type="Oxygen Therapy",
                description="Oxygen 2L/min via nasal cannula",
                timestamp=datetime.now(),
                status="completed"
            ))
        
        elif action == "order_nitro":
            new_state.nitro_ordered = True
            new_state.orders_given.append(ClinicalOrder(
                order_id=str(uuid.uuid4()),
                order_type="Nitroglycerin 0.4mg SL",
                description="Sublingual nitroglycerin",
                timestamp=datetime.now(),
                status="pending"
            ))
        
        elif action == "order_morphine":
            new_state.morphine_ordered = True
            new_state.orders_given.append(ClinicalOrder(
                order_id=str(uuid.uuid4()),
                order_type="Morphine 2-4mg IV",
                description="IV morphine for pain management",
                timestamp=datetime.now(),
                status="pending"
            ))
        
        return new_state
    
    async def _complete_ecg_after_delay(self, state: AERTSState):
        """Complete ECG after 5 second delay"""
        await asyncio.sleep(5)
        state.ecg_completed = True
        # Update the order status
        for order in state.orders_given:
            if order.order_type == "12-lead ECG":
                order.status = "completed"
                order.result = "ST elevation in leads II, III, aVF - Inferior STEMI"
                break
    
    async def _check_state_transition(self, current_state: AERTSState) -> Optional[Dict[str, Any]]:
        """Check if state transition should occur"""
        current_state_name = current_state.current_state
        
        if current_state_name not in self.state_transitions:
            return None
        
        transition_rules = self.state_transitions[current_state_name]
        
        # Check if all required conditions are met
        conditions_met = True
        for condition in transition_rules["required_conditions"]:
            if not getattr(current_state, condition, False):
                conditions_met = False
                break
        
        if conditions_met:
            # Perform state transition
            new_state_name = transition_rules["next_state"]
            current_state.current_state = new_state_name
            
            # Record transition
            transition = StateTransition(
                from_state=current_state_name,
                to_state=new_state_name,
                trigger="automatic",
                timestamp=datetime.now(),
                success=True,
                message=f"Transitioned from {current_state_name} to {new_state_name}"
            )
            current_state.state_transitions.append(transition)
            
            return {
                "transitioned": True,
                "from_state": current_state_name,
                "to_state": new_state_name,
                "message": f"State transition: {current_state_name} → {new_state_name}"
            }
        
        return None
    
    async def _generate_agent_intents(self, action_result: Dict[str, Any], 
                                    current_state: AERTSState, 
                                    transition_result: Optional[Dict[str, Any]]) -> tuple:
        """Generate intents for Nurse and Doctor agents"""
        nurse_intent = None
        doctor_intent = None
        
        action = action_result["action"]
        
        # Generate nurse intent based on action
        if action in ["administer_asa", "order_ecg", "establish_iv", "start_oxygen", "order_nitro", "order_morphine"]:
            nurse_intent = CoordinatorIntent(
                target_agent="nurse",
                intent_type="acknowledge_order",
                data={
                    "order_type": action_result["message"],
                    "patient_state": current_state.patient_vitals.dict()
                },
                priority=1
            )
        
        elif action == "request_vitals":
            nurse_intent = CoordinatorIntent(
                target_agent="nurse",
                intent_type="provide_status_update",
                data={
                    "vitals": current_state.patient_vitals.dict(),
                    "orders_status": [order.dict() for order in current_state.orders_given]
                },
                priority=1
            )
        
        # Generate doctor intent for SBAR consultation
        elif action == "sbar_consult":
            doctor_intent = CoordinatorIntent(
                target_agent="doctor",
                intent_type="sbar_consultation",
                data={
                    "patient_state": current_state.patient_vitals.dict(),
                    "orders_given": [order.dict() for order in current_state.orders_given],
                    "current_phase": current_state.current_state
                },
                priority=2
            )
        
        return nurse_intent, doctor_intent
    
    async def _check_clinical_safety(self, action_result: Dict[str, Any], 
                                   current_state: AERTSState) -> Optional[ClinicalWarning]:
        """Check for clinical safety issues"""
        action = action_result["action"]
        vitals = current_state.patient_vitals
        
        # Check for nitroglycerin contraindication (hypotension)
        if action == "order_nitro":
            systolic_bp = int(vitals.bp.split('/')[0])
            if systolic_bp < 100:
                return ClinicalWarning(
                    warning_type="contraindication",
                    message="Systolic BP is below 100 mmHg - nitroglycerin contraindicated",
                    severity="high",
                    recommendation="Consider alternative pain management or fluid resuscitation first",
                    timestamp=datetime.now()
                )
        
        # Check for morphine contraindication (respiratory depression risk)
        if action == "order_morphine":
            if vitals.rr < 12:
                return ClinicalWarning(
                    warning_type="contraindication",
                    message="Respiratory rate is below 12 - morphine may cause respiratory depression",
                    severity="high",
                    recommendation="Consider lower dose or alternative pain management",
                    timestamp=datetime.now()
                )
        
        return None
    
    async def transition_to_s4(self, current_state: AERTSState) -> StateTransitionResult:
        """Transition to S4 (Senior Handover) after SBAR approval"""
        current_state.current_state = "S4_SENIOR_HANDOVER"
        
        transition = StateTransition(
            from_state="S3_CRITICAL_CONSULTATION",
            to_state="S4_SENIOR_HANDOVER",
            trigger="sbar_approved",
            timestamp=datetime.now(),
            success=True,
            message="SBAR consultation approved - Senior Doctor arriving"
        )
        current_state.state_transitions.append(transition)
        
        return StateTransitionResult(
            success=True,
            from_state="S3_CRITICAL_CONSULTATION",
            to_state="S4_SENIOR_HANDOVER",
            trigger="sbar_approved",
            message="Senior Doctor is arriving for handover",
            new_state=current_state,
            coordinator_message="Senior Doctor is here. Prepare your handover report using SBAR structure."
        )
    
    async def transition_to_s5(self, current_state: AERTSState) -> StateTransitionResult:
        """Transition to S5 (Debriefing) after handover completion"""
        current_state.current_state = "S5_DEBRIEFING"
        current_state.final_debrief_generated = True
        
        transition = StateTransition(
            from_state="S4_SENIOR_HANDOVER",
            to_state="S5_DEBRIEFING",
            trigger="handover_completed",
            timestamp=datetime.now(),
            success=True,
            message="Handover completed - Generating final debrief"
        )
        current_state.state_transitions.append(transition)
        
        return StateTransitionResult(
            success=True,
            from_state="S4_SENIOR_HANDOVER",
            to_state="S5_DEBRIEFING",
            trigger="handover_completed",
            message="Simulation complete - Final debrief generated",
            new_state=current_state,
            coordinator_message="Simulation complete. Final debrief and evaluation available.",
            final_debrief={
                "completion_time": (datetime.now() - current_state.start_time).total_seconds(),
                "orders_completed": len([o for o in current_state.orders_given if o.status == "completed"]),
                "state_transitions": len(current_state.state_transitions),
                "clinical_warnings": len(current_state.clinical_warnings)
            }
        )
