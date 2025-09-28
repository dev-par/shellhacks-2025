import asyncio

# Import the main customer service agent
from emergency_room_agent.agent import emergency_room_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async

load_dotenv()

# ===== PART 1: Initialize In-Memory Session Service =====
# Using in-memory storage for this example (non-persistent)
session_service = InMemorySessionService()


# ===== PART 2: Define Initial State =====
# Enhanced STEMI Protocol State
initial_state = {
    "user_name": "Dr. Sarah Johnson",
    "current_state": "S1_INITIAL_STABILIZATION",
    "patient_data": {
        "age": 55,
        "gender": "male",
        "chief_complaint": "crushing substernal chest pain",
        "vital_signs": {
            "bp_systolic": 120,
            "bp_diastolic": 80,
            "heart_rate": 95,
            "oxygen_sat": 98,
            "respiratory_rate": 18,
            "temperature": 98.6
        },
        "allergies": ["Penicillin"],
        "medications": ["Aspirin 81mg daily"],
        "medical_history": ["Hypertension", "Smoking history"]
    },
    "interventions": {
        "asa_administered": False,
        "ecg_ordered": False,
        "ecg_result": None,
        "nitro_ordered": False,
        "morphine_ordered": False,
        "diagnosis_confirmed": False,
        "iv_access": False
    },
    "sbar_report": {
        "situation": "",
        "background": "",
        "assessment": "",
        "recommendation": ""
    },
    "sbar_approval": None,
    "training_score": 0,
    "session_start_time": None
}

"""
# ===== PART 3: State Transition Logic =====
def check_state_transition(current_state, interventions, patient_data):
    Check if state transition conditions are met
    transitions = {
        "S1_INITIAL_STABILIZATION": {
            "triggers": ["asa_administered", "ecg_ordered"],
            "next_state": "S2_DIAGNOSTIC_CONFIRMATION",
            "description": "ASA administered OR ECG ordered"
        },
        "S2_DIAGNOSTIC_CONFIRMATION": {
            "triggers": ["diagnosis_confirmed", "nitro_ordered", "morphine_ordered"],
            "next_state": "S3_CRITICAL_CONSULTATION",
            "description": "Diagnosis confirmed AND (Nitro OR Morphine) ordered",
            "safety_check": "check_bp_for_nitro"
        },
        "S3_CRITICAL_CONSULTATION": {
            "triggers": ["sbar_consult"],
            "next_state": "S4_SENIOR_HANDOVER",
            "description": "SBAR consultation initiated"
        },
        "S4_SENIOR_HANDOVER": {
            "triggers": ["sbar_handover"],
            "next_state": "S5_DEBRIEFING",
            "description": "SBAR handover completed and approved"
        }
    }
    
    if current_state not in transitions:
        return {"transition_allowed": False, "reason": "Unknown state"}
    
    transition = transitions[current_state]
    
    # Check if triggers are met
    triggers_met = any(interventions.get(trigger, False) for trigger in transition["triggers"])
    
    if triggers_met:
        # Special safety check for nitroglycerin
        if "safety_check" in transition and transition["safety_check"] == "check_bp_for_nitro":
            if interventions.get("nitro_ordered", False):
                bp_systolic = patient_data["vital_signs"]["bp_systolic"]
                if bp_systolic < 100:
                    return {
                        "transition_allowed": False,
                        "reason": f"Blood pressure too low for nitroglycerin (BP: {bp_systolic})",
                        "safety_warning": "Consider morphine instead"
                    }
        
        return {
            "transition_allowed": True,
            "new_state": transition["next_state"],
            "description": transition["description"]
        }
    
    return {
        "transition_allowed": False,
        "reason": f"Missing required actions: {transition['triggers']}",
        "description": transition["description"]
    }
"""

