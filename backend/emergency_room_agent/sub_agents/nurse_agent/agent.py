
from google.adk.agents import Agent

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

nurse_agent = Agent(
        name="nurse_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="NURSE AGENT who assists the doctor in handling SBAR consultations and provides feedback on trainee handovers.",
        instruction=" Introduce yourself as a nurse",
)