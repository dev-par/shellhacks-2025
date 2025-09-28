from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import json

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

def feedback_report(report: str) -> dict:
    """
    Analyze SBAR report and provide structured feedback.
    """
    # Simple analysis - in a real implementation, this would use LLM
    if len(report) < 50:
        return {
            "approval": "SBAR_NEEDS_WORK",
            "report_quality": "SBAR_BAD", 
            "feedback": "Please provide more detailed information in your SBAR report."
        }
    
    # Check for key SBAR components
    report_lower = report.lower()
    has_situation = any(word in report_lower for word in ["situation", "patient", "current"])
    has_background = any(word in report_lower for word in ["background", "history", "previous"])
    has_assessment = any(word in report_lower for word in ["assessment", "diagnosis", "evaluation"])
    has_recommendation = any(word in report_lower for word in ["recommendation", "suggest", "recommend"])
    
    if has_situation and has_background and has_assessment and has_recommendation:
        return {
            "approval": "APPROVED",
            "report_quality": "SBAR_GOOD",
            "feedback": "Excellent SBAR report. All components present and well-structured."
        }
    else:
        missing = []
        if not has_situation: missing.append("Situation")
        if not has_background: missing.append("Background") 
        if not has_assessment: missing.append("Assessment")
        if not has_recommendation: missing.append("Recommendation")
        
        return {
            "approval": "SBAR_NEEDS_WORK",
            "report_quality": "SBAR_BAD",
            "feedback": f"Please include: {', '.join(missing)}"
        }

doctor_agent = Agent(
    name="doctor_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    description="Senior Doctor Agent: reviews SBAR reports from trainees and provides structured feedback.",
    instruction="""You are Dr. Wang, a senior emergency medicine physician with 20 years of experience.
    You're reviewing trainee SBAR reports and providing constructive feedback.
    
    When a trainee sends you a message, treat it as their SBAR report.
    Use the feedback_report tool to analyze the report and provide structured feedback.
    Be direct but constructive in your feedback.

    Patient information contains much of the basic information about the patient: {patient_information}
    """,
    tools=[FunctionTool(feedback_report)]
)