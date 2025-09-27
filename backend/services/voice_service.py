"""
Voice Service - Handles speech-to-text and text-to-speech conversion
"""

import asyncio
import logging
from typing import Dict, Any, Optional
import base64
import io

# Placeholder for Google Cloud Speech and Text-to-Speech APIs
# In a real implementation, these would be imported and configured
try:
    from google.cloud import speech
    from google.cloud import texttospeech
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False
    logging.warning("Google Cloud Speech/TTS not available. Using mock implementation.")

logger = logging.getLogger(__name__)

class VoiceService:
    """Service for handling voice interactions in AERTS"""
    
    def __init__(self):
        self.speech_client = None
        self.tts_client = None
        self.voice_configs = self._setup_voice_configs()
        
        if GOOGLE_CLOUD_AVAILABLE:
            try:
                self.speech_client = speech.SpeechClient()
                self.tts_client = texttospeech.TextToSpeechClient()
                logger.info("Google Cloud Speech/TTS initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Google Cloud services: {e}")
                self.speech_client = None
                self.tts_client = None
    
    def _setup_voice_configs(self) -> Dict[str, Any]:
        """Setup voice configurations for different agent types"""
        return {
            "professional": {
                "name": "en-US-Wavenet-D",
                "language_code": "en-US",
                "ssml_gender": "MALE" if GOOGLE_CLOUD_AVAILABLE else None,
                "pitch": 0.0,
                "speaking_rate": 0.9
            },
            "nurse": {
                "name": "en-US-Wavenet-C",
                "language_code": "en-US",
                "ssml_gender": "FEMALE" if GOOGLE_CLOUD_AVAILABLE else None,
                "pitch": 0.0,
                "speaking_rate": 0.9
            },
            "doctor": {
                "name": "en-US-Wavenet-D",
                "language_code": "en-US",
                "ssml_gender": "MALE" if GOOGLE_CLOUD_AVAILABLE else None,
                "pitch": -1.0,
                "speaking_rate": 0.8
            },
            "concerned": {
                "name": "en-US-Wavenet-C",
                "language_code": "en-US",
                "ssml_gender": "FEMALE" if GOOGLE_CLOUD_AVAILABLE else None,
                "pitch": 2.0,
                "speaking_rate": 1.1
            }
        }
    
    async def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech audio to text"""
        if not self.speech_client:
            return await self._mock_speech_to_text(audio_data)
        
        try:
            # Configure audio settings
            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
                enable_automatic_punctuation=True,
                model="medical_dictation"  # Use medical dictation model if available
            )
            
            # Perform speech recognition
            response = self.speech_client.recognize(config=config, audio=audio)
            
            if response.results:
                return response.results[0].alternatives[0].transcript
            else:
                return ""
                
        except Exception as e:
            logger.error(f"Speech-to-text error: {e}")
            return await self._mock_speech_to_text(audio_data)
    
    async def text_to_speech(self, text: str, voice_type: str = "professional") -> bytes:
        """Convert text to speech audio"""
        if not self.tts_client:
            return await self._mock_text_to_speech(text, voice_type)
        
        try:
            voice_config = self.voice_configs.get(voice_type, self.voice_configs["professional"])
            
            # Configure synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Configure voice parameters
            voice = texttospeech.VoiceSelectionParams(
                language_code=voice_config["language_code"],
                name=voice_config["name"],
                ssml_gender=voice_config["ssml_gender"]
            )
            
            # Configure audio output
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                pitch=voice_config["pitch"],
                speaking_rate=voice_config["speaking_rate"]
            )
            
            # Perform synthesis
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return response.audio_content
            
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            return await self._mock_text_to_speech(text, voice_type)
    
    async def _mock_speech_to_text(self, audio_data: bytes) -> str:
        """Mock speech-to-text for testing"""
        # In a real implementation, this would use a fallback service
        # or return a pre-defined response for testing
        mock_responses = [
            "Give aspirin 325 milligrams",
            "Get an ECG immediately",
            "Start oxygen therapy",
            "Establish IV access",
            "Order nitroglycerin",
            "Give morphine for pain",
            "What are the current vitals?",
            "Call cardiology consult",
            "SBAR situation is 55 year old male with chest pain",
            "Handover report patient is stable"
        ]
        
        # Simple hash-based selection for consistent testing
        import hashlib
        hash_value = int(hashlib.md5(audio_data).hexdigest(), 16)
        return mock_responses[hash_value % len(mock_responses)]
    
    async def _mock_text_to_speech(self, text: str, voice_type: str) -> bytes:
        """Mock text-to-speech for testing"""
        # In a real implementation, this would use a fallback TTS service
        # For now, return a small audio placeholder
        return b"mock_audio_data"
    
    def get_voice_characteristics(self, voice_type: str) -> Dict[str, Any]:
        """Get voice characteristics for a given voice type"""
        return self.voice_configs.get(voice_type, self.voice_configs["professional"])
    
    async def process_voice_command(self, audio_data: bytes, session_id: str) -> Dict[str, Any]:
        """Process a voice command and return both text and audio responses"""
        # Convert speech to text
        text = await self.speech_to_text(audio_data)
        
        # Process the command (this would integrate with the main command processing)
        # For now, return the text
        return {
            "text": text,
            "audio_data": audio_data,  # Placeholder
            "confidence": 0.95,  # Placeholder
            "language": "en-US"
        }
    
    async def generate_agent_audio_responses(self, responses: Dict[str, str]) -> Dict[str, bytes]:
        """Generate audio for multiple agent responses"""
        audio_responses = {}
        
        for agent_name, response_text in responses.items():
            # Determine voice type based on agent
            voice_type = self._get_voice_type_for_agent(agent_name)
            audio_data = await self.text_to_speech(response_text, voice_type)
            audio_responses[agent_name] = audio_data
        
        return audio_responses
    
    def _get_voice_type_for_agent(self, agent_name: str) -> str:
        """Get appropriate voice type for agent"""
        voice_mapping = {
            "Coordinator": "professional",
            "Nurse": "nurse",
            "Doctor": "doctor",
            "Family": "concerned",
            "Evaluator": "professional"
        }
        
        return voice_mapping.get(agent_name, "professional")
    
    async def validate_medical_terminology(self, text: str) -> Dict[str, Any]:
        """Validate medical terminology in speech-to-text output"""
        medical_terms = [
            "aspirin", "asa", "ecg", "ekg", "electrocardiogram",
            "oxygen", "o2", "iv", "intravenous", "nitroglycerin", "nitro",
            "morphine", "pain", "analgesia", "cardiology", "consult",
            "sbar", "handover", "report", "vitals", "status"
        ]
        
        found_terms = []
        for term in medical_terms:
            if term.lower() in text.lower():
                found_terms.append(term)
        
        confidence = len(found_terms) / len(medical_terms) if medical_terms else 0
        
        return {
            "is_medical": len(found_terms) > 0,
            "found_terms": found_terms,
            "confidence": confidence,
            "suggestions": self._get_terminology_suggestions(text, found_terms)
        }
    
    def _get_terminology_suggestions(self, text: str, found_terms: list) -> list:
        """Get suggestions for medical terminology"""
        suggestions = []
        
        if "chest pain" in text.lower() and "ecg" not in found_terms:
            suggestions.append("Consider ordering an ECG")
        
        if "pain" in text.lower() and "morphine" not in found_terms and "aspirin" not in found_terms:
            suggestions.append("Consider pain management (morphine) or aspirin")
        
        if "heart" in text.lower() and "cardiology" not in found_terms:
            suggestions.append("Consider cardiology consultation")
        
        return suggestions
