from datetime import datetime

from google.genai import types


# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


async def display_state(
    session_service, app_name, user_id, session_id, label="Current State"
):
    """Display the current session state in a formatted way."""
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        # Format the output with clear sections
        print(f"\n{'-' * 10} {label} {'-' * 10}")

        # Handle patient information
        patient_info = session.state.get("patient_information", {})
        if patient_info:
            patient_name = patient_info.get("patient_name", "Unknown")
            patient_age = patient_info.get("patient_age", "Unknown")
            print(f"👤 Patient: {patient_name} (Age: {patient_age})")
            
            # Display vitals if available
            static_data = patient_info.get("static_patient_data", {})
            vitals = static_data.get("vitals_snapshot", {})
            if vitals:
                print(f"📊 Vitals:")
                print(f"  • BP: {vitals.get('BP_Systolic', 'N/A')}/{vitals.get('BP_Diastolic', 'N/A')}")
                print(f"  • HR: {vitals.get('HR', 'N/A')} bpm")
                print(f"  • O2 Sat: {vitals.get('O2_Sat', 'N/A')}% ({vitals.get('O2_Source', 'N/A')})")
                print(f"  • Pain Score: {vitals.get('Pain_Score', 'N/A')}/10")
            
            # Display history if available
            history = static_data.get("history", {})
            if history:
                print(f"📋 History:")
                print(f"  • Complaint: {history.get('Complaint', 'N/A')}")
                print(f"  • Known History: {history.get('Known_History', 'N/A')}")
                print(f"  • Allergies: {history.get('Allergies', 'N/A')}")
        else:
            print("👤 Patient: No patient information available")

        # Handle session flags
        session_flags = session.state.get("session_flags", {})
        if session_flags:
            print(f"🚩 Session Flags:")
            for flag, value in session_flags.items():
                status = "✅" if value else "❌"
                print(f"  {status} {flag.replace('_', ' ').title()}")
        else:
            print("🚩 Session Flags: None")

        # Handle any other state variables (for backward compatibility)
        other_keys = set(session.state.keys()) - {"patient_information", "session_flags"}
        if other_keys:
            print(f"📝 Other State:")
            for key in other_keys:
                value = session.state.get(key)
                print(f"  • {key}: {value}")

        print("-" * (22 + len(label)))
    except Exception as e:
        print(f"Error displaying state: {e}")


async def process_agent_response(event):
    """Process and display agent response events."""
    # Log basic event info
    #print(f"Event ID: {event.id}, Author: {event.author}")

    # Check for specific parts first
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "executable_code") and part.executable_code:
                # Access the actual code string via .code
                print(
                    f"  Debug: Agent generated code:\n```python\n{part.executable_code.code}\n```"
                )
                has_specific_part = True
            elif hasattr(part, "code_execution_result") and part.code_execution_result:
                # Access outcome and output correctly
                print(
                    f"  Debug: Code Execution Result: {part.code_execution_result.outcome} - Output:\n{part.code_execution_result.output}"
                )
                has_specific_part = True
            elif hasattr(part, "tool_response") and part.tool_response:
                # Print tool response information
                print(f"  Tool Response: {part.tool_response.output}")
                has_specific_part = True
            # Also print any text parts found in any event for debugging
            elif hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"  Text: '{part.text.strip()}'")

    # Check for final response after specific parts
    final_response = None
    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
            # Use colors and formatting to make the final response stand out
            print(
                f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ AGENT RESPONSE ═════════════════════════════════════════{Colors.RESET}"
            )
            print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")
            print(
                f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═════════════════════════════════════════════════════════════{Colors.RESET}\n"
            )
        else:
            print(
                f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}==> Final Agent Response: [No text content in final event]{Colors.RESET}\n"
            )

    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(
        f"\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}--- Running Query: {query} ---{Colors.RESET}"
    )
    final_response_text = None

    # Display state before processing
    """
    await display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State BEFORE processing",
    )
    """

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # Process each event and get the final response if available
            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"Error during agent call: {e}")

    # Display state after processing the message
    """
    await display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State AFTER processing",
    )
    """

    return final_response_text