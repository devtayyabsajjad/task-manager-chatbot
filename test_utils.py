"""
Test suite for utility functions.
Tests all helper functions in the utils module.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock

from app.utils import (
    sanitize_message,
    format_chat_response,
    validate_model_name,
    estimate_tokens,
    create_system_prompt,
    create_error_response,
    health_check_groq_client
)


class TestSanitizeMessage:
    """Test message sanitization functionality."""
    
    def test_sanitize_normal_message(self):
        """Test sanitizing a normal message."""
        message = "Hello, how are you today?"
        result = sanitize_message(message)
        assert result == "Hello, how are you today?"
    
    def test_sanitize_empty_message(self):
        """Test sanitizing an empty message."""
        result = sanitize_message("")
        assert result == ""
    
    def test_sanitize_none_message(self):
        """Test sanitizing None message."""
        result = sanitize_message(None)
        assert result == ""
    
    def test_sanitize_whitespace(self):
        """Test sanitizing message with excessive whitespace."""
        message = "Hello    world   \n\n  test"
        result = sanitize_message(message)
        assert result == "Hello world test"
    
    def test_sanitize_script_tags(self):
        """Test removing script tags."""
        message = "Hello <script>alert('xss')</script> world"
        result = sanitize_message(message)
        assert result == "Hello  world"
    
    def test_sanitize_html_tags(self):
        """Test removing HTML tags."""
        message = "Hello <b>bold</b> and <i>italic</i> text"
        result = sanitize_message(message)
        assert result == "Hello bold and italic text"
    
    def test_sanitize_long_message(self):
        """Test truncating very long messages."""
        message = "x" * 5000
        result = sanitize_message(message)
        assert len(result) <= 4003  # 4000 + "..."
        assert result.endswith("...")


class TestFormatChatResponse:
    """Test chat response formatting."""
    
    def test_format_basic_response(self):
        """Test formatting a basic response."""
        result = format_chat_response("Hello!", "llama-3.1-8b-instant", 25)
        
        assert result["reply"] == "Hello!"
        assert result["model_used"] == "llama-3.1-8b-instant"
        assert result["tokens_used"] == 25
        assert result["status"] == "success"
        assert "timestamp" in result
    
    def test_format_response_no_tokens(self):
        """Test formatting response without token count."""
        result = format_chat_response("Hello!", "llama-3.1-8b-instant")
        
        assert result["reply"] == "Hello!"
        assert result["model_used"] == "llama-3.1-8b-instant"
        assert result["tokens_used"] is None
        assert result["status"] == "success"
    
    def test_format_response_strips_whitespace(self):
        """Test that response strips whitespace."""
        result = format_chat_response("  Hello!  \n", "llama-3.1-8b-instant")
        assert result["reply"] == "Hello!"


class TestValidateModelName:
    """Test model name validation."""
    
    def test_valid_models(self):
        """Test validation of valid model names."""
        valid_models = [
            "llama-3.1-8b-instant",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ]
        
        for model in valid_models:
            assert validate_model_name(model) is True
    
    def test_invalid_models(self):
        """Test validation of invalid model names."""
        invalid_models = [
            "invalid-model",
            "gpt-4",
            "",
            None,
            "llama3-8b-8193"  # Wrong context length
        ]
        
        for model in invalid_models:
            assert validate_model_name(model) is False


class TestEstimateTokens:
    """Test token estimation functionality."""
    
    def test_estimate_empty_text(self):
        """Test token estimation for empty text."""
        result = estimate_tokens("")
        assert result == 0
    
    def test_estimate_short_text(self):
        """Test token estimation for short text."""
        text = "Hello world"  # 11 characters
        result = estimate_tokens(text)
        assert result == 2  # 11 // 4 = 2
    
    def test_estimate_longer_text(self):
        """Test token estimation for longer text."""
        text = "This is a longer text that should have more tokens estimated."
        result = estimate_tokens(text)
        expected = len(text) // 4
        assert result == expected


class TestCreateSystemPrompt:
    """Test system prompt creation."""
    
    def test_create_basic_system_prompt(self):
        """Test creating basic system prompt."""
        result = create_system_prompt()
        
        assert "helpful AI assistant" in result
        assert "clear, concise, and helpful" in result
        assert "friendly and professional" in result
    
    def test_create_system_prompt_with_custom_instructions(self):
        """Test creating system prompt with custom instructions."""
        custom = "Always respond in a formal tone."
        result = create_system_prompt(custom)
        
        assert "helpful AI assistant" in result
        assert custom in result
        assert "Additional instructions:" in result


class TestCreateErrorResponse:
    """Test error response creation."""
    
    def test_create_basic_error_response(self):
        """Test creating basic error response."""
        result = create_error_response("ValidationError", "Invalid input")
        
        assert result["error"] == "ValidationError"
        assert result["message"] == "Invalid input"
        assert result["status_code"] == 500  # Default
        assert "timestamp" in result
    
    def test_create_error_response_custom_status(self):
        """Test creating error response with custom status code."""
        result = create_error_response("NotFound", "Resource not found", 404)
        
        assert result["error"] == "NotFound"
        assert result["message"] == "Resource not found"
        assert result["status_code"] == 404


class TestHealthCheckGroqClient:
    """Test Groq client health check functionality."""
    
    def test_health_check_no_client(self):
        """Test health check with no client."""
        result = health_check_groq_client(None)
        
        assert result["status"] == "unhealthy"
        assert "not initialized" in result["message"]
        assert "timestamp" in result
    
    def test_health_check_with_client(self):
        """Test health check with valid client."""
        mock_client = Mock()
        result = health_check_groq_client(mock_client)
        
        assert result["status"] == "healthy"
        assert "connected and ready" in result["message"]
        assert "timestamp" in result
    
    def test_health_check_client_exception(self):
        """Test health check when client raises exception."""
        mock_client = Mock()
        mock_client.side_effect = Exception("Connection failed")
        
        # This test might need adjustment based on actual implementation
        result = health_check_groq_client(mock_client)
        assert "timestamp" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

