import asyncio
import uuid
import json

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from emergency_room_agent import root_agent as emergency_room_agent
from utils import call_agent_async_json

load_dotenv()

# Create a new session service to store state
session_service_stateful = InMemorySessionService()

initial_state = {
    "states": {
        'current_stage': 0,
        'stages': ['S0_INITIAL_STABILIZATION', 'S1_DIAGNOSTIC_CONFIRMATION', 'S2_CRITICAL_CONSULTATION', 'S3_SENIOR_HANDOVER', 'S4_DEBRIEFING']
    },
    "patient_information": {
        "patient_name": "Brandon Hancock",
        "patient_age": 55,
        "static_patient_data": {
        "vitals_snapshot": {
            "BP_Systolic": 118,
            "BP_Diastolic": 75,
            "HR": 105,
            "O2_Sat": 94,
            "O2_Source": "Room Air",
            "Pain_Score": 8
        },
        "history": {
            "Age_Sex": "55-year-old male",
            "Complaint": "Crushing substernal chest pain",
            "Known_History": "Hypertension, Smoker",
            "Allergies": "None known"
        }
        }
    },
    "session_flags": {
        "protocol_asa_given": False,
        "protocol_ecg_ordered": False,
        "protocol_diagnosis_confirmed": False,
        "protocol_nitro_or_morphine": False
    }
}

async def main():

    # Create a NEW session
    APP_NAME = "Brandon Bot"
    USER_ID = "brandon_hancock"
    SESSION_ID = str(uuid.uuid4())
    initial_state["session_id"] = SESSION_ID


    stateful_session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )
    runner = Runner(
        agent=emergency_room_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )

    while True:
        # Get user input
        user_input = input("You: ")

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            break

        # Process the user query through the agent with JSON output
        await call_agent_async_json(runner, USER_ID, SESSION_ID, user_input)


if __name__ == "__main__":
    asyncio.run(main())