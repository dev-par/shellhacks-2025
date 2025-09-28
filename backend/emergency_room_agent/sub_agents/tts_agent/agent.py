import asyncio
import pyaudio
import wave
import tempfile
import os
from google.cloud import texttospeech
from typing import Optional
import io

class TTSAgent:
    def __init__(self, 
                 credentials_path: str = None,
                 language_code: str = "en-US",
                 voice_name: str = None,
                 speaking_rate: float = 1.0,
                 pitch: float = 0.0):
        """
        Initialize TTS Agent with Google Cloud Text-to-Speech
        
        Args:
            credentials_path: Path to Google Cloud credentials JSON
            language_code: Language code (e.g., 'en-US')
            voice_name: Specific voice name (e.g., 'en-US-Neural2-D')
            speaking_rate: Speech rate (0.25 to 4.0)
            pitch: Voice pitch (-20.0 to 20.0)
        """
        # Set up Google Cloud credentials if provided
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        self.client = texttospeech.TextToSpeechClient()
        self.language_code = language_code
        self.voice_name = voice_name
        self.speaking_rate = speaking_rate
        self.pitch = pitch
        
        # Audio playback settings
        self.audio = pyaudio.PyAudio()
        
    def get_available_voices(self, language_code: str = None):
        """
        Get list of available voices for testing different voices
        
        Args:
            language_code: Filter by language code
            
        Returns:
            List of available voices
        """
        voices = self.client.list_voices()
        
        available_voices = []
        for voice in voices.voices:
            if language_code is None or language_code in voice.language_codes:
                available_voices.append({
                    'name': voice.name,
                    'language_codes': voice.language_codes,
                    'gender': voice.ssml_gender.name
                })
                
        return available_voices
        
    async def speak_text(self, text: str, save_to_file: str = None) -> Optional[str]:
        """
        Convert text to speech and play it through speakers
        
        Args:
            text: Text to convert to speech (e.g., "Hello, this is the doctor")
            save_to_file: Optional path to save audio file
            
        Returns:
            Path to saved audio file if save_to_file is provided
        """
        # Create synthesis input
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Build voice selection parameters
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.voice_name
        )
        
        # Configure audio output
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=self.speaking_rate,
            pitch=self.pitch
        )
        
        # Perform text-to-speech synthesis
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Save to file or temporary file
        if save_to_file:
            audio_file_path = save_to_file
        else:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            audio_file_path = temp_file.name
            temp_file.close()
        
        # Write audio content to file
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(response.audio_content)
            
        # Play the audio through speakers
        await self._play_audio_file(audio_file_path)
        
        # Clean up temporary file if not saving
        if not save_to_file:
            try:
                os.unlink(audio_file_path)
            except:
                pass
            return None
        
        return audio_file_path
    
    async def speak_with_emotion(self, text: str, emotion: str = "neutral"):
        """
        Speak text with emotional inflection using SSML
        
        Args:
            text: Text to speak
            emotion: Emotion type (calm, urgent, concerned, reassuring)
        """
        # Create SSML with emotional prosody
        emotion_settings = {
            "calm": {"rate": "slow", "pitch": "-2st"},
            "urgent": {"rate": "fast", "pitch": "+3st"},
            "concerned": {"rate": "medium", "pitch": "-1st"},
            "reassuring": {"rate": "slow", "pitch": "-1st"}
        }
        
        settings = emotion_settings.get(emotion, {"rate": "medium", "pitch": "0st"})
        
        ssml = f"""
        <speak>
            <prosody rate="{settings['rate']}" pitch="{settings['pitch']}">
                {text}
            </prosody>
        </speak>
        """
        
        # Use SSML synthesis
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml.strip())
        
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.voice_name
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Create temporary file and play
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_file.write(response.audio_content)
        temp_file.close()
        
        await self._play_audio_file(temp_file.name)
        
        # Clean up
        try:
            os.unlink(temp_file.name)
        except:
            pass
    
    async def _play_audio_file(self, audio_file_path: str):
        """Play an audio file using pyaudio"""
        try:
            # Open wave file
            wf = wave.open(audio_file_path, 'rb')
            
            # Create audio stream
            stream = self.audio.open(
                format=self.audio.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )
            
            # Play audio
            chunk = 1024
            data = wf.readframes(chunk)
            
            while data:
                stream.write(data)
                data = wf.readframes(chunk)
                # Add small delay to prevent blocking
                await asyncio.sleep(0.01)
            
            # Clean up
            stream.stop_stream()
            stream.close()
            wf.close()
            
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def set_voice_parameters(self, 
                           voice_name: str = None,
                           speaking_rate: float = None,
                           pitch: float = None):
        """
        Update voice parameters on the fly
        
        Args:
            voice_name: New voice name (e.g., 'en-US-Neural2-F' for female)
            speaking_rate: New speaking rate
            pitch: New pitch
        """
        if voice_name:
            self.voice_name = voice_name
        if speaking_rate:
            self.speaking_rate = speaking_rate
        if pitch:
            self.pitch = pitch
    
    def __del__(self):
        """Cleanup audio resources"""
        if hasattr(self, 'audio'):
            self.audio.terminate()