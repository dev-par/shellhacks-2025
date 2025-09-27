"""
Doctor Agent - Handles SBAR consultation and Senior Doctor handover
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from models.scenario import AERTSState, CoordinatorIntent, DoctorResponse, SBARData, HandoverData
from services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class DoctorAgent:
    """Doctor Agent for SBAR consultation and Senior Doctor handover"""
    
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.name = "Dr. Johnson"
        self.specialty = "Emergency Medicine"
        self.role = "Attending Physician"
        
    async def process_intent(self, intent: CoordinatorIntent, current_state: AERTSState) -> DoctorResponse:
        """Process intent from Coordinator"""
        if not intent:
            return DoctorResponse(
                text="",
                timestamp=datetime.now()
            )
        
        intent_type = intent.intent_type
        data = intent.data
        
        if intent_type == "sbar_consultation":
            return await self._process_sbar_consultation(data, current_state)
        elif intent_type == "senior_handover":
            return await self._process_senior_handover(data, current_state)
        else:
            return DoctorResponse(
                text="I'm here to assist with the case.",
                timestamp=datetime.now()
            )
    
    async def _process_sbar_consultation(self, data: Dict[str, Any], 
                                       current_state: AERTSState) -> DoctorResponse:
        """Process SBAR consultation request"""
        
        # Build SBAR data from current state
        sbar_data = self._build_sbar_data(current_state)
        
        # Generate Doctor response using Gemini
        response_text = await self._generate_sbar_response(sbar_data, current_state)
        
        # Determine approval status
        approval_status = await self._evaluate_sbar_quality(sbar_data, current_state)
        
        return DoctorResponse(
            text=response_text,
            timestamp=datetime.now(),
            approval_status=approval_status["status"],
            feedback=approval_status["feedback"],
            structured_data={
                "sbar_data": sbar_data.dict(),
                "approval": approval_status["status"],
                "recommendations": approval_status["recommendations"]
            }
        )
    
    def _build_sbar_data(self, current_state: AERTSState) -> SBARData:
        """Build SBAR data from current state"""
        vitals = current_state.patient_vitals
        
        # Situation
        situation = f"55-year-old male with crushing substernal chest pain, 8/10, diaphoretic. Vitals: BP {vitals.bp}, HR {vitals.hr}, O2 Sat {vitals.o2_sat}%"
        
        # Background
        background = "No known cardiac history. Patient arrived via EMS with acute onset chest pain. No allergies known."
        
        # Assessment
        assessment = f"High suspicion for STEMI based on presentation. Pain level {vitals.pain_level}/10, diaphoretic. ECG ordered and pending."
        
        # Recommendation
        orders_summary = [order.order_type for order in current_state.orders_given]
        recommendation = f"Continue current interventions: {', '.join(orders_summary)}. Prepare for potential catheterization. Monitor closely for complications."
        
        return SBARData(
            situation=situation,
            background=background,
            assessment=assessment,
            recommendation=recommendation,
            timestamp=datetime.now()
        )
    
    async def _generate_sbar_response(self, sbar_data: SBARData, 
                                    current_state: AERTSState) -> str:
        """Generate Doctor response to SBAR consultation"""
        
        context = {
            "sbar_data": sbar_data.dict(),
            "current_state": current_state.current_state,
            "orders_given": [order.dict() for order in current_state.orders_given],
            "doctor_name": self.name,
            "doctor_role": self.role
        }
        
        prompt = f"""You are {self.name}, an attending emergency physician receiving an SBAR report from a trainee.

SBAR Report:
Situation: {sbar_data.situation}
Background: {sbar_data.background}
Assessment: {sbar_data.assessment}
Recommendation: {sbar_data.recommendation}

Current interventions: {', '.join([order.order_type for order in current_state.orders_given])}

Respond as an attending physician would:
1. Acknowledge the SBAR report
2. Provide feedback on the quality
3. Give approval or request clarification
4. Provide additional guidance if needed

Keep response professional but concise.
"""
        
        try:
            response = await self.gemini_service.generate_doctor_response(prompt, context)
            return response
        except Exception as e:
            logger.error(f"Error generating doctor response: {e}")
            return self._get_fallback_sbar_response(sbar_data)
    
    def _get_fallback_sbar_response(self, sbar_data: SBARData) -> str:
        """Fallback SBAR response if Gemini fails"""
        return f"""Thank you for the SBAR report. 

Situation: {sbar_data.situation}
Background: {sbar_data.background}
Assessment: {sbar_data.assessment}
Recommendation: {sbar_data.recommendation}

