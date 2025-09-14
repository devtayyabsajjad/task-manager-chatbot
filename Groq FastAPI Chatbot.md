# Groq FastAPI Chatbot

A complete, production-ready backend API for AI chatbot applications using **FastAPI** and **Groq's powerful language models** (LLaMA3, Mixtral). This project provides a robust, scalable, and well-documented foundation for building AI-powered chat applications.

## 🚀 Features

- **FastAPI Framework**: Modern, fast, and automatic API documentation
- **Groq Integration**: Leverage powerful models like LLaMA3 8B/70B and Mixtral 8x7B
- **CORS Enabled**: Ready for frontend integration from any domain
- **Comprehensive Error Handling**: Graceful handling of API errors and edge cases
- **Request Validation**: Automatic input validation using Pydantic models
- **Health Monitoring**: Built-in health check endpoints
- **Docker Support**: Complete containerization with Docker and docker-compose
- **Testing Suite**: Comprehensive test coverage with pytest
- **Production Ready**: Logging, configuration management, and deployment scripts
- **Interactive Documentation**: Auto-generated API docs at `/docs` and `/redoc`

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Endpoints](#-api-endpoints)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ⚡ Quick Start

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd groq-fastapi-chatbot
   pip install -r requirements.txt
   ```

2. **Set your Groq API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

3. **Run the server**:
   ```bash
   python run.py
   ```

4. **Test the API**:
   ```bash
   curl -X POST "http://localhost:8000/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello AI!"}'
   ```

5. **View API documentation**: Open http://localhost:8000/docs

## 🛠 Installation

### Prerequisites

- Python 3.8 or higher
- Groq API key (get one at [console.groq.com](https://console.groq.com))

### Method 1: Local Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd groq-fastapi-chatbot

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env file and add your Groq API key
nano .env  # or use your preferred editor
```

### Method 2: Docker Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd groq-fastapi-chatbot

# Copy environment template
cp .env.example .env

# Edit .env file and add your Groq API key
nano .env

# Build and run with Docker Compose
docker-compose up --build
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# REQUIRED: Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# OPTIONAL: Model Configuration
GROQ_DEFAULT_MODEL=llama-3.1-8b-instant

# OPTIONAL: Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# OPTIONAL: API Limits
MAX_MESSAGE_LENGTH=4000
DEFAULT_MAX_TOKENS=1024
DEFAULT_TEMPERATURE=0.7

# OPTIONAL: CORS Configuration
ALLOWED_ORIGINS=*

# OPTIONAL: Logging
LOG_LEVEL=INFO
```

### Getting a Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up or log in to your account
3. Navigate to the API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file

### Available Models

The API supports the following Groq models:

| Model ID | Name | Description | Max Tokens | Recommended |
|----------|------|-------------|------------|-------------|
| `llama-3.1-8b-instant` | LLaMA3 8B | Fast and efficient for general conversations | 8,192 | ✅ |
| `llama3-70b-8192` | LLaMA3 70B | More powerful for complex tasks | 8,192 | ⚠️ |
| `mixtral-8x7b-32768` | Mixtral 8x7B | High-performance mixture of experts | 32,768 | ✅ |
| `gemma-7b-it` | Gemma 7B | Google's instruction-following model | 8,192 | ⚠️ |

## 📡 API Endpoints

### Base URL
- Local development: `http://localhost:8000`
- Production: Your deployed domain

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint - API status |
| GET | `/health` | Health check |
| GET | `/models` | List available models |
| POST | `/chat` | Main chat endpoint |
| GET | `/docs` | Interactive API documentation |
| GET | `/redoc` | Alternative API documentation |

### POST /chat

The main endpoint for chat interactions.

**Request Body:**
```json
{
  "message": "Hello AI!",
  "model": "llama-3.1-8b-instant",
  "max_tokens": 1024,
  "temperature": 0.7
}
```

**Request Parameters:**
- `message` (required): User message (1-4000 characters)
- `model` (optional): Model to use (default: `llama-3.1-8b-instant`)
- `max_tokens` (optional): Maximum response tokens (1-4096, default: 1024)
- `temperature` (optional): Response randomness 0.0-2.0 (default: 0.7)