"""
def update_interventions(command, interventions, patient_data):
    "Update interventions based on command"
    command_lower = command.lower()
    
    # S1 Interventions
    if "aspirin" in command_lower or "asa" in command_lower:
        interventions["asa_administered"] = True
        print("✅ Aspirin 325mg administered")
    
    if "ecg" in command_lower or "electrocardiogram" in command_lower:
        interventions["ecg_ordered"] = True
        print("✅ 12-lead ECG ordered")
        # Simulate ECG result after 5 seconds
        import asyncio
        asyncio.create_task(simulate_ecg_result(interventions))
    
    if "iv" in command_lower or "intravenous" in command_lower:
        interventions["iv_access"] = True
        print("✅ IV access established")
    
    # S2 Interventions
    if "nitro" in command_lower or "nitroglycerin" in command_lower:
        # Check BP safety
        bp_systolic = patient_data["vital_signs"]["bp_systolic"]
        if bp_systolic >= 100:
            interventions["nitro_ordered"] = True
            print(f"✅ Nitroglycerin ordered (BP: {bp_systolic} - safe)")
        else:
            print(f"⚠️ Nitroglycerin HOLD - BP too low ({bp_systolic})")
            print("💡 Consider morphine for pain management")
    
    if "morphine" in command_lower:
        interventions["morphine_ordered"] = True
        print("✅ Morphine ordered for pain management")
    
    if "confirm" in command_lower and "diagnosis" in command_lower:
        interventions["diagnosis_confirmed"] = True
        print("✅ STEMI diagnosis confirmed")
    
    # S3 Interventions
    if "sbar" in command_lower and "consult" in command_lower:
        interventions["sbar_consult"] = True
        print("✅ SBAR consultation initiated")
    
    # S4 Interventions
    if "sbar" in command_lower and "handover" in command_lower:
        interventions["sbar_handover"] = True
        print("✅ SBAR handover submitted")
"""


# ===== PART 4: Test Session Manager =====
class STEMITestSession:
    def __init__(self, session_service, app_name, user_id):
        self.session_service = session_service
        self.app_name = app_name
        self.user_id = user_id
        self.session_id = None
        self.runner = None
        
    async def create_session(self, initial_state):
        """Create a new test session"""
        new_session = await self.session_service.create_session(
            app_name=self.app_name,
            user_id=self.user_id,
            state=initial_state
        )
        self.session_id = new_session.id
        print(f"✅ Created STEMI test session: {self.session_id}")
        return self.session_id
    
    def setup_runner(self, agent):
        """Setup the agent runner"""
        self.runner = Runner(
            agent=agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )
        print("✅ Agent runner configured")
    
    async def send_command(self, command):
        """Send a command to the agent and get response"""
        print(f"\n🔵 Sending: {command}")
        
        # Update interventions based on command
        session = await self.session_service.get_session(
            app_name=self.app_name, user_id=self.user_id, session_id=self.session_id
        )
        
        # Check for state transition
        current_state = session.state["current_state"]
    
        
        # Add to interaction history
        await add_user_query_to_history(
            self.session_service, self.app_name, self.user_id, self.session_id, command
        )
        
        # Process through agent
        response = await call_agent_async(self.runner, self.user_id, self.session_id, command)
        return response
    
    async def get_session_state(self):
        """Get current session state"""
        session = await self.session_service.get_session(
            app_name=self.app_name, user_id=self.user_id, session_id=self.session_id
        )
        return session.state
    
    async def print_state(self, label="Current State"):
        """Print current session state"""
        state = await self.get_session_state()
        print(f"\n📊 {label}:")
        print(f"  Current State: {state['current_state']}")
        print(f"  Patient: {state['patient_data']['age']}yo {state['patient_data']['gender']} - {state['patient_data']['chief_complaint']}")
        print(f"  Vitals: BP {state['patient_data']['vital_signs']['bp_systolic']}/{state['patient_data']['vital_signs']['bp_diastolic']}, HR {state['patient_data']['vital_signs']['heart_rate']}")
        print(f"  Interventions: {[k for k, v in state['interventions'].items() if v]}")
        if state['interventions']['ecg_result']:
            print(f"  ECG Result: {state['interventions']['ecg_result']['result']}")

