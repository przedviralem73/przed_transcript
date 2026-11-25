"""
Groq API (Whisper) integration module.
Handles speech-to-text conversion using Groq's Whisper API.
"""

import logging
from typing import Optional
from groq import AsyncGroq

logger = logging.getLogger(__name__)


class GroqWhisperClient:
    """
    Client for Groq Whisper API.
    Provides fast speech-to-text recognition with auto language detection.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize Groq Whisper client.
        
        Args:
            api_key: Groq API key
        """
        self.client = AsyncGroq(api_key=api_key)
        
    async def recognize_audio(
        self,
        audio_file_path: str,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        timeout: int = 300  # 5 minutes timeout
    ) -> Optional[str]:
        """
        Recognize speech from audio file using Whisper.
        
        Args:
            audio_file_path: Path to the audio file (supports various formats)
            language: Optional language code (ISO-639-1, e.g., "ru", "en")
                     If None, auto-detects the language
            prompt: Optional prompt to guide the transcription style and vocabulary
            timeout: Request timeout in seconds (default: 300)
            
        Returns:
            Recognized text or None if recognition failed
        """
        try:
            logger.info(f"Sending audio to Groq Whisper API: {audio_file_path}")
            
            # Open and read the audio file
            with open(audio_file_path, 'rb') as audio_file:
                # Create transcription using Whisper
                transcription = await self.client.audio.transcriptions.create(
                    file=(audio_file_path, audio_file.read()),
                    model="whisper-large-v3-turbo",  # Fast and accurate model
                    response_format="json",
                    language=language,  # Auto-detect if None
                    prompt=prompt,
                    temperature=0.0,  # Deterministic output
                    timeout=timeout
                )
                
                text = transcription.text
                
                if text:
                    logger.info(f"Successfully recognized text (length: {len(text)} chars)")
                    logger.debug(f"Text preview: {text[:100]}...")
                    return text
                else:
                    logger.warning("Empty recognition result")
                    return None
                    
        except FileNotFoundError:
            logger.error(f"Audio file not found: {audio_file_path}")
            return None
        except TimeoutError:
            logger.error(f"Timeout while processing audio file: {audio_file_path}")
            return None
        except Exception as e:
            logger.error(f"Error during speech recognition: {e}")
            return None
