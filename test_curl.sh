#!/bin/bash
# Groq FastAPI Chatbot - cURL Testing Examples
# This script demonstrates how to test the API using cURL commands

set -e  # Exit on any error

# Configuration
BASE_URL="http://localhost:8000"
CONTENT_TYPE="Content-Type: application/json"

echo "🤖 Groq FastAPI Chatbot - cURL Test Script"
echo "=========================================="

# Function to make a pretty JSON output
pretty_json() {
    if command -v jq &> /dev/null; then
        echo "$1" | jq .
    else
        echo "$1"
    fi
}

# Function to test endpoint with error handling
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo ""
    echo "Testing: $description"
    echo "Endpoint: $method $endpoint"
    echo "----------------------------------------"
    
    if [ -n "$data" ]; then
        echo "Request data: $data"
        echo ""
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" \
                       -H "$CONTENT_TYPE" \
                       -d "$data" \
                       -w "\nHTTP_STATUS:%{http_code}")
    else
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" \
                       -w "\nHTTP_STATUS:%{http_code}")
    fi
    
    # Extract HTTP status and body
    http_status=$(echo "$response" | grep "HTTP_STATUS:" | cut -d: -f2)
    body=$(echo "$response" | sed '/HTTP_STATUS:/d')
    
    echo "HTTP Status: $http_status"
    echo "Response:"
    pretty_json "$body"
    
    if [ "$http_status" -ge 200 ] && [ "$http_status" -lt 300 ]; then
        echo "✅ Success"
    else
        echo "❌ Failed"
    fi
    
    echo ""
}

# Check if server is running
echo "Checking if server is running at $BASE_URL..."
if ! curl -s "$BASE_URL/health" > /dev/null; then
    echo "❌ Server is not running at $BASE_URL"
    echo "Please start the server first:"
    echo "  python run.py"
    echo "  # or"
    echo "  uvicorn app.main:app --host 0.0.0.0 --port 8000"
    exit 1
fi
echo "✅ Server is running"

# Test 1: Root endpoint
test_endpoint "GET" "/" "" "Root endpoint health check"

# Test 2: Health check
test_endpoint "GET" "/health" "" "Health check endpoint"

# Test 3: Get available models
test_endpoint "GET" "/models" "" "Get available models"

# Test 4: Simple chat
test_endpoint "POST" "/chat" \
    '{"message": "Hello! Can you tell me a short joke?"}' \
    "Simple chat message"

# Test 5: Chat with custom parameters
test_endpoint "POST" "/chat" \
    '{"message": "Explain machine learning in one sentence.", "model": "mixtral-8x7b-32768", "max_tokens": 100, "temperature": 0.5}' \
    "Chat with custom parameters"

# Test 6: Chat with different model
test_endpoint "POST" "/chat" \
    '{"message": "What is the capital of France?", "model": "llama3-70b-8192"}' \
    "Chat with LLaMA3 70B model"

# Test 7: Error cases
echo ""
echo "🔍 Testing Error Cases"
echo "====================="

# Empty message
test_endpoint "POST" "/chat" \
    '{"message": ""}' \
    "Empty message (should fail)"

# Missing message field
test_endpoint "POST" "/chat" \
    '{"text": "Hello"}' \
    "Missing message field (should fail)"

# Invalid model
test_endpoint "POST" "/chat" \
    '{"message": "Hello", "model": "invalid-model"}' \
    "Invalid model name (should fail)"

# Invalid temperature
test_endpoint "POST" "/chat" \
    '{"message": "Hello", "temperature": 3.0}' \
    "Invalid temperature (should fail)"

# Invalid max_tokens
test_endpoint "POST" "/chat" \
    '{"message": "Hello", "max_tokens": 0}' \
    "Invalid max_tokens (should fail)"

# Test 8: CORS preflight request
echo ""
echo "🌐 Testing CORS"
echo "==============="

echo "Testing CORS preflight request..."
cors_response=$(curl -s -X OPTIONS "$BASE_URL/chat" \
                     -H "Origin: http://localhost:3000" \
                     -H "Access-Control-Request-Method: POST" \
                     -H "Access-Control-Request-Headers: Content-Type" \
                     -w "\nHTTP_STATUS:%{http_code}" \
                     -I)

cors_status=$(echo "$cors_response" | grep "HTTP_STATUS:" | cut -d: -f2)
echo "CORS preflight status: $cors_status"

if [ "$cors_status" -eq 200 ]; then
    echo "✅ CORS is properly configured"
else
    echo "❌ CORS configuration issue"
fi

echo ""
echo "🎉 All tests completed!"
echo ""
echo "📚 Additional cURL Examples:"
echo "============================"
echo ""
echo "# Basic chat:"
echo "curl -X POST \"$BASE_URL/chat\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"message\": \"Hello AI!\"}'"
echo ""
echo "# Chat with custom parameters:"
echo "curl -X POST \"$BASE_URL/chat\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"message\": \"Tell me about AI\", \"model\": \"mixtral-8x7b-32768\", \"max_tokens\": 500, \"temperature\": 0.8}'"
echo ""
echo "# Get available models:"
echo "curl -X GET \"$BASE_URL/models\""
echo ""
echo "# Health check:"
echo "curl -X GET \"$BASE_URL/health\""

