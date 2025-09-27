"""
Evaluator Agent - Generates final debrief and performance evaluation
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from models.scenario import AERTSState, EvaluationResult
from services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class EvaluatorAgent:
    """Evaluator Agent for final debrief and performance assessment"""
    
    def __init__(self):
        self.evaluation_criteria = {
            "sbar_completeness": 0.25,
            "clinical_accuracy": 0.25,
            "communication_quality": 0.20,
            "timing_efficiency": 0.15,
            "safety_awareness": 0.15
        }
    
    async def evaluate_handover(self, handover_data: Dict[str, Any], 
                              current_state: AERTSState) -> EvaluationResult:
        """Evaluate handover quality"""
        
        # Calculate individual scores
        sbar_score = self._evaluate_sbar_completeness(handover_data)
        clinical_score = self._evaluate_clinical_accuracy(current_state)
        communication_score = self._evaluate_communication_quality(handover_data)
        timing_score = self._evaluate_timing_efficiency(current_state)
        safety_score = self._evaluate_safety_awareness(current_state)
        
        # Calculate weighted overall score
        overall_score = (
            sbar_score * self.evaluation_criteria["sbar_completeness"] +
            clinical_score * self.evaluation_criteria["clinical_accuracy"] +
            communication_score * self.evaluation_criteria["communication_quality"] +
            timing_score * self.evaluation_criteria["timing_efficiency"] +
            safety_score * self.evaluation_criteria["safety_awareness"]
        )
        
        # Generate feedback
        feedback = self._generate_feedback(
            sbar_score, clinical_score, communication_score, 
            timing_score, safety_score, current_state
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            sbar_score, clinical_score, communication_score, 
            timing_score, safety_score
        )
        
        return EvaluationResult(
            overall_score=overall_score,
            sbar_completeness=sbar_score,
            clinical_accuracy=clinical_score,
            communication_quality=communication_score,
            timing_efficiency=timing_score,
            feedback=feedback,
            recommendations=recommendations,
            timestamp=datetime.now()
        )
    
    def _evaluate_sbar_completeness(self, handover_data: Dict[str, Any]) -> float:
        """Evaluate SBAR completeness in handover"""
        score = 0.0
        
        # Check for required SBAR components
        required_components = ['patient_summary', 'current_status', 'interventions_performed']
        
        for component in required_components:
            if component in handover_data and handover_data[component]:
                if isinstance(handover_data[component], str) and len(handover_data[component]) > 20:
                    score += 25
                elif isinstance(handover_data[component], list) and len(handover_data[component]) > 0:
                    score += 25
        
        # Check for additional quality indicators
        if 'critical_concerns' in handover_data and handover_data['critical_concerns']:
            score += 10
        
        if 'pending_actions' in handover_data and handover_data['pending_actions']:
            score += 10
        
        return min(score, 100.0)
    
    def _evaluate_clinical_accuracy(self, current_state: AERTSState) -> float:
        """Evaluate clinical accuracy of interventions"""
        score = 0.0
        
        # Check for essential STEMI interventions
        essential_interventions = [
            "Aspirin 325mg",
            "12-lead ECG",
            "IV Access",
            "Oxygen Therapy"
        ]
        
        completed_interventions = [order.order_type for order in current_state.orders_given 
                                 if order.status == "completed"]
        
        # Score based on essential interventions completed
        for intervention in essential_interventions:
            if any(intervention.lower() in order.lower() for order in completed_interventions):
                score += 20
        
        # Bonus points for additional appropriate interventions
        additional_interventions = [
            "Nitroglycerin",
            "Morphine",
            "Cardiology consult"
        ]
        
        for intervention in additional_interventions:
            if any(intervention.lower() in order.lower() for order in completed_interventions):
                score += 5
        
        return min(score, 100.0)
    
    def _evaluate_communication_quality(self, handover_data: Dict[str, Any]) -> float:
        """Evaluate communication quality"""
        score = 50.0  # Base score
        
        # Check for clear, structured communication
        if 'patient_summary' in handover_data:
            summary = handover_data['patient_summary']
            if len(summary) > 50:  # Detailed summary
                score += 20
            if any(word in summary.lower() for word in ['chest pain', 'stemi', 'cardiac']):
                score += 10  # Medical terminology used
        
        if 'current_status' in handover_data:
            status = handover_data['current_status']
            if len(status) > 30:  # Detailed status
                score += 20
        
        return min(score, 100.0)
    
    def _evaluate_timing_efficiency(self, current_state: AERTSState) -> float:
        """Evaluate timing efficiency"""
        if not current_state.start_time:
            return 50.0
        
        elapsed_time = (datetime.now() - current_state.start_time).total_seconds()
        
        # Ideal timing for STEMI protocol
        ideal_times = {
            "ecg_ordered": 60,  # 1 minute
            "asa_administered": 120,  # 2 minutes
            "iv_access": 180,  # 3 minutes
            "sbar_consulted": 300  # 5 minutes
        }
        
        score = 100.0
        
        # Check timing of key interventions
        for order in current_state.orders_given:
            order_time = (order.timestamp - current_state.start_time).total_seconds()
            
            if "ECG" in order.order_type:
                if order_time > ideal_times["ecg_ordered"]:
                    score -= 20
            elif "Aspirin" in order.order_type:
                if order_time > ideal_times["asa_administered"]:
                    score -= 20
            elif "IV" in order.order_type:
                if order_time > ideal_times["iv_access"]:
                    score -= 15
        
        # Check overall completion time
        if elapsed_time > 600:  # 10 minutes
            score -= 10
        
        return max(score, 0.0)
    
    def _evaluate_safety_awareness(self, current_state: AERTSState) -> float:
        """Evaluate safety awareness"""
        score = 100.0
        
        # Deduct points for clinical warnings
        score -= len(current_state.clinical_warnings) * 10
        
        # Check for appropriate safety considerations
        vitals = current_state.patient_vitals
        
        # Check if nitro was given with appropriate BP
        if current_state.nitro_ordered:
            systolic_bp = int(vitals.bp.split('/')[0])
            if systolic_bp < 100:
                score -= 30  # Major safety issue
        
        # Check if morphine was given with appropriate RR
        if current_state.morphine_ordered:
            if vitals.rr < 12:
                score -= 30  # Major safety issue
        
        return max(score, 0.0)
    
    def _generate_feedback(self, sbar_score: float, clinical_score: float, 
                          communication_score: float, timing_score: float, 
                          safety_score: float, current_state: AERTSState) -> str:
        """Generate comprehensive feedback"""
        feedback_parts = []
        
        # Overall performance
        overall_score = (
            sbar_score * self.evaluation_criteria["sbar_completeness"] +
            clinical_score * self.evaluation_criteria["clinical_accuracy"] +
            communication_score * self.evaluation_criteria["communication_quality"] +
            timing_score * self.evaluation_criteria["timing_efficiency"] +
            safety_score * self.evaluation_criteria["safety_awareness"]
        )
        
        if overall_score >= 90:
            feedback_parts.append("Outstanding performance! You demonstrated excellent clinical judgment and communication skills.")
        elif overall_score >= 80:
            feedback_parts.append("Very good performance with room for minor improvements.")
        elif overall_score >= 70:
            feedback_parts.append("Good performance overall, but several areas need attention.")
        else:
            feedback_parts.append("Performance needs significant improvement. Focus on the areas highlighted below.")
        
        # Specific feedback
        if sbar_score < 70:
            feedback_parts.append("SBAR structure needs work - ensure all components (Situation, Background, Assessment, Recommendation) are clearly addressed.")
        
        if clinical_score < 70:
            feedback_parts.append("Clinical accuracy needs improvement - review STEMI protocol and essential interventions.")
        
        if communication_score < 70:
            feedback_parts.append("Communication could be clearer and more structured.")
        
        if timing_score < 70:
            feedback_parts.append("Timing efficiency needs improvement - remember that time is muscle in STEMI cases.")
        
        if safety_score < 70:
            feedback_parts.append("Safety awareness needs improvement - always consider contraindications before ordering medications.")
        
        return " ".join(feedback_parts)
    
    def _generate_recommendations(self, sbar_score: float, clinical_score: float, 
                                 communication_score: float, timing_score: float, 
                                 safety_score: float) -> List[str]:
        """Generate specific recommendations for improvement"""
        recommendations = []
        
        if sbar_score < 80:
            recommendations.extend([
                "Practice SBAR structure with case studies",
                "Use SBAR templates for consistency",
                "Ensure all four components are addressed"
            ])
        
        if clinical_score < 80:
            recommendations.extend([
                "Review STEMI treatment protocols",
                "Memorize essential interventions (MONA)",
                "Practice clinical decision-making scenarios"
            ])
        
        if communication_score < 80:
            recommendations.extend([
                "Practice clear, concise communication",
                "Use medical terminology appropriately",
                "Structure reports logically"
            ])
        
        if timing_score < 80:
            recommendations.extend([
                "Practice time management in high-pressure situations",
                "Memorize critical timing requirements",
                "Use checklists to ensure efficiency"
            ])
        
        if safety_score < 80:
            recommendations.extend([
                "Review medication contraindications",
                "Always check vitals before ordering medications",
                "Practice safety checks before interventions"
            ])
        
        return recommendations
    
    async def generate_final_debrief(self, current_state: AERTSState) -> Dict[str, Any]:
        """Generate final debrief report"""
        
        # Calculate final scores
        total_orders = len(current_state.orders_given)
        completed_orders = len([o for o in current_state.orders_given if o.status == "completed"])
        completion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0
        
        # Calculate timing
        total_time = (datetime.now() - current_state.start_time).total_seconds()
        
        # Generate performance summary
        performance_summary = self._generate_performance_summary(current_state)
        
        # Generate key achievements
        achievements = self._generate_achievements(current_state)
        
        # Generate areas for improvement
        improvements = self._generate_improvement_areas(current_state)
        
        return {
            "session_summary": {
                "total_time_minutes": round(total_time / 60, 1),
                "orders_given": total_orders,
                "orders_completed": completed_orders,
                "completion_rate": round(completion_rate, 1),
                "state_transitions": len(current_state.state_transitions),
                "clinical_warnings": len(current_state.clinical_warnings)
            },
            "performance_summary": performance_summary,
            "achievements": achievements,
            "improvements": improvements,
            "final_state": current_state.current_state,
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_performance_summary(self, current_state: AERTSState) -> Dict[str, Any]:
        """Generate performance summary"""
        return {
            "overall_rating": "Good" if len(current_state.orders_given) >= 5 else "Needs Improvement",
            "clinical_competence": "Demonstrated" if current_state.asa_administered and current_state.ecg_ordered else "Needs Work",
            "communication_skills": "Effective" if current_state.sbar_consulted else "Needs Practice",
            "safety_awareness": "Good" if len(current_state.clinical_warnings) == 0 else "Needs Attention"
        }
    
    def _generate_achievements(self, current_state: AERTSState) -> List[str]:
        """Generate list of achievements"""
        achievements = []
        
        if current_state.asa_administered:
            achievements.append("✓ Administered aspirin promptly")
        
        if current_state.ecg_ordered:
            achievements.append("✓ Ordered ECG immediately")
        
        if current_state.iv_access:
            achievements.append("✓ Established IV access")
        
        if current_state.sbar_consulted:
            achievements.append("✓ Completed SBAR consultation")
        
        if current_state.senior_handover_completed:
            achievements.append("✓ Completed senior handover")
        
        if len(current_state.orders_given) >= 5:
            achievements.append("✓ Demonstrated comprehensive care")
        
        return achievements
    
    def _generate_improvement_areas(self, current_state: AERTSState) -> List[str]:
        """Generate areas for improvement"""
        improvements = []
        
        if not current_state.asa_administered:
            improvements.append("Administer aspirin immediately upon arrival")
        
        if not current_state.ecg_ordered:
            improvements.append("Order ECG as first priority")
        
        if not current_state.iv_access:
            improvements.append("Establish IV access early")
        
        if not current_state.sbar_consulted:
            improvements.append("Practice SBAR communication")
        
        if len(current_state.clinical_warnings) > 0:
            improvements.append("Review medication contraindications")
        
        if len(current_state.orders_given) < 5:
            improvements.append("Consider additional appropriate interventions")
        
        return improvements
