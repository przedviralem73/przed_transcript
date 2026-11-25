"""
Main Telegram bot module.
Handles commands and voice message processing.
"""

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

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    welcome_message = (
        "Привет! Я бот для распознавания голосовых сообщений.\n\n"
        "Просто отправь мне голосовое сообщение, и я конвертирую его в текст.\n\n"
        "Я поддерживаю автоматическое определение языка и добавляю пунктуацию!\n\n"
        "Используй /help для получения дополнительной информации."
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    help_message = (
        "**Как пользоваться ботом:**\n\n"
        "Запиши голосовое сообщение в Telegram\n"
        "Отправь его мне\n"
        "Получи текстовую расшифровку!\n\n"
        "**Поддерживаемые языки:**\n"
        "Русский\n"
        "Английский\n"
        "Автоопределение языка\n\n"
        "**Ограничения:**\n"
        "Нет ограничений по длине голосового сообщения\n"
        "Обработка может занять время для длинных записей\n\n"
        "Если возникли проблемы, попробуй отправить сообщение ещё раз."
    )
    await update.message.reply_text(help_message, parse_mode='Markdown')


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors in the bot."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Произошла ошибка при обработке вашего запроса. Попробуйте ещё раз."
        )


async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle voice messages from users.
    Downloads the voice file and prepares it for processing.
    """
    voice = update.message.voice
    user_id = update.effective_user.id
    
    # Log voice message details
    logger.info(
        f"Received voice message from user {user_id}: "
        f"duration={voice.duration}s, size={format_file_size(voice.file_size)}"
    )
    
    # Send initial status message
    status_message = await update.message.reply_text(
        f"🎙 Обрабатываю ваше голосовое сообщение...\n"
        f"⏱ Длительность: {format_duration(voice.duration)}\n"
        f"📦 Размер: {format_file_size(voice.file_size)}"
    )
    
    temp_file_path = None
    
    try:
        # Ensure temp directory exists
        ensure_temp_directory(Config.TEMP_DIR)
        
        # Download the voice file
        voice_file = await context.bot.get_file(voice.file_id)
        
        # Create unique filename using user_id and file_id
        temp_file_path = os.path.join(
            Config.TEMP_DIR,
            f"voice_{user_id}_{voice.file_id}.ogg"
        )
        
        # Download to temporary location
        await voice_file.download_to_drive(temp_file_path)
        logger.info(f"Downloaded voice file to: {temp_file_path}")
        
        # Initialize Groq Whisper client
        try:
            Config.validate_groq_config()
            speech_client = GroqWhisperClient(api_key=Config.GROQ_API_KEY)
        except ValueError as e:
            logger.error(f"Groq configuration error: {e}")
            await status_message.edit_text(
                "Ошибка конфигурации сервиса распознавания речи.\n"
                "Пожалуйста, обратитесь к администратору бота."
            )
            return
        
        # Update status message based on duration
        if voice.duration > 60:  # Longer than 1 minute
            await status_message.edit_text(
                "🔄 Распознаю речь... это может занять время.\n"
                "⏳ Пожалуйста, подождите..."
            )
        else:
            await status_message.edit_text(
                "🔄 Распознаю речь... это займет несколько секунд."
            )
        
        # Recognize speech with Whisper
        recognized_text = await speech_client.recognize_audio(
            audio_file_path=temp_file_path,
            language=None  # Auto-detect language
        )
        
        if recognized_text:
            # Format the recognized text for better readability
            formatted_text = format_recognized_text(recognized_text)
            
            # Prepare response with metadata
            response_header = f"✅ **Распознанный текст:**\n\n"
            response_footer = f"\n\n📊 Длительность: {format_duration(voice.duration)}"
            
            # Telegram has a message length limit of 4096 characters
            max_text_length = 4096 - len(response_header) - len(response_footer) - 100  # Buffer
            
            if len(formatted_text) > max_text_length:
                # For long messages, send header first
                await status_message.edit_text(response_header, parse_mode='Markdown')
                
                # Split text into chunks
                chunk_size = 3800  # Safe chunk size for Telegram
                chunks = []
                
                # Try to split by paragraphs first
                paragraphs = formatted_text.split('\n\n')
                current_chunk = []
                current_length = 0
                
                for para in paragraphs:
                    para_length = len(para) + 2  # +2 for \n\n
                    if current_length + para_length > chunk_size and current_chunk:
                        chunks.append('\n\n'.join(current_chunk))
                        current_chunk = [para]
                        current_length = para_length
                    else:
                        current_chunk.append(para)
                        current_length += para_length
                
                if current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                
                # Send each chunk
                for i, chunk in enumerate(chunks):
                    if i == len(chunks) - 1:
                        # Last chunk includes footer
                        await update.message.reply_text(f"{chunk}{response_footer}")
                    else:
                        await update.message.reply_text(chunk)
            else:
                # Short message, send everything together
                full_response = f"{response_header}{formatted_text}{response_footer}"
                await status_message.edit_text(full_response, parse_mode='Markdown')
        else:
            # Recognition failed
            await status_message.edit_text(
                "Не удалось распознать речь в голосовом сообщении.\n\n"
                "Возможные причины:\n"
                "• Плохое качество записи\n"
                "• Слишком тихий звук\n"
                "• Проблемы с API сервисом\n\n"
                "Попробуйте отправить другое голосовое сообщение."
            )
        
    except Exception as e:
        logger.error(f"Error processing voice message: {e}")
        await status_message.edit_text(
            "Произошла ошибка при обработке голосового сообщения.\n"
            "Попробуйте отправить его ещё раз."
        )
    
    finally:
        # Clean up the temporary file
        if temp_file_path:
            cleanup_temp_file(temp_file_path)


def main():
    """Start the bot."""
    logger.info("Starting bot...")
    
    # Ensure temp directory exists
    ensure_temp_directory(Config.TEMP_DIR)
    
    # Create application
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add voice message handler
    application.add_handler(MessageHandler(filters.VOICE, voice_handler))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    if Config.USE_WEBHOOK:
        logger.info(f"Starting webhook on port {Config.WEBHOOK_PORT}")
        application.run_webhook(
            listen="0.0.0.0",
            port=Config.WEBHOOK_PORT,
            url_path=Config.BOT_TOKEN,
            webhook_url=f"{Config.WEBHOOK_URL}/{Config.BOT_TOKEN}"
        )
    else:
        logger.info("Starting polling mode")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