**Response:**
```json
{
  "reply": "Hello! How can I help you today?",
  "model_used": "llama-3.1-8b-instant",
  "tokens_used": 25
}
```

**Error Response:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

### GET /models

Returns list of available models.

**Response:**
```json
{
  "models": [
    {
      "id": "llama-3.1-8b-instant",
      "name": "LLaMA3 8B",
      "description": "Fast and efficient model for general conversations"
    }
  ]
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "groq_client": "connected"
}
```

## 💡 Usage Examples

### cURL Examples

```bash
# Basic chat
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello AI!"}'

# Chat with custom parameters
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Explain quantum computing",
       "model": "mixtral-8x7b-32768",
       "max_tokens": 500,
       "temperature": 0.8
     }'

# Get available models
curl -X GET "http://localhost:8000/models"

# Health check
curl -X GET "http://localhost:8000/health"
```

### Python Client Example

```python
import requests

# Initialize client
base_url = "http://localhost:8000"

# Send a chat message
response = requests.post(
    f"{base_url}/chat",
    json={
        "message": "Tell me a joke about programming",
        "model": "llama-3.1-8b-instant",
        "temperature": 0.9
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"AI: {data['reply']}")
    print(f"Tokens used: {data['tokens_used']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### JavaScript/Frontend Example

```javascript
// Fetch API example
async function chatWithAI(message) {
    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                model: 'llama-3.1-8b-instant',
                temperature: 0.7
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('AI Response:', data.reply);
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Usage
chatWithAI("Hello, how are you?")
    .then(response => {
        document.getElementById('chat-response').textContent = response.reply;
    })
    .catch(error => {
        console.error('Chat failed:', error);
    });
```

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py

# Run tests with coverage
pip install pytest-cov
pytest --cov=app tests/
```

### Manual Testing

#### Using the Python Test Script

```bash
# Run the interactive test script
python examples/test_api.py
```

This script will:
1. Check API health
2. List available models
3. Test basic chat functionality
4. Test different models
5. Provide an interactive chat mode

#### Using the cURL Test Script

```bash
# Run comprehensive cURL tests
./examples/test_curl.sh
```

This script tests:
- All API endpoints
- Error handling
- CORS configuration
- Various parameter combinations

### Test Coverage

The test suite covers:
- ✅ All API endpoints
- ✅ Request validation
- ✅ Error handling
- ✅ CORS functionality
- ✅ Utility functions
- ✅ Configuration management
- ✅ Health checks

## 🚀 Deployment

### Local Development

```bash
# Method 1: Using the run script
python run.py

# Method 2: Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Method 3: Using the startup script with custom parameters
python run.py --host 0.0.0.0 --port 8080 --reload --log-level debug
```

### Docker Deployment

```bash
# Build the Docker image
docker build -t groq-fastapi-chatbot .

# Run with Docker
docker run -p 8000:8000 --env-file .env groq-fastapi-chatbot

# Or use Docker Compose
docker-compose up -d
```

### Production Deployment

For production deployment, consider:

1. **Use a production WSGI server** (already configured with uvicorn)
2. **Set up reverse proxy** (nginx recommended)
3. **Configure SSL/TLS certificates**
4. **Set up monitoring and logging**
5. **Configure environment variables securely**
6. **Set up auto-scaling** if needed

#### Example nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Cloud Deployment Options

- **Heroku**: Use the included `Dockerfile`
- **AWS ECS/Fargate**: Deploy using Docker containers
- **Google Cloud Run**: Serverless container deployment
- **DigitalOcean App Platform**: Simple container deployment
- **Railway**: Easy deployment with Git integration
- **Render**: Modern cloud platform with free tier (see detailed guide below)

### Render Deployment (Recommended)

Render offers an excellent free tier for deploying FastAPI applications with automatic SSL and Git-based deployments.

#### Quick Render Deployment

1. **Push to Git Repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy to Render**:
   - Go to [render.com](https://render.com) and sign up
   - Click "New +" → "Blueprint"
   - Connect your Git repository
   - Render will detect the `render.yaml` file automatically
   - Add your `GROQ_API_KEY` in environment variables
   - Click "Apply" to deploy

3. **Access Your API**:
   - Your API will be available at: `https://your-app-name.onrender.com`
   - API docs at: `https://your-app-name.onrender.com/docs`

#### Render Configuration Files Included

- `render.yaml` - Infrastructure as Code configuration
- `RENDER_DEPLOYMENT.md` - Comprehensive deployment guide

For detailed Render deployment instructions, see the [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) guide.

## 🔧 Development

### Project Structure

```
groq-fastapi-chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py          # Main FastAPI application
│   ├── config.py        # Configuration management
│   └── utils.py         # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_main.py     # API endpoint tests
│   └── test_utils.py    # Utility function tests
├── examples/
│   ├── test_api.py      # Python client example
│   └── test_curl.sh     # cURL testing script
├── docs/                # Additional documentation
├── .env.example         # Environment template
├── .gitignore          # Git ignore rules
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── requirements.txt    # Python dependencies
├── run.py             # Application startup script
└── README.md          # This file
```

### Adding New Features

1. **Create feature branch**: `git checkout -b feature/new-feature`
2. **Implement changes** in the appropriate modules
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Test thoroughly** using the provided test scripts
6. **Submit pull request**

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Use meaningful variable and function names

### Adding New Models

To add support for new Groq models:

1. Update the model list in `app/config.py`
2. Update the validation in `app/utils.py`
3. Add tests for the new model
4. Update documentation

## 🔍 Troubleshooting

### Common Issues

#### 1. "GROQ_API_KEY is not set" Error

**Problem**: The API key environment variable is not configured.

**Solution**:
```bash
# Check if .env file exists
ls -la .env

# If not, copy from template
cp .env.example .env

# Edit and add your API key
nano .env
```

#### 2. "Port already in use" Error

**Problem**: Port 8000 is already occupied.

**Solution**:
```bash
# Check what's using the port
lsof -i :8000

# Kill the process or use a different port
python run.py --port 8080
```

#### 3. CORS Issues

**Problem**: Frontend can't access the API due to CORS restrictions.

**Solution**: The API is configured to allow all origins by default. If you're still having issues:

```bash
# Check CORS configuration in .env
ALLOWED_ORIGINS=*

# Or specify specific origins
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

#### 4. Model Not Available Error

**Problem**: Selected model is not available.

**Solution**:
```bash
# Check available models
curl -X GET "http://localhost:8000/models"

# Use a supported model
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello", "model": "llama-3.1-8b-instant"}'
```

#### 5. High Response Times

**Problem**: API responses are slow.

**Solutions**:
- Use faster models (llama-3.1-8b-instant instead of llama3-70b-8192)
- Reduce max_tokens parameter
- Check your internet connection
- Monitor Groq API status

### Debug Mode

Enable debug mode for detailed error information:

```bash
# Set DEBUG=true in .env file
DEBUG=true

# Or run with debug flag
python run.py --log-level debug
```

### Logging

Check application logs for detailed error information:

```bash
# Logs are printed to stdout by default
python run.py

# For Docker deployment
docker-compose logs -f groq-chatbot
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run the test suite**: `pytest`
5. **Update documentation** if needed
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to the branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/groq-fastapi-chatbot.git
cd groq-fastapi-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The amazing web framework
- [Groq](https://groq.com/) - For providing powerful AI models
- [Pydantic](https://pydantic-docs.helpmanual.io/) - For data validation
- [Uvicorn](https://www.uvicorn.org/) - ASGI server implementation

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/yourusername/groq-fastapi-chatbot/issues)
3. Create a new issue with detailed information
4. Join our community discussions

## 🔮 Roadmap

- [ ] Add support for streaming responses
- [ ] Implement conversation history/memory
- [ ] Add user authentication and rate limiting
- [ ] Support for file uploads and multimodal inputs
- [ ] Integration with vector databases for RAG
- [ ] WebSocket support for real-time chat
- [ ] Monitoring and analytics dashboard
- [ ] Multi-language support

---

**Built with ❤️ using FastAPI and Groq**

*Happy coding! 🚀*