Good work on the SBAR structure. I approve the current management plan. Continue monitoring and prepare for potential catheterization. Let me know if there are any changes in the patient's condition."""
    
    async def _evaluate_sbar_quality(self, sbar_data: SBARData, 
                                   current_state: AERTSState) -> Dict[str, Any]:
        """Evaluate SBAR quality and determine approval"""
        
        # Check SBAR completeness
        completeness_score = 0
        feedback_parts = []
        
        if sbar_data.situation and len(sbar_data.situation) > 20:
            completeness_score += 25
        else:
            feedback_parts.append("Situation could be more detailed")
        
        if sbar_data.background and len(sbar_data.background) > 20:
            completeness_score += 25
        else:
            feedback_parts.append("Background needs more context")
        
        if sbar_data.assessment and len(sbar_data.assessment) > 20:
            completeness_score += 25
        else:
            feedback_parts.append("Assessment could be more comprehensive")
        
        if sbar_data.recommendation and len(sbar_data.recommendation) > 20:
            completeness_score += 25
        else:
            feedback_parts.append("Recommendation needs more specificity")
        
        # Determine approval
        if completeness_score >= 75:
            status = "APPROVED"
            feedback = "Excellent SBAR report. Clear and comprehensive."
        elif completeness_score >= 50:
            status = "CONDITIONAL_APPROVAL"
            feedback = f"Good SBAR structure. Areas for improvement: {', '.join(feedback_parts)}"
        else:
            status = "NEEDS_IMPROVEMENT"
            feedback = f"SBAR needs work. Issues: {', '.join(feedback_parts)}"
        
        return {
            "status": status,
            "feedback": feedback,
            "completeness_score": completeness_score,
            "recommendations": feedback_parts
        }
    
    async def process_handover(self, handover_data: Dict[str, Any], 
                             current_state: AERTSState) -> DoctorResponse:
        """Process Senior Doctor handover"""
        
        # Generate Senior Doctor response
        response_text = await self._generate_handover_response(handover_data, current_state)
        
        # Evaluate handover quality
        evaluation = await self._evaluate_handover_quality(handover_data, current_state)
        
        return DoctorResponse(
            text=response_text,
            timestamp=datetime.now(),
            approval_status=evaluation["status"],
            feedback=evaluation["feedback"],
            structured_data=evaluation
        )
    
    async def _generate_handover_response(self, handover_data: Dict[str, Any], 
                                        current_state: AERTSState) -> str:
        """Generate Senior Doctor handover response"""
        
        context = {
            "handover_data": handover_data,
            "current_state": current_state.current_state,
            "patient_vitals": current_state.patient_vitals.dict(),
            "orders_given": [order.dict() for order in current_state.orders_given],
            "doctor_name": self.name,
            "doctor_role": "Senior Attending Physician"
        }
        
        prompt = f"""You are {self.name}, a senior attending physician receiving a handover report from a trainee.

Handover Report:
{handover_data.get('patient_summary', 'No summary provided')}

Current Status:
{handover_data.get('current_status', 'No status provided')}

Interventions Performed:
{', '.join(handover_data.get('interventions_performed', []))}

Pending Actions:
{', '.join(handover_data.get('pending_actions', []))}

Critical Concerns:
{', '.join(handover_data.get('critical_concerns', []))}

Respond as a senior attending physician would:
1. Acknowledge the handover
2. Ask clarifying questions if needed
3. Provide feedback on the handover quality
4. Give approval and take over the case
5. Provide any additional guidance

Keep response professional and supportive.
"""
        
        try:
            response = await self.gemini_service.generate_doctor_response(prompt, context)
            return response
        except Exception as e:
            logger.error(f"Error generating handover response: {e}")
            return self._get_fallback_handover_response(handover_data)
    
    def _get_fallback_handover_response(self, handover_data: Dict[str, Any]) -> str:
        """Fallback handover response if Gemini fails"""
        return f"""Thank you for the handover report. 

I understand the situation: {handover_data.get('patient_summary', 'No summary provided')}

Current status: {handover_data.get('current_status', 'No status provided')}

I can see you've performed: {', '.join(handover_data.get('interventions_performed', []))}

Good work on the handover. I'll take over from here. Continue monitoring and let me know if there are any changes."""
    
    async def _evaluate_handover_quality(self, handover_data: Dict[str, Any], 
                                       current_state: AERTSState) -> Dict[str, Any]:
        """Evaluate handover quality"""
        
        # Check handover completeness
        completeness_score = 0
        feedback_parts = []
        
        required_fields = ['patient_summary', 'current_status', 'interventions_performed']
        
        for field in required_fields:
            if field in handover_data and handover_data[field]:
                completeness_score += 33
            else:
                feedback_parts.append(f"Missing or incomplete {field}")
        
        # Check if interventions are mentioned
        if 'interventions_performed' in handover_data:
            interventions = handover_data['interventions_performed']
            if len(interventions) >= 3:  # Expect at least 3 interventions
                completeness_score += 10
            else:
                feedback_parts.append("Should mention more interventions performed")
        
        # Determine overall quality
        if completeness_score >= 80:
            status = "EXCELLENT"
            feedback = "Outstanding handover. Clear, comprehensive, and well-structured."
        elif completeness_score >= 60:
            status = "GOOD"
            feedback = f"Good handover. Minor improvements needed: {', '.join(feedback_parts)}"
        else:
            status = "NEEDS_IMPROVEMENT"
            feedback = f"Handover needs work. Issues: {', '.join(feedback_parts)}"
        
        return {
            "status": status,
            "feedback": feedback,
            "completeness_score": completeness_score,
            "recommendations": feedback_parts,
            "overall_quality": completeness_score
        }
