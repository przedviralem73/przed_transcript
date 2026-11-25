"""
Utility functions for the bot.
Handles file operations, cleanup, and formatting.
"""

import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def ensure_temp_directory(temp_dir: str) -> None:
    """
    Ensure that the temporary directory exists.
    
    Args:
        temp_dir: Path to the temporary directory
    """
    Path(temp_dir).mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured temp directory exists: {temp_dir}")


def cleanup_temp_file(file_path: str) -> None:
    """
    Delete a temporary file if it exists.
    
    Args:
        file_path: Path to the file to delete
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Cleaned up temp file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to cleanup file {file_path}: {e}")


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def format_duration(seconds: int) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "1:30" or "15:45")
    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}"


def format_recognized_text(text: str) -> str:
    """
    Format recognized text for better readability.
    Adds proper spacing and breaks long text into paragraphs.
    
    Args:
        text: Raw recognized text
        
    Returns:
        Formatted text with proper paragraphs
    """
    if not text:
        return text
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]
    
    # Split into sentences (simple approach)
    sentences = []
    current_sentence = []
    words = text.split()
    
    for word in words:
        current_sentence.append(word)
        # Check if word ends with sentence-ending punctuation
        if word.endswith(('.', '!', '?')):
            sentences.append(' '.join(current_sentence))
            current_sentence = []
    
    # Add remaining words if any
    if current_sentence:
        sentences.append(' '.join(current_sentence))
    
    # Group sentences into paragraphs (every 3-4 sentences)
    paragraphs = []
    paragraph_size = 3
    
    for i in range(0, len(sentences), paragraph_size):
        paragraph = ' '.join(sentences[i:i + paragraph_size])
        paragraphs.append(paragraph)
    
    # Join paragraphs with double newline
    formatted_text = '\n\n'.join(paragraphs)
    
    return formatted_text


def add_smart_line_breaks(text: str, max_line_length: int = 80) -> str:
    """
    Add smart line breaks to long text for better readability in Telegram.
    
    Args:
        text: Text to format
        max_line_length: Maximum line length before breaking
        
    Returns:
        Text with smart line breaks
    """
    if len(text) <= max_line_length:
        return text
    
    paragraphs = text.split('\n\n')
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        words = paragraph.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            if current_length + word_length > max_line_length and current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length
        
        if current_line:
            lines.append(' '.join(current_line))
        
        formatted_paragraphs.append('\n'.join(lines))
    
    return '\n\n'.join(formatted_paragraphs)
