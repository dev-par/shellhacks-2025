from google.adk import Agent





nurse_agent = Agent(
    name="nurse_agent",
    description="A nurse agent that can help with patient care",
    model="gemini-2.0-flash",
)


root_agent = nurse_agent