#!/usr/bin/env python3
"""
Example script to test the Groq FastAPI Chatbot API.
This script demonstrates how to interact with the API programmatically.
"""

import requests
import json
import time
from typing import Dict, Any


class ChatbotAPIClient:
    """Simple client for interacting with the Groq FastAPI Chatbot API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the API client.
        
        Args:
            base_url (str): Base URL of the API server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the API is healthy."""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "unhealthy"}
    
    def get_models(self) -> Dict[str, Any]:
        """Get available models."""
        try:
            response = self.session.get(f"{self.base_url}/models")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def chat(self, message: str, model: str = "llama-3.1-8b-instant", 
             max_tokens: int = 1024, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Send a chat message to the API.
        
        Args:
            message (str): User message
            model (str): Model to use
            max_tokens (int): Maximum tokens in response
            temperature (float): Response randomness
            
        Returns:
            Dict[str, Any]: API response
        """
        try:
            payload = {
                "message": message,
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = self.session.post(
                f"{self.base_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}


def main():
    """Main function to demonstrate API usage."""
    print("🤖 Groq FastAPI Chatbot - API Test Script")
    print("=" * 50)
    
    # Initialize client
    client = ChatbotAPIClient()
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    health = client.health_check()
    print(f"Health status: {json.dumps(health, indent=2)}")
    
    if health.get("status") != "healthy":
        print("❌ API is not healthy. Please check the server.")
        return
    
    # Test 2: Get available models
    print("\n2. Getting available models...")
    models = client.get_models()
    if "error" not in models:
        print("Available models:")
        for model in models.get("models", []):
            print(f"  - {model['id']}: {model['name']}")
    else:
        print(f"Error getting models: {models['error']}")
    
    # Test 3: Simple chat
    print("\n3. Testing simple chat...")
    response = client.chat("Hello! Can you tell me a short joke?")
    if "error" not in response:
        print(f"User: Hello! Can you tell me a short joke?")
        print(f"Bot: {response['reply']}")
        print(f"Model: {response['model_used']}")
        print(f"Tokens: {response.get('tokens_used', 'unknown')}")
    else:
        print(f"Error: {response['error']}")
    
    # Test 4: Chat with different model
    print("\n4. Testing chat with Mixtral model...")
    response = client.chat(
        "Explain quantum computing in simple terms.",
        model="mixtral-8x7b-32768",
        max_tokens=512
    )
    if "error" not in response:
        print(f"User: Explain quantum computing in simple terms.")
        print(f"Bot: {response['reply'][:200]}...")  # Truncate for display
        print(f"Model: {response['model_used']}")
        print(f"Tokens: {response.get('tokens_used', 'unknown')}")
    else:
        print(f"Error: {response['error']}")
    
    # Test 5: Interactive chat
    print("\n5. Interactive chat mode (type 'quit' to exit)...")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
            
            print("Bot: Thinking...")
            start_time = time.time()
            response = client.chat(user_input)
            end_time = time.time()
            
            if "error" not in response:
                print(f"Bot: {response['reply']}")
                print(f"(Model: {response['model_used']}, "
                      f"Tokens: {response.get('tokens_used', 'unknown')}, "
                      f"Time: {end_time - start_time:.2f}s)")
            else:
                print(f"Error: {response['error']}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n👋 Thanks for testing the Groq FastAPI Chatbot!")


if __name__ == "__main__":
    main()

