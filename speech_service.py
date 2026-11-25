import logging
from typing import Optional
from groq import AsyncGroq

logger = logging.getLogger(__name__)


class GroqWhisperClient:

    def __init__(self, api_key: str):

        self.client = AsyncGroq(api_key=api_key)
        
    async def recognize_audio(
        self,
        audio_file_path: str,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        timeout: int = 300  
    ) -> Optional[str]:
 
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcription = await self.client.audio.transcriptions.create(
                    file=(audio_file_path, audio_file.read()),
                    model="whisper-large-v3-turbo", 
                    response_format="json",
                    language=language,  
                    prompt=prompt,
                    temperature=0.0, 
                    timeout=timeout
                )
                
                text = transcription.text
                
                if text:
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
