import re
from google.adk.agents import Agent

from google.adk.agents import Agent
import json

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

def feedback_report(report: str) -> dict:
    """
    Ask the LLM to analyze the freeform SBAR report and return JSON.
    """
    # The LLM prompt: we give it the trainee report and instructions
    # This is what the agent will see via tools
    prompt = f"""
    You are a senior doctor reviewing a trainee's SBAR report.
    The report is:

    \"\"\"{report}\"\"\"

    Instructions:
    - Only reject if the report is not a valid SBAR (missing situation, background, assessment, recommendation).
    - Determine report_quality: SBAR_GOOD or SBAR_BAD.
    - Return JSON with keys: approval, report_quality, feedback.
    - Feedback should be polite and concise. Like 'Can you please elaborate on the situation?' or 'Thank you for the report.'
    """

    return {"llm_prompt": prompt}
# If ADK accepts raw functions, this is fine:
doctor_agent = Agent(
    name="doctor_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    description="Senior Doctor Agent: reviews SBAR reports from trainees and provides structured feedback.",
    instruction=(
        "You are 'Dr. Wang' — a senior doctor: blunt, direct, mentor energy. Be constructive, never mean. Make "
        "Task: When a trainee sends you a message, treat that message as their SBAR report. "
        "Analyze the report carefully and provide structured feedback using the 'feedback_report' tool. "
        "The feedback should be in JSON format indicating approval status, report quality, and feedback message."
    ),
    tools=[feedback_report]
)