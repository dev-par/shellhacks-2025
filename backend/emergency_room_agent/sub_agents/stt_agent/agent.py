import asyncio
import pyaudio
import wave
from google.cloud import speech
from typing import Optional, Callable
import threading
import queue

class STTAgent:
    def __init__(self, 
                 credentials_path: str = None,
                 language_code: str = "en-US",
                 sample_rate: int = 16000):
        """
        Initialize STT Agent with Google Cloud Speech-to-Text
        
        Args:
            credentials_path: Path to Google Cloud credentials JSON
            language_code: Language for speech recognition
            sample_rate: Audio sample rate
        """
        # Set up Google Cloud credentials if provided
        if credentials_path:
            import os
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        self.client = speech.SpeechClient()
        self.language_code = language_code
        self.sample_rate = sample_rate
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        # Audio recording settings
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.audio = pyaudio.PyAudio()
        
    async def start_continuous_recognition(self, 
                                         on_transcript: Callable[[str], None],
                                         on_final: Callable[[str], None] = None):
        """
        Start continuous speech recognition
        
        Args:
            on_transcript: Callback for interim transcripts
            on_final: Callback for final transcripts
        """
        self.is_listening = True
        
        # Start audio recording in separate thread
        record_thread = threading.Thread(target=self._record_audio)
        record_thread.start()
        
        # Process audio stream
        await self._process_audio_stream(on_transcript, on_final)
        
    def _record_audio(self):
        """Record audio from microphone"""
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        while self.is_listening:
            try:
                data = stream.read(self.chunk, exception_on_overflow=False)
                self.audio_queue.put(data)
            except Exception as e:
                print(f"Error recording audio: {e}")
                break
                
        stream.stop_stream()
        stream.close()
        
    async def _process_audio_stream(self, 
                                  on_transcript: Callable[[str], None],
                                  on_final: Callable[[str], None] = None):
        """Process recorded audio with Google Speech-to-Text"""
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.sample_rate,
            language_code=self.language_code,
            enable_automatic_punctuation=True,
        )
        
        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )
        
        def request_generator():
            while self.is_listening:
                try:
                    data = self.audio_queue.get(timeout=1.0)
                    yield speech.StreamingRecognizeRequest(audio_content=data)
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error in request generator: {e}")
                    break
        
        try:
            requests = request_generator()
            responses = self.client.streaming_recognize(streaming_config, requests)
            
            for response in responses:
                if not self.is_listening:
                    break
                    
                for result in response.results:
                    transcript = result.alternatives[0].transcript
                    
                    if result.is_final:
                        if on_final:
                            on_final(transcript)
                        else:
                            on_transcript(transcript)
                    else:
                        on_transcript(transcript)
                        
        except Exception as e:
            print(f"Error in speech recognition: {e}")
    
    def stop_listening(self):
        """Stop continuous recognition"""
        self.is_listening = False
        
    def __del__(self):
        """Cleanup audio resources"""
        if hasattr(self, 'audio'):
            self.audio.terminate()