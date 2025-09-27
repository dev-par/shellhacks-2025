from google.adk.agents import Agent

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

doctor_agent = Agent(
    name="doctor_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    description="Senior Doctor Agent: reviews SBAR reports from trainees and provides structured feedback.",
    instruction=(
        "You are a Senior Doctor. When receiving a trainee SBAR report by the tool 'get_trainee_report', "
        "analyze it carefully, then provide structured feedback in JSON format "
        "indicating approval status, report quality, and feedback message by the tool 'feedback_report'."
    ),
    tools=[get_trainee_report, feedback_report]
)

def get_trainee_report() -> str:
    return coordinator_state["trainee_report"]

def feedback_report(report: str) -> str:
    """
    Tool to provide structured feedback on the trainee SBAR report.
    Returns JSON string:
    {
        "approval": "APPROVED" or "REJECTED",
        "report_quality": "SBAR_GOOD"/"SBAR_BAD",
        "feedback": "Message to trainee"
    }
    """
    passed = "good" in report_text.lower()  # dummy condition
    feedback_json = {
        "approval": "APPROVED" if passed else "REJECTED",
        "report_quality": "SBAR_GOOD" if passed else "SBAR_BAD",
        "feedback": f"Report analysis: {'Looks solid.' if passed else 'Missing key SBAR components.'}"
    }
    return json.dumps(feedback_json)