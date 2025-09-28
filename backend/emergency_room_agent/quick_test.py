import asyncio
import os
from sub_agents.tts_agent import TTSAgent
from sub_agents.stt_agent import STTAgent

async def quick_tts_test():
    """Test TTS only - no microphone needed"""
    print("Testing TTS (Text-to-Speech)...")
    
    # Create TTS agent
    tts = TTSAgent(
        credentials_path="./google-cloud-credentials.json",
        voice_name="en-US-Neural2-D",  # Male voice
        speaking_rate=1.0
    )
    
    # Test basic speech
    print("Speaking: 'Hello, this is a test'")
    await tts.speak_text("Hello, this is a test of the text to speech system.")
    
    # Test emotional speech
    print("Speaking with urgency...")
    await tts.speak_with_emotion("This is an urgent message!", emotion="urgent")
    
    print("Speaking calmly...")
    await tts.speak_with_emotion("Please stay calm, everything will be okay.", emotion="calm")

async def quick_stt_test():
    """Test STT - requires microphone"""
    print("Testing STT (Speech-to-Text)...")
    print("Say something into your microphone. Press Ctrl+C to stop.")
    
    # Create STT agent
    stt = STTAgent(
        credentials_path="./google-cloud-credentials.json"
    )
    
    def on_speech(transcript):
        print(f"You said: {transcript}")
    
    def on_final(transcript):
        print(f"FINAL: {transcript}")
        print("---")
    
    try:
        await stt.start_continuous_recognition(
            on_transcript=on_speech,
            on_final=on_final
        )
    except KeyboardInterrupt:
        print("Stopping speech recognition...")
        stt.stop_listening()

async def quick_combined_test():
    """Test both TTS and STT together"""
    print("Combined Test - Speak and get a response!")
    
    tts = TTSAgent(
        credentials_path="./google-cloud-credentials.json",
        voice_name="en-US-Neural2-F"  # Female voice
    )
    
    stt = STTAgent(
        credentials_path="./google-cloud-credentials.json"  
    )
    
    # Simple responses
    responses = {
        "hello": "Hello! How can I help you today?",
        "help": "I'm here to assist you. What do you need?",
        "pain": "I understand you're in pain. Can you describe where it hurts?",
        "chest": "Chest pain can be serious. Are you having trouble breathing?"
    }
    
    def on_final_speech(transcript):
        print(f"You said: {transcript}")
        
        # Simple keyword matching for responses
        transcript_lower = transcript.lower()
        response = "I heard you, but I'm not sure how to respond to that."
        
        for keyword, reply in responses.items():
            if keyword in transcript_lower:
                response = reply
                break
        
        print(f"Responding: {response}")
        asyncio.create_task(tts.speak_text(response))
    
    print("Say something like 'hello', 'help', 'I have chest pain'...")
    print("Press Ctrl+C to stop.")
    
    try:
        await stt.start_continuous_recognition(on_final=on_final_speech)
    except KeyboardInterrupt:
        print("Stopping conversation...")
        stt.stop_listening()

def check_setup():
    """Check if everything is set up correctly"""
    print("Checking setup...")
    
    # Check if credentials file exists
    creds_path = "./google-cloud-credentials.json" 
    if not os.path.exists(creds_path):
        print("❌ Google credentials file not found!")
        print("1. Go to Google Cloud Console")
        print("2. Enable Speech-to-Text and Text-to-Speech APIs")
        print("3. Create a service account and download JSON credentials")
        print("4. Update the path in this script")
        return False
    
    # Check if required packages are installed
    try:
        import google.cloud.speech
        import google.cloud.texttospeech
        import pyaudio
        print("✅ All packages installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install google-cloud-speech google-cloud-texttospeech pyaudio")
        return False
    
    print("✅ Setup looks good!")
    return True

async def main():
    """Main test function"""
    if not check_setup():
        return
    
    print("\nQuick Test Options:")
    print("1. Test TTS only (no microphone needed)")
    print("2. Test STT only (microphone required)")
    print("3. Test both together (microphone required)")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        await quick_tts_test()
    elif choice == "2":
        await quick_stt_test()
    elif choice == "3":
        await quick_combined_test()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())