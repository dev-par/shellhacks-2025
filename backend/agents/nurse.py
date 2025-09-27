"""
Nurse Agent - Uses Gemini LLM for dynamic dialogue responses
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from models.scenario import AERTSState, CoordinatorIntent, NurseResponse
from services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class NurseAgent:
    """Nurse Agent with Gemini LLM integration for dynamic responses"""
    
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.name = "Nurse Sarah"
        self.role = "RN"
        
    async def process_intent(self, intent: CoordinatorIntent, current_state: AERTSState) -> NurseResponse:
        """Process intent from Coordinator and generate dynamic response"""
        if not intent:
            return NurseResponse(
                text="",
                timestamp=datetime.now(),
                intent_processed="none"
            )
        
        intent_type = intent.intent_type
        data = intent.data
        
        # Generate dynamic response using Gemini
        response_text = await self._generate_dynamic_response(intent_type, data, current_state)
        
        # Update patient state if needed
        clinical_update = await self._process_clinical_action(intent_type, data, current_state)
        
        return NurseResponse(
            text=response_text,
            timestamp=datetime.now(),
            intent_processed=intent_type,
            clinical_update=clinical_update
        )
    
    async def _generate_dynamic_response(self, intent_type: str, data: Dict[str, Any], 
                                       current_state: AERTSState) -> str:
        """Generate dynamic response using Gemini LLM"""
        
        # Create context for Gemini
        context = self._build_context(current_state, intent_type, data)
        
        # Generate prompt based on intent type
        prompt = self._build_prompt(intent_type, context, data)
        
        try:
            # Use Gemini to generate response
            response = await self.gemini_service.generate_nurse_response(prompt, context)
            return response
        except Exception as e:
            logger.error(f"Error generating nurse response: {e}")
            # Fallback to predefined responses
            return self._get_fallback_response(intent_type, data)
    
    def _build_context(self, current_state: AERTSState, intent_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for Gemini"""
        return {
            "patient_vitals": current_state.patient_vitals.dict(),
            "current_state": current_state.current_state,
            "orders_given": [order.dict() for order in current_state.orders_given],
            "intent_type": intent_type,
            "intent_data": data,
            "nurse_name": self.name,
            "nurse_role": self.role,
            "timestamp": datetime.now().isoformat()
        }
    
    def _build_prompt(self, intent_type: str, context: Dict[str, Any], data: Dict[str, Any]) -> str:
        """Build prompt for Gemini based on intent type"""
        
        base_prompt = f"""You are {context['nurse_name']}, an experienced RN in the emergency department. 
        You are responding to a medical trainee during a STEMI simulation.
        
        Current patient status:
        - Age: 55, Male
        - Chief complaint: Crushing substernal chest pain, 8/10
        - Vitals: BP {context['patient_vitals']['bp']}, HR {context['patient_vitals']['hr']}, 
          RR {context['patient_vitals']['rr']}, O2 Sat {context['patient_vitals']['o2_sat']}%
        - Current phase: {context['current_state']}
        
        Respond professionally and realistically as an experienced nurse would. Keep responses concise but informative.
        """
        
        if intent_type == "acknowledge_order":
            order_type = data.get("order_type", "medical order")
            return f"""{base_prompt}
            
            The trainee has given the order: "{order_type}"
            
            Acknowledge the order professionally and indicate you're carrying it out. 
            Provide brief status update if relevant.
            """
        
        elif intent_type == "provide_status_update":
            return f"""{base_prompt}
            
            The trainee has requested a status update on the patient.
            
            Provide a comprehensive but concise status report including:
            - Current vital signs
            - Patient's condition
            - Any changes since last assessment
            - Status of ongoing interventions
            """
        
        elif intent_type == "clinical_warning":
            issue = data.get("issue", "clinical concern")
            return f"""{base_prompt}
            
            There is a clinical safety concern: {issue}
            
            Express appropriate concern as a nurse would, suggest alternatives if appropriate,
            and ask for clarification on how to proceed.
            """
        
        else:
            return f"""{base_prompt}
            
            Respond to the current situation as an experienced nurse would.
            """
    
    def _get_fallback_response(self, intent_type: str, data: Dict[str, Any]) -> str:
        """Fallback responses if Gemini fails"""
        fallback_responses = {
            "acknowledge_order": "Understood, Doctor. I'll carry out that order right away.",
            "provide_status_update": "Patient is stable but still complaining of chest pain. Vitals are as reported.",
            "clinical_warning": "I have a concern about that order. Should we reconsider?",
            "default": "I'm here and ready to assist, Doctor."
        }
        
        return fallback_responses.get(intent_type, fallback_responses["default"])
    
    async def _process_clinical_action(self, intent_type: str, data: Dict[str, Any], 
                                     current_state: AERTSState) -> Optional[Dict[str, Any]]:
        """Process clinical action and return any state updates"""
        
        if intent_type == "acknowledge_order":
            order_type = data.get("order_type", "")
            
            # Simulate clinical effects based on order
            if "aspirin" in order_type.lower():
                return {
                    "medication_administered": "Aspirin 325mg",
                    "effect": "Antiplatelet therapy initiated",
                    "patient_response": "Patient is chewing aspirin as instructed"
                }
            elif "ecg" in order_type.lower():
                return {
                    "procedure_initiated": "12-lead ECG",
                    "status": "ECG leads applied, recording in progress",
                    "expected_completion": "5 seconds"
                }
            elif "iv" in order_type.lower():
                return {
                    "procedure_completed": "IV access established",
                    "location": "Left antecubital fossa",
                    "gauge": "18 gauge",
                    "status": "Ready for medications"
                }
            elif "oxygen" in order_type.lower():
                return {
                    "therapy_started": "Oxygen 2L/min via nasal cannula",
                    "effect": "O2 saturation improving",
                    "patient_response": "Patient tolerating well"
                }
            elif "nitro" in order_type.lower():
                return {
                    "medication_ready": "Nitroglycerin 0.4mg SL",
                    "status": "Administered sublingually",
                    "effect": "Patient reports some relief"
                }
            elif "morphine" in order_type.lower():
                return {
                    "medication_administered": "Morphine 2mg IV",
                    "effect": "Pain decreased from 8/10 to 5/10",
                    "monitoring": "Respiratory status being monitored"
                }
        
        elif intent_type == "provide_status_update":
            vitals = current_state.patient_vitals
            return {
                "vital_signs": {
                    "bp": vitals.bp,
                    "hr": vitals.hr,
                    "rr": vitals.rr,
                    "o2_sat": vitals.o2_sat,
                    "pain_level": vitals.pain_level
                },
                "clinical_notes": [
                    "Patient remains diaphoretic",
                    "Chest pain persistent but slightly improved",
                    "Alert and oriented x3",
                    "No signs of respiratory distress"
                ],
                "interventions_active": [
                    order.order_type for order in current_state.orders_given 
                    if order.status in ["completed", "in_progress"]
                ]
            }
        
        return None
