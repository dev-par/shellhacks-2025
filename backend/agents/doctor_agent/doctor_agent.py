from google.adk.agents import Agent

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

doctor_agent = Agent(
        name="doctor_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="SENIOR DOCTOR AGENT who handles SBAR consultations and grades trainee handovers.",
        instruction="Use the 'get_trainee_report' tool to get the trainee's report. Analyze the report and provide a feedback to the trainee.",
        "Use the 'feedback_report' tool to provide a feedback to the trainee in expected JSON format. Limit the message to 100 words.",
        tools=[get_trainee_report, feedback_report],
)

def get_trainee_report() -> str:
    return coordinator_state["trainee_report"]

def feedback_report(report: str) -> str:
    """
    Provides a feedback to the trainee in expected JSON format.
    The feedback should be in the following format:
    {
        'passed': "True or False",
        "message": "The feedback to the trainee",
    }
    """
    passed = "good" in report_text.lower()  # dummy condition
    feedback_json = {
        "approval": "APPROVED" if passed else "REJECTED",
        "report_quality": "SBAR_GOOD" if passed else "SBAR_BAD",
        "feedback": f"Report analysis: {'Looks solid.' if passed else 'Missing key SBAR components.'}"
    }
    return json.dumps(feedback_json)