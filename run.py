#!/usr/bin/env python3
"""
Startup script for Groq FastAPI Chatbot.
This script provides an easy way to run the application with proper configuration.
"""

import os
import sys
import argparse
import uvicorn
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.config import settings, validate_settings


def main():
    """Main function to start the FastAPI application."""
    parser = argparse.ArgumentParser(description="Groq FastAPI Chatbot Server")
    parser.add_argument(
        "--host", 
        default=settings.host, 
        help=f"Host to bind to (default: {settings.host})"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=settings.port, 
        help=f"Port to bind to (default: {settings.port})"
    )
    parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development"
    )
    parser.add_argument(
        "--log-level", 
        default=settings.log_level.lower(), 
        choices=["critical", "error", "warning", "info", "debug"],
        help=f"Log level (default: {settings.log_level.lower()})"
    )
    
    args = parser.parse_args()
    
    # Validate settings
    print("🔍 Validating configuration...")
    if not validate_settings():
        print("❌ Configuration validation failed!")
        sys.exit(1)
    
    print("✅ Configuration validated successfully!")
    print(f"🚀 Starting Groq FastAPI Chatbot on {args.host}:{args.port}")
    print(f"📚 API Documentation: http://{args.host}:{args.port}/docs")
    print(f"🔄 Auto-reload: {'enabled' if args.reload else 'disabled'}")
    print(f"📝 Log level: {args.log_level.upper()}")
    
    # Start the server
    try:
        uvicorn.run(
            "app.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level=args.log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

