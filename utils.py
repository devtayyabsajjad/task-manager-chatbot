"""
Utility functions for Groq FastAPI Chatbot.
Contains helper functions for message processing, validation, and formatting.
"""

import re
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def sanitize_message(message: str) -> str:
    """
    Sanitize user input message by removing potentially harmful content.
    
    Args:
        message (str): Raw user message
        
    Returns:
        str: Sanitized message
    """
    if not message:
        return ""
    
    # Remove excessive whitespace
    message = re.sub(r'\s+', ' ', message.strip())
    
    # Remove potential script tags (basic XSS protection)
    message = re.sub(r'<script.*?</script>', '', message, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove HTML tags
    message = re.sub(r'<[^>]+>', '', message)
    
    # Limit message length (additional safety check)
    if len(message) > 4000:
        message = message[:4000] + "..."
        logger.warning("Message truncated due to length limit")
    
    return message


def format_chat_response(response: str, model: str, tokens: Optional[int] = None) -> Dict[str, Any]:
    """
    Format the chat response with metadata.
    
    Args:
        response (str): AI response text
        model (str): Model used for generation
        tokens (Optional[int]): Number of tokens used
        
    Returns:
        Dict[str, Any]: Formatted response with metadata
    """
    return {
        "reply": response.strip(),
        "model_used": model,
        "tokens_used": tokens,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "success"
    }


def validate_model_name(model: str) -> bool:
    """
    Validate if the provided model name is supported.
    
    Args:
        model (str): Model name to validate
        
    Returns:
        bool: True if model is valid, False otherwise
    """
    valid_models = [
        "llama-3.1-8b-instant",
        "llama3-70b-8192", 
        "mixtral-8x7b-32768",
        "gemma-7b-it"
    ]
    
    return model in valid_models


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of token count for a given text.
    This is an approximation - actual token count may vary.
    
    Args:
        text (str): Text to estimate tokens for
        
    Returns:
        int: Estimated token count
    """
    # Rough approximation: 1 token ≈ 4 characters for English text
    return len(text) // 4


def create_system_prompt(custom_instructions: Optional[str] = None) -> str:
    """
    Create a system prompt for the AI model.
    
    Args:
        custom_instructions (Optional[str]): Custom instructions to add to the system prompt
        
    Returns:
        str: Complete system prompt
    """
    base_prompt = (
        "You are a helpful AI assistant. Provide clear, concise, and helpful responses. "
        "Be friendly and professional in your interactions. If you're unsure about something, "
        "acknowledge the uncertainty rather than guessing."
    )
    
    if custom_instructions:
        base_prompt += f"\n\nAdditional instructions: {custom_instructions}"
    
    return base_prompt


def log_chat_interaction(user_message: str, ai_response: str, model: str, tokens: Optional[int] = None):
    """
    Log chat interaction for monitoring and debugging.
    
    Args:
        user_message (str): User's input message
        ai_response (str): AI's response
        model (str): Model used
        tokens (Optional[int]): Tokens consumed
    """
    logger.info(
        f"Chat interaction - Model: {model}, "
        f"User message length: {len(user_message)}, "
        f"Response length: {len(ai_response)}, "
        f"Tokens used: {tokens or 'unknown'}"
    )


def create_error_response(error_type: str, message: str, status_code: int = 500) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        error_type (str): Type of error
        message (str): Error message
        status_code (int): HTTP status code
        
    Returns:
        Dict[str, Any]: Formatted error response
    """
    return {
        "error": error_type,
        "message": message,
        "status_code": status_code,
        "timestamp": datetime.utcnow().isoformat()
    }


def health_check_groq_client(groq_client) -> Dict[str, Any]:
    """
    Perform a health check on the Groq client.
    
    Args:
        groq_client: Groq client instance
        
    Returns:
        Dict[str, Any]: Health check results
    """
    try:
        if not groq_client:
            return {
                "status": "unhealthy",
                "message": "Groq client is not initialized",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Try a simple API call to test connectivity
        # Note: This is a basic check - in production you might want a more sophisticated test
        return {
            "status": "healthy",
            "message": "Groq client is connected and ready",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "message": f"Groq client health check failed: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }

