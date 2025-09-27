from google.adk.agents import Agent

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"


doctor_agent = Agent(
        name="doctor_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="SENIOR DOCTOR AGENT who handles SBAR consultations and grades trainee handovers.",
        instruction=" Introduce yourself as a senior doctor",
)
