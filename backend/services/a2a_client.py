"""
A2A Client - Agent-to-Agent communication for remote Doctor Agent
"""

import asyncio
import logging
import httpx
from typing import Dict, Any, Optional
from datetime import datetime

from models.scenario import AERTSState, SBARData

logger = logging.getLogger(__name__)

class A2AClient:
    """Client for Agent-to-Agent communication with remote Doctor Agent"""
    
    def __init__(self):
        self.base_url = "https://api.medical-ai.com"  # Placeholder URL
        self.timeout = 30.0
        self.retry_attempts = 3
        
    async def send_sbar_consult(self, sbar_data: Dict[str, Any], 
                              current_state: AERTSState) -> Dict[str, Any]:
        """Send SBAR consultation to remote Doctor Agent"""
        
        # Prepare SBAR payload
        payload = {
            "sbar_data": sbar_data,
            "patient_state": current_state.patient_vitals.dict(),
            "current_phase": current_state.current_state,
            "orders_given": [order.dict() for order in current_state.orders_given],
            "timestamp": datetime.now().isoformat(),
            "consultation_type": "sbar_consultation"
        }
        
        try:
            # In a real implementation, this would make an HTTP request to the remote service
            # For now, we'll simulate the response
            response = await self._simulate_remote_consultation(payload)
            return response
            
        except Exception as e:
            logger.error(f"Error in A2A SBAR consultation: {e}")
            return self._get_fallback_sbar_response()
    
    async def send_handover_request(self, handover_data: Dict[str, Any], 
                                  current_state: AERTSState) -> Dict[str, Any]:
        """Send handover request to remote Senior Doctor Agent"""
        
        # Prepare handover payload
        payload = {
            "handover_data": handover_data,
            "patient_state": current_state.patient_vitals.dict(),
            "current_phase": current_state.current_state,
            "orders_given": [order.dict() for order in current_state.orders_given],
            "timestamp": datetime.now().isoformat(),
            "consultation_type": "senior_handover"
        }
        
        try:
            # In a real implementation, this would make an HTTP request to the remote service
            # For now, we'll simulate the response
            response = await self._simulate_remote_handover(payload)
            return response
            
        except Exception as e:
            logger.error(f"Error in A2A handover request: {e}")
            return self._get_fallback_handover_response()
    
    async def _simulate_remote_consultation(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate remote consultation response"""
        # Simulate network delay
        await asyncio.sleep(1.0)
        
        # Simulate different response scenarios based on SBAR quality
        sbar_data = payload.get("sbar_data", {})
        
        # Check SBAR completeness
        completeness_score = 0
        required_components = ['situation', 'background', 'assessment', 'recommendation']
        
        for component in required_components:
            if component in sbar_data and sbar_data[component]:
                if len(sbar_data[component]) > 20:
                    completeness_score += 25
        
        # Generate response based on completeness
        if completeness_score >= 75:
            return {
                "approval": "APPROVED",
                "reason": "SBAR comprehensive and well-structured. Management plan appropriate.",
                "recommendations": [
                    "Continue current interventions",
                    "Monitor for complications",
                    "Prepare for potential catheterization"
                ],
                "confidence": 0.9,
                "response_time": 1.2
            }
        elif completeness_score >= 50:
            return {
                "approval": "CONDITIONAL_APPROVAL",
                "reason": "SBAR structure good but needs more detail in some areas.",
                "recommendations": [
                    "Provide more specific details in assessment",
                    "Clarify recommendation priorities",
                    "Continue current management"
                ],
                "confidence": 0.7,
                "response_time": 1.5
            }
        else:
            return {
                "approval": "NEEDS_IMPROVEMENT",
                "reason": "SBAR incomplete. Missing key components or insufficient detail.",
                "recommendations": [
                    "Restructure SBAR with all four components",
                    "Provide more clinical detail",
                    "Clarify current patient status"
                ],
                "confidence": 0.5,
                "response_time": 2.0
            }
    
    async def _simulate_remote_handover(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate remote handover response"""
        # Simulate network delay
        await asyncio.sleep(1.5)
        
        # Simulate handover evaluation
        handover_data = payload.get("handover_data", {})
        
        # Check handover completeness
        completeness_score = 0
        required_fields = ['patient_summary', 'current_status', 'interventions_performed']
        
        for field in required_fields:
            if field in handover_data and handover_data[field]:
                completeness_score += 33
        
        # Generate response based on completeness
        if completeness_score >= 80:
            return {
                "approval": "APPROVED",
                "feedback": "Excellent handover. Clear, comprehensive, and well-structured.",
                "quality_score": 90,
                "recommendations": [
                    "Continue current management",
                    "Monitor closely for changes",
                    "Good work on the handover"
                ],
                "response_time": 1.8
            }
        elif completeness_score >= 60:
            return {
                "approval": "GOOD",
                "feedback": "Good handover overall. Minor improvements needed.",
                "quality_score": 75,
                "recommendations": [
                    "Include more specific details",
                    "Clarify pending actions",
                    "Continue current management"
                ],
                "response_time": 2.2
            }
        else:
            return {
                "approval": "NEEDS_IMPROVEMENT",
                "feedback": "Handover needs work. Missing key information.",
                "quality_score": 55,
                "recommendations": [
                    "Restructure handover report",
                    "Include all essential information",
                    "Practice handover format"
                ],
                "response_time": 2.5
            }
    
    def _get_fallback_sbar_response(self) -> Dict[str, Any]:
        """Fallback SBAR response when remote service fails"""
        return {
            "approval": "APPROVED",
            "reason": "SBAR consultation completed (offline mode)",
            "recommendations": [
                "Continue current management",
                "Monitor patient closely",
                "Prepare for potential interventions"
            ],
            "confidence": 0.8,
            "response_time": 0.5,
            "offline_mode": True
        }
    
    def _get_fallback_handover_response(self) -> Dict[str, Any]:
        """Fallback handover response when remote service fails"""
        return {
            "approval": "APPROVED",
            "feedback": "Handover completed (offline mode)",
            "quality_score": 80,
            "recommendations": [
                "Continue current management",
                "Monitor patient status",
                "Good work on the handover"
            ],
            "response_time": 0.5,
            "offline_mode": True
        }
    
    async def health_check(self) -> bool:
        """Check if remote A2A service is available"""
        try:
            # In a real implementation, this would ping the remote service
            # For now, we'll simulate a health check
            await asyncio.sleep(0.1)
            return True
        except Exception as e:
            logger.error(f"A2A service health check failed: {e}")
            return False
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Get A2A service status"""
        is_healthy = await self.health_check()
        
        return {
            "service_name": "A2A Doctor Agent",
            "base_url": self.base_url,
            "is_healthy": is_healthy,
            "last_check": datetime.now().isoformat(),
            "features": [
                "sbar_consultation",
                "senior_handover",
                "clinical_evaluation"
            ]
        }
