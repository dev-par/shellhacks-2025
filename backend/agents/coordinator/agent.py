import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent



root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_current_time],
)

def get_current_time(city: str) -> dict:
    

    tz_identifier = "America/New_York"
   

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    currenttime = {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}
    
    return {"status": "success", "currentime": currenttime}
