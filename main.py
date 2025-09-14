"""
Groq FastAPI Chatbot - Main Application
A complete backend API for AI chatbot using FastAPI and Groq's LLaMA3 model.
"""

import os
import logging
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global Groq client
groq_client: Optional[Groq] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    global groq_client
    
    # Startup
    logger.info("Starting Groq FastAPI Chatbot...")
    
    # Initialize Groq client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY environment variable is not set!")
        raise RuntimeError("GROQ_API_KEY is required")
    
    try:
        groq_client = Groq(api_key=api_key)
        logger.info("Groq client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Groq client: {e}")
        raise RuntimeError(f"Failed to initialize Groq client: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Groq FastAPI Chatbot...")
    groq_client = None


# Initialize FastAPI app
app = FastAPI(
    title="Groq FastAPI Chatbot",
    description="A complete backend API for AI chatbot using FastAPI and Groq's LLaMA3 model",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS - Allow all origins for maximum compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response validation
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(
        ..., 
        min_length=1, 
        max_length=4000,
        description="User message to send to the AI chatbot"
    )
    model: Optional[str] = Field(
        default="llama-3.1-8b-instant",
        description="Groq model to use for the chat"
    )
    max_tokens: Optional[int] = Field(
        default=1024,
        ge=1,
        le=4096,
        description="Maximum number of tokens in the response"
    )
    temperature: Optional[float] = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for response randomness (0.0 = deterministic, 2.0 = very random)"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    model_config = {"protected_namespaces": ()}
    
    reply: str = Field(
        ...,
        description="AI chatbot response"
    )
    model_used: str = Field(
        ...,
        description="The model used for generating the response"
    )
    tokens_used: Optional[int] = Field(
        None,
        description="Number of tokens used in the response"
    )


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")


# API Routes
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Groq FastAPI Chatbot is running!",
        "status": "healthy",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "groq_client": "connected" if groq_client else "disconnected"
    }


@app.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        503: {"model": ErrorResponse, "description": "Service Unavailable"}
    },
    tags=["Chat"]
)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - Send a message to the AI chatbot and get a response.
    
    This endpoint accepts a user message and returns an AI-generated response
    using Groq's LLaMA3 model.
    
    Args:
        request: ChatRequest containing the user message and optional parameters
        
    Returns:
        ChatResponse: Contains the AI response and metadata
        
    Raises:
        HTTPException: For various error conditions (400, 500, 503)
    """
    if not groq_client:
        logger.error("Groq client is not initialized")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Groq service is not available"
        )
    
    try:
        logger.info(f"Processing chat request with model: {request.model}")
        
        # Create chat completion using Groq
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stream=False
        )
        
        # Extract response
        ai_response = chat_completion.choices[0].message.content
        tokens_used = chat_completion.usage.total_tokens if chat_completion.usage else None
        
        logger.info(f"Chat response generated successfully. Tokens used: {tokens_used}")
        
        return ChatResponse(
            reply=ai_response,
            model_used=request.model,
            tokens_used=tokens_used
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        
        # Handle specific Groq API errors
        if "invalid_api_key" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Groq API key"
            )
        elif "rate_limit" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
        elif "model" in str(e).lower() and "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Model '{request.model}' is not available"
            )
        else:
            # Generic server error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing your request"
            )


@app.get("/models", tags=["Models"])
async def get_available_models():
    """Get list of available Groq models."""
    if not groq_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Groq service is not available"
        )
    
    try:
        # Common Groq models (as of 2024)
        available_models = [
            {
                "id": "llama-3.1-8b-instant",
                "name": "LLaMA3 8B",
                "description": "Fast and efficient model for general conversations"
            },
            {
                "id": "llama3-70b-8192", 
                "name": "LLaMA3 70B",
                "description": "More powerful model for complex tasks"
            },
            {
                "id": "mixtral-8x7b-32768",
                "name": "Mixtral 8x7B",
                "description": "High-performance mixture of experts model"
            },
            {
                "id": "gemma-7b-it",
                "name": "Gemma 7B",
                "description": "Google's Gemma model for instruction following"
            }
        ]
        
        return {"models": available_models}
        
    except Exception as e:
        logger.error(f"Error fetching models: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch available models"
        )


# Custom exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    logger.error(f"ValueError: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid input", "detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "An unexpected error occurred"}
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

