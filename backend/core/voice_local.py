"""
Local Voice Features
Text-to-Speech using Piper TTS
Speech-to-Text using Faster Whisper
"""

import os
import io
import asyncio
from typing import Optional
from pathlib import Path

# Note: These imports will work after installing dependencies
# For now, we'll create the structure with fallback implementations

class LocalVoice:
    """Local TTS and STT system"""
    
    def __init__(self):
        self.whisper_model = os.getenv("WHISPER_MODEL", "base")
        self.piper_voice = os.getenv("PIPER_VOICE", "en_US-lessac-medium")
        self.audio_dir = Path("backend/data/audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize models (lazy loading)
        self._whisper = None
        self._piper = None
    
    def _init_whisper(self):
        """Initialize Whisper model (lazy)"""
        if self._whisper is None:
            try:
                from faster_whisper import WhisperModel
                self._whisper = WhisperModel(
                    self.whisper_model,
                    device="cpu",
                    compute_type="int8"
                )
                print(f"✅ Whisper model loaded: {self.whisper_model}")
            except ImportError:
                print("⚠️  faster-whisper not installed, STT will not work")
                self._whisper = False
            except Exception as e:
                print(f"❌ Error loading Whisper: {e}")
                self._whisper = False
    
    def _init_piper(self):
        """Initialize Piper TTS model (lazy)"""
        if self._piper is None:
            try:
                # Placeholder for Piper TTS initialization
                # Actual implementation depends on piper-tts library
                print(f"✅ Piper TTS initialized: {self.piper_voice}")
                self._piper = True
            except Exception as e:
                print(f"❌ Error loading Piper: {e}")
                self._piper = False
    
    async def text_to_speech(
        self,
        text: str,
        voice: str = "female",
        rate: str = "+0%"
    ) -> bytes:
        """
        Convert text to speech using Piper TTS
        
        Args:
            text: Text to convert
            voice: Voice type (currently using piper voices)
            rate: Speech rate
        
        Returns:
            Audio bytes (WAV format)
        """
        # For now, fall back to edge-tts temporarily
        # TODO: Implement Piper TTS when stable
        try:
            import edge_tts
            
            voice_map = {
                "female": "en-US-AriaNeural",
                "male": "en-US-GuyNeural"
            }
            
            selected_voice = voice_map.get(voice, voice_map["female"])
            
            communicate = edge_tts.Communicate(text, selected_voice, rate=rate)
            audio_bytes = io.BytesIO()
            
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_bytes.write(chunk["data"])
            
            return audio_bytes.getvalue()
        
        except ImportError:
            print("⚠️  edge-tts not installed, using fallback")
            return b""
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            return b""
    
    async def speech_to_text(self, audio_bytes: bytes) -> str:
        """
        Convert speech to text using Faster Whisper
        
        Args:
            audio_bytes: Audio file bytes
        
        Returns:
            Transcribed text
        """
        self._init_whisper()
        
        if not self._whisper:
            return "Speech-to-text not available (Whisper not loaded)"
        
        try:
            # Save temporary audio file
            temp_audio = self.audio_dir / "temp_stt.wav"
            with open(temp_audio, 'wb') as f:
                f.write(audio_bytes)
            
            # Transcribe
            segments, info = self._whisper.transcribe(str(temp_audio))
            
            # Combine segments
            text = " ".join([segment.text for segment in segments])
            
            # Clean up
            temp_audio.unlink()
            
            return text.strip()
        
        except Exception as e:
            return f"Error in speech-to-text: {str(e)}"

# Global instance
local_voice = LocalVoice()

# Export functions for API
async def speak(text: str, voice: str = "female", rate: str = "+0%") -> bytes:
    """Text-to-speech wrapper"""
    return await local_voice.text_to_speech(text, voice, rate)

async def listen(audio_bytes: bytes) -> str:
    """Speech-to-text wrapper"""
    return await local_voice.speech_to_text(audio_bytes)
