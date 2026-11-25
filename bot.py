import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import Config
from utils import (
    ensure_temp_directory, 
    cleanup_temp_file, 
    format_file_size, 
    format_duration,
    format_recognized_text,
    add_smart_line_breaks
)
from speech_service import GroqWhisperClient

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Я бот для распознавания голосовых сообщений.\n"
        "(разработал - @przedviralem1)\n"
        "Просто отправь/перекинь мне голосовое сообщение, и я конвертирую его в текст.\n"
        "Могу зависнуть на 50 - 60 секунд из-за неактива."
    )
    await update.message.reply_text(welcome_message)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Произошла ошибка при обработке вашего запроса. Попробуйте ещё раз."
        )


async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice
    user_id = update.effective_user.id


    status_message = await update.message.reply_text(
        f"Обрабатываю ваше голосовое сообщение."
    )
    
    temp_file_path = None
    
    try:
        ensure_temp_directory(Config.TEMP_DIR)
        
        voice_file = await context.bot.get_file(voice.file_id)
        
        temp_file_path = os.path.join(
            Config.TEMP_DIR,
            f"voice_{user_id}_{voice.file_id}.ogg"
        )

        await voice_file.download_to_drive(temp_file_path)

        try:
            Config.validate_groq_config()
            speech_client = GroqWhisperClient(api_key=Config.GROQ_API_KEY)
        except ValueError as e:
            await status_message.edit_text(
                "Ошибка конфигурации сервиса распознавания речи."
            )
            return
        
        if voice.duration > 60: 
            await status_message.edit_text(
                "Распознаю речь... это может занять время.\n"
                "Пожалуйста, подождите..."
            )
        else:
            await status_message.edit_text(
                "Распознаю речь... это займет несколько секунд."
            )
        
        recognized_text = await speech_client.recognize_audio(
            audio_file_path=temp_file_path,
            language=None 
        )
        
        if recognized_text:
            formatted_text = format_recognized_text(recognized_text)
    
            max_text_length = 4096 - 100  
            
            if len(formatted_text) > max_text_length:
                # Удаляем статусное сообщение
                await status_message.delete()
                
                chunk_size = 3800  
                chunks = []
                
                paragraphs = formatted_text.split('\n\n')
                current_chunk = []
                current_length = 0
                
                for para in paragraphs:
                    para_length = len(para) + 2 
                    if current_length + para_length > chunk_size and current_chunk:
                        chunks.append('\n\n'.join(current_chunk))
                        current_chunk = [para]
                        current_length = para_length
                    else:
                        current_chunk.append(para)
                        current_length += para_length
                
                if current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                
                # Отправляем первый chunk как reply на голосовое
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await update.message.reply_text(chunk)
                    else:
                        await update.message.reply_text(chunk)
            else:
                # Удаляем статусное сообщение
                await status_message.delete()
                # Отправляем текст как reply на голосовое сообщение
                await update.message.reply_text(formatted_text)
        else:
            await status_message.edit_text(
                "Не удалось распознать речь в голосовом сообщении."
            )
        
    except Exception as e:
        await status_message.edit_text(
            "Произошла ошибка при обработке голосового сообщения.\n"
            "Попробуйте отправить его ещё раз."
        )
    
    finally:
        if temp_file_path:
            cleanup_temp_file(temp_file_path)


def main():
    ensure_temp_directory(Config.TEMP_DIR)

    application = Application.builder().token(Config.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    
    application.add_handler(MessageHandler(filters.VOICE, voice_handler))
  
    application.add_error_handler(error_handler)
 
    if Config.USE_WEBHOOK:
        application.run_webhook(
            listen="0.0.0.0",
            port=Config.WEBHOOK_PORT,
            url_path=Config.BOT_TOKEN,
            webhook_url=f"{Config.WEBHOOK_URL}/{Config.BOT_TOKEN}"
        )
    else:
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