# ===== PART 5: Test Functions =====
async def test_stemi_protocol():
    """Test the complete STEMI protocol flow"""
    print("🏥 Starting STEMI Protocol Test")
    print("=" * 50)
    
    # Setup test session
    test_session = STEMITestSession(session_service, "Emergensee", "testDoctor")
    await test_session.create_session(initial_state)
    test_session.setup_runner(emergency_room_agent)
    
    # Test S1: Initial Stabilization
    print("\n🟢 PHASE S1: Initial Stabilization")
    print("-" * 30)
    
    await test_session.send_command("I need to assess this 55-year-old male with chest pain")
    await test_session.send_command("Order aspirin 325mg")
    await test_session.send_command("Order 12-lead ECG")
    await test_session.send_command("Establish IV access")
    
    await test_session.print_state("After S1 Commands")
    
    # Wait for ECG result
    print("\n⏳ Waiting for ECG result (5 seconds)...")
    await asyncio.sleep(6)  # Wait for ECG simulation
    
    # Test S2: Diagnostic Confirmation
    print("\n🟡 PHASE S2: Diagnostic Confirmation")
    print("-" * 30)
    
    await test_session.send_command("ECG shows ST elevation in leads II, III, aVF")
    await test_session.send_command("Confirm STEMI diagnosis")
    await test_session.send_command("Order nitroglycerin 0.4mg sublingual")
    await test_session.send_command("Order morphine 2mg IV for pain")
    
    await test_session.print_state("After S2 Commands")
    
    # Test S3: Critical Consultation
    print("\n🟠 PHASE S3: Critical Consultation")
    print("-" * 30)
    
    await test_session.send_command("I need to consult with the senior doctor")
    await test_session.send_command("Use SBAR consult tool")
    
    await test_session.print_state("After S3 Commands")
    
    # Test S4: Senior Handover
    print("\n🔴 PHASE S4: Senior Handover")
    print("-" * 30)
    
    await test_session.send_command("Prepare SBAR handover report")
    await test_session.send_command("Situation: 55-year-old male with STEMI, stable vitals")
    await test_session.send_command("Background: HTN, smoking history, crushing chest pain")
    await test_session.send_command("Assessment: Confirmed STEMI, ST elevation present")
    await test_session.send_command("Recommendation: Immediate cardiac catheterization")
    
    await test_session.print_state("Final State")
    
    print("\n✅ STEMI Protocol Test Complete!")

async def interactive_mode():
    """Interactive mode for manual testing"""
    print("\n🏥 Welcome to AERTS STEMI Training!")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("Type 'state' to see current session state.")
    print("Type 'help' for available commands.")
    print("Type 'test' to run automated protocol test.\n")
    
    # Setup constants
    APP_NAME = "Emergensee"
    USER_ID = "newDoctorTrainee"

    # Create session
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")

    # Setup runner
    runner = Runner(
        agent=emergency_room_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Ending training session. Goodbye!")
            break
        elif user_input.lower() == "state":
            # Show current state
            session = await session_service.get_session(
                app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
            )
            print("\n📊 Current Session State:")
            print(f"  Current State: {session.state['current_state']}")
            print(f"  Patient: {session.state['patient_data']['age']}yo {session.state['patient_data']['gender']}")
            print(f"  Vitals: BP {session.state['patient_data']['vital_signs']['bp_systolic']}/{session.state['patient_data']['vital_signs']['bp_diastolic']}")
            print(f"  Interventions: {[k for k, v in session.state['interventions'].items() if v]}")
            continue
        elif user_input.lower() == "help":
            print("\n🆘 Available Commands:")
            print("  Medical Orders:")
            print("    - 'Order aspirin 325mg'")
            print("    - 'Order 12-lead ECG'")
            print("    - 'Establish IV access'")
            print("    - 'Order nitroglycerin' (check BP first)")
            print("    - 'Order morphine'")
            print("    - 'Confirm STEMI diagnosis'")
            print("  System Commands:")
            print("    - 'state' - show current state")
            print("    - 'test' - run automated test")
            print("    - 'help' - show this help")
            print("    - 'exit' - end session")
            continue
        elif user_input.lower() == "test":
            await test_stemi_protocol()
            continue

        # Update interventions based on command
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        
        # Check for state transition
        current_state = session.state["current_state"]
        

        # Process command
        await add_user_query_to_history(
            session_service, APP_NAME, USER_ID, SESSION_ID, user_input
        )
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

async def main_async():
    print("🏥 AERTS STEMI Protocol Testing")
    print("=" * 40)
    print("Choose testing mode:")
    print("1. Interactive Mode (manual testing)")
    print("2. Automated STEMI Protocol Test")
    print("3. State Inspection Only")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        await interactive_mode()
    elif choice == "2":
        await test_stemi_protocol()
    elif choice == "3":
        print("\n📋 Initial State Configuration:")
        print("=" * 40)
        for key, value in initial_state.items():
            if key == "patient_data":
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            elif key == "interventions":
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")
    else:
        print("Invalid choice, running interactive mode...")
        await interactive_mode()


def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
