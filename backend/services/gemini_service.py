"""
Gemini Service - Integration with Google's Gemini AI for dynamic responses
"""

import asyncio
import logging
from typing import Dict, Any, Optional
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("Google Generative AI not available. Using mock responses.")

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for Gemini AI integration"""
    
    def __init__(self):
        self.model = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize Gemini service"""
        if not GEMINI_AVAILABLE:
            logger.warning("Gemini not available, using mock responses")
            self.is_initialized = True
            return
        
        try:
            # Configure Gemini
            genai.configure(api_key="your-api-key-here")  # Replace with actual API key
            
            # Initialize model
            self.model = genai.GenerativeModel('gemini-pro')
            self.is_initialized = True
            logger.info("Gemini service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            self.is_initialized = False
    
    async def generate_nurse_response(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate nurse response using Gemini"""
        if not self.is_initialized or not self.model:
            return self._get_mock_nurse_response(context)
        
        try:
            # Add context to prompt
            full_prompt = f"""
            Context: {json.dumps(context, indent=2)}
            
            {prompt}
            
            Respond as an experienced emergency department nurse. Keep response concise (1-2 sentences) and professional.
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content, full_prompt
            )
            
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error generating nurse response: {e}")
            return self._get_mock_nurse_response(context)
    
    async def generate_doctor_response(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate doctor response using Gemini"""
        if not self.is_initialized or not self.model:
            return self._get_mock_doctor_response(context)
        
        try:
            # Add context to prompt
            full_prompt = f"""
            Context: {json.dumps(context, indent=2)}
            
            {prompt}
            
            Respond as an experienced emergency medicine attending physician. Keep response professional and authoritative.
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content, full_prompt
            )
            
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error generating doctor response: {e}")
            return self._get_mock_doctor_response(context)
    
    def _get_mock_nurse_response(self, context: Dict[str, Any]) -> str:
        """Mock nurse response when Gemini is not available"""
        intent_type = context.get("intent_type", "unknown")
        
        mock_responses = {
            "acknowledge_order": [
                "Understood, Doctor. I'll carry out that order right away.",
                "Copy that. I'm on it now.",
                "Right away, Doctor. I'll get that done.",
                "I'll take care of that immediately."
            ],
            "provide_status_update": [
                "Patient is stable but still complaining of chest pain. Vitals are as reported.",
                "Current status: Patient remains diaphoretic, pain level 7/10. All vitals stable.",
                "Patient is alert and oriented. Chest pain persistent but slightly improved.",
                "Status update: Patient stable, IV running well, oxygen tolerated."
            ],
            "clinical_warning": [
                "I have a concern about that order. Should we reconsider?",
                "Hold on, Doctor. There might be a contraindication here.",
                "I'm not sure about that order given the current vitals. What do you think?",
                "Should we double-check that before proceeding?"
            ],
            "default": [
                "I'm here and ready to assist, Doctor.",
                "What would you like me to do next?",
                "I'm monitoring the patient closely.",
                "Ready for your next order, Doctor."
            ]
        }
        
        import random
        responses = mock_responses.get(intent_type, mock_responses["default"])
        return random.choice(responses)
    
    def _get_mock_doctor_response(self, context: Dict[str, Any]) -> str:
        """Mock doctor response when Gemini is not available"""
        intent_type = context.get("intent_type", "unknown")
        
        if "sbar" in intent_type.lower():
            return """Thank you for the SBAR report. 

Situation: 55-year-old male with chest pain
Background: No known cardiac history
Assessment: High suspicion for STEMI
Recommendation: Continue current management, prepare for catheterization

Good work on the SBAR structure. I approve the current management plan. Continue monitoring and let me know if there are any changes."""
        
        elif "handover" in intent_type.lower():
            return """Thank you for the handover report. 

I understand the situation and current status. I can see you've performed the essential interventions.

Good work on the handover. I'll take over from here. Continue monitoring and let me know if there are any changes."""
        
        else:
            return "I'm here to assist with the case. What do you need?"
    
    async def evaluate_sbar_quality(self, sbar_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate SBAR quality using Gemini"""
        if not self.is_initialized or not self.model:
            return self._get_mock_sbar_evaluation(sbar_data)
        
        try:
            prompt = f"""
            Evaluate this SBAR report for completeness and quality:
            
            Situation: {sbar_data.get('situation', 'Not provided')}
            Background: {sbar_data.get('background', 'Not provided')}
            Assessment: {sbar_data.get('assessment', 'Not provided')}
            Recommendation: {sbar_data.get('recommendation', 'Not provided')}
            
            Rate each component (0-100) and provide overall feedback.
            Return JSON format: {{"situation_score": X, "background_score": Y, "assessment_score": Z, "recommendation_score": W, "overall_score": A, "feedback": "text"}}
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            
            # Try to parse JSON response
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return self._get_mock_sbar_evaluation(sbar_data)
                
        except Exception as e:
            logger.error(f"Error evaluating SBAR: {e}")
            return self._get_mock_sbar_evaluation(sbar_data)
    
    def _get_mock_sbar_evaluation(self, sbar_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock SBAR evaluation when Gemini is not available"""
        # Simple scoring based on content length and keywords
        scores = {}
        
        for component in ['situation', 'background', 'assessment', 'recommendation']:
            content = sbar_data.get(component, '')
            if len(content) > 50:
                scores[f"{component}_score"] = 85
            elif len(content) > 20:
                scores[f"{component}_score"] = 70
            else:
                scores[f"{component}_score"] = 50
        
        overall_score = sum(scores.values()) / len(scores)
        
        if overall_score >= 80:
            feedback = "Excellent SBAR report. Clear and comprehensive."
        elif overall_score >= 70:
            feedback = "Good SBAR structure. Minor improvements needed."
        else:
            feedback = "SBAR needs work. Ensure all components are addressed."
        
        return {
            **scores,
            "overall_score": overall_score,
            "feedback": feedback
        }
    
    async def evaluate_handover_quality(self, handover_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate handover quality using Gemini"""
        if not self.is_initialized or not self.model:
            return self._get_mock_handover_evaluation(handover_data)
        
        try:
            prompt = f"""
            Evaluate this handover report for completeness and quality:
            
            Patient Summary: {handover_data.get('patient_summary', 'Not provided')}
            Current Status: {handover_data.get('current_status', 'Not provided')}
            Interventions Performed: {handover_data.get('interventions_performed', [])}
            Pending Actions: {handover_data.get('pending_actions', [])}
            Critical Concerns: {handover_data.get('critical_concerns', [])}
            
            Rate the handover quality (0-100) and provide feedback.
            Return JSON format: {{"overall_score": X, "completeness_score": Y, "clarity_score": Z, "feedback": "text"}}
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            
            # Try to parse JSON response
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return self._get_mock_handover_evaluation(handover_data)
                
        except Exception as e:
            logger.error(f"Error evaluating handover: {e}")
            return self._get_mock_handover_evaluation(handover_data)
    
    def _get_mock_handover_evaluation(self, handover_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock handover evaluation when Gemini is not available"""
        # Simple scoring based on content completeness
        completeness_score = 0
        
        required_fields = ['patient_summary', 'current_status', 'interventions_performed']
        for field in required_fields:
            if field in handover_data and handover_data[field]:
                completeness_score += 33
        
        overall_score = min(completeness_score, 100)
        
        if overall_score >= 80:
            feedback = "Excellent handover. Clear and comprehensive."
        elif overall_score >= 60:
            feedback = "Good handover. Minor improvements needed."
        else:
            feedback = "Handover needs work. Ensure all key information is included."
        
        return {
            "overall_score": overall_score,
            "completeness_score": completeness_score,
            "clarity_score": overall_score,
            "feedback": feedback
        }
