"""
Test suite for Groq FastAPI Chatbot main application.
Tests all API endpoints and functionality.
"""

import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# Set test environment variables before importing the app
os.environ["GROQ_API_KEY"] = "test_api_key_12345"

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_groq_response():
    """Mock Groq API response."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Hello! How can I help you today?"
    mock_response.usage = Mock()
    mock_response.usage.total_tokens = 25
    return mock_response


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Groq FastAPI Chatbot is running!"
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_health_check_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "groq_client" in data


class TestModelsEndpoint:
    """Test models endpoint."""
    
    def test_get_available_models(self, client):
        """Test getting available models."""
        response = client.get("/models")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert len(data["models"]) > 0
        
        # Check model structure
        model = data["models"][0]
        assert "id" in model
        assert "name" in model
        assert "description" in model


class TestChatEndpoint:
    """Test chat endpoint functionality."""
    
    @patch('app.main.groq_client')
    def test_chat_success(self, mock_client, client, mock_groq_response):
        """Test successful chat interaction."""
        # Setup mock
        mock_client.chat.completions.create.return_value = mock_groq_response
        
        # Test request
        response = client.post(
            "/chat",
            json={"message": "Hello AI!"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["reply"] == "Hello! How can I help you today?"
        assert data["model_used"] == "llama-3.1-8b-instant"
        assert data["tokens_used"] == 25
    
    @patch('app.main.groq_client')
    def test_chat_with_custom_parameters(self, mock_client, client, mock_groq_response):
        """Test chat with custom parameters."""
        # Setup mock
        mock_client.chat.completions.create.return_value = mock_groq_response
        
        # Test request with custom parameters
        response = client.post(
            "/chat",
            json={
                "message": "Tell me a joke",
                "model": "mixtral-8x7b-32768",
                "max_tokens": 512,
                "temperature": 0.9
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["model_used"] == "mixtral-8x7b-32768"
        
        # Verify the mock was called with correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["model"] == "mixtral-8x7b-32768"
        assert call_args[1]["max_tokens"] == 512
        assert call_args[1]["temperature"] == 0.9
    
    def test_chat_empty_message(self, client):
        """Test chat with empty message."""
        response = client.post(
            "/chat",
            json={"message": ""}
        )
        assert response.status_code == 422  # Validation error
    
    def test_chat_message_too_long(self, client):
        """Test chat with message that's too long."""
        long_message = "x" * 5000  # Exceeds max length
        response = client.post(
            "/chat",
            json={"message": long_message}
        )
        assert response.status_code == 422  # Validation error
    
    def test_chat_invalid_temperature(self, client):
        """Test chat with invalid temperature."""
        response = client.post(
            "/chat",
            json={
                "message": "Hello",
                "temperature": 3.0  # Invalid temperature
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_chat_invalid_max_tokens(self, client):
        """Test chat with invalid max_tokens."""
        response = client.post(
            "/chat",
            json={
                "message": "Hello",
                "max_tokens": 0  # Invalid max_tokens
            }
        )
        assert response.status_code == 422  # Validation error
    
    @patch('app.main.groq_client')
    def test_chat_groq_api_error(self, mock_client, client):
        """Test chat when Groq API returns an error."""
        # Setup mock to raise an exception
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        response = client.post(
            "/chat",
            json={"message": "Hello"}
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "error" in data["detail"] or "error" in str(data)
    
    @patch('app.main.groq_client', None)
    def test_chat_no_groq_client(self, client):
        """Test chat when Groq client is not available."""
        response = client.post(
            "/chat",
            json={"message": "Hello"}
        )
        
        assert response.status_code == 503
        data = response.json()
        assert "service" in data["detail"].lower() or "available" in data["detail"].lower()


class TestCORSHeaders:
    """Test CORS configuration."""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.options("/chat")
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers
    
    def test_preflight_request(self, client):
        """Test preflight CORS request."""
        response = client.options(
            "/chat",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        assert response.status_code == 200


class TestRequestValidation:
    """Test request validation and error handling."""
    
    def test_invalid_json(self, client):
        """Test request with invalid JSON."""
        response = client.post(
            "/chat",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_message_field(self, client):
        """Test request missing required message field."""
        response = client.post(
            "/chat",
            json={"not_message": "Hello"}
        )
        assert response.status_code == 422
    
    def test_wrong_content_type(self, client):
        """Test request with wrong content type."""
        response = client.post(
            "/chat",
            data="message=Hello",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        # FastAPI should handle this gracefully
        assert response.status_code in [422, 415]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

