# 🚂 Railway Deployment Guide for Groq FastAPI Chatbot

This guide provides step-by-step instructions for deploying your Groq FastAPI Chatbot to Railway and integrating it with your JavaScript application.

## 🌐 Why Railway?

Railway is an excellent choice for deploying FastAPI applications because it offers:
- **Git-based deployments** with automatic builds
- **Environment variable management** for secure API key storage
- **Automatic HTTPS** certificates
- **Zero-downtime deployments** with rollback capabilities
- **Built-in monitoring** and logs
- **Free tier available** for small projects

## 📋 Prerequisites

Before deploying to Railway, ensure you have:

1. **Groq API Key**: Get one from [console.groq.com](https://console.groq.com)
2. **Git Repository**: Your project code in a Git repository (GitHub, GitLab, or Bitbucket)
3. **Railway Account**: Sign up at [railway.app](https://railway.app)
4. **Railway CLI** (optional): Install from [railway.app/cli](https://railway.app/cli)

## 🚀 Quick Deployment

### Method 1: GitHub/GitLab Integration (Recommended)

1. **Push your code to Git**:
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push origin main
   ```

2. **Connect to Railway**:
   - Go to [railway.app](https://railway.app) and sign in
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository containing the chatbot code
   - Railway will automatically detect the `railway.json` configuration

3. **Configure Environment Variables**:
   - In your Railway project dashboard, go to "Variables"
   - Add your `GROQ_API_KEY` (this is the only required variable)
   - Other variables are pre-configured with sensible defaults

4. **Deploy**:
   - Railway will automatically build and deploy your application
   - Monitor the build logs in the Railway dashboard
   - Once deployed, you'll get a public URL like: `https://your-project.up.railway.app`

### Method 2: Railway CLI

1. **Install Railway CLI**:
   ```bash
   # npm install -g @railway/cli
   # or
   curl -fsSL https://railway.app/install.sh | sh
   ```

2. **Login and deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set environment variables**:
   ```bash
   railway variables set GROQ_API_KEY=your_api_key_here
   ```

## ⚙️ Configuration Details

### railway.json Configuration

The included `railway.json` file configures Railway to:
- Use Nixpacks as the build system
- Run the application with the correct start command
- Set up health checks
- Configure restart policies

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Environment Variables

Set these in your Railway project dashboard:

| Key | Value | Required | Description |
|-----|-------|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes | Required for API access |
| `GROQ_DEFAULT_MODEL` | `llama-3.1-8b-instant` | No | Default AI model |
| `HOST` | `0.0.0.0` | No | Server host (Railway sets this) |
| `DEBUG` | `false` | No | Debug mode |
| `MAX_MESSAGE_LENGTH` | `4000` | No | Maximum message length |
| `DEFAULT_MAX_TOKENS` | `1024` | No | Default response tokens |
| `DEFAULT_TEMPERATURE` | `0.7` | No | Response randomness |
| `ALLOWED_ORIGINS` | `*` | No | CORS origins (see below) |
| `LOG_LEVEL` | `INFO` | No | Logging level |

## 🌍 JavaScript Integration

### CORS Configuration

Your application is already configured to allow all origins (`*`) for maximum compatibility. For production, consider restricting origins:

```bash
# In Railway environment variables
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### JavaScript Client Examples

#### Fetch API Example

```javascript
// Basic chat function
async function chatWithAI(message, options = {}) {
    const response = await fetch('https://your-project.up.railway.app/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message,
            model: options.model || 'llama-3.1-8b-instant',
            max_tokens: options.maxTokens || 1024,
            temperature: options.temperature || 0.7
        })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
}

// Usage
try {
    const response = await chatWithAI("Hello, how are you?");
    console.log('AI Response:', response.reply);
    console.log('Model used:', response.model_used);
    console.log('Tokens used:', response.tokens_used);
} catch (error) {
    console.error('Error:', error);
}
```

#### Axios Example

```javascript
import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'https://your-project.up.railway.app',
    timeout: 30000,
});

export const chatAPI = {
    async sendMessage(message, options = {}) {
        try {
            const response = await apiClient.post('/chat', {
                message,
                model: options.model || 'llama-3.1-8b-instant',
                max_tokens: options.maxTokens || 1024,
                temperature: options.temperature || 0.7
            });
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || error.message);
        }
    },

    async getModels() {
        try {
            const response = await apiClient.get('/models');
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || error.message);
        }
    },

    async healthCheck() {
        try {
            const response = await apiClient.get('/health');
            return response.data;
        } catch (error) {
            throw new Error('Service unavailable');
        }
    }
};
```

#### React Hook Example

```javascript
import { useState, useCallback } from 'react';

export function useChatbot(apiUrl = 'https://your-project.up.railway.app') {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const sendMessage = useCallback(async (message, options = {}) => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`${apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message,
                    ...options
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            return data;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, [apiUrl]);

    return { sendMessage, loading, error };
}
```

#### Vue.js Composition API Example

```javascript
import { ref, computed } from 'vue';

export function useChatbot(apiUrl = 'https://your-project.up.railway.app') {
    const loading = ref(false);
    const error = ref(null);
    const messages = ref([]);

    const sendMessage = async (message, options = {}) => {
        loading.value = true;
        error.value = null;

        try {
            const response = await fetch(`${apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message,
                    ...options
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            messages.value.push({
                id: Date.now(),
                user: message,
                bot: data.reply,
                model: data.model_used,
                tokens: data.tokens_used,
                timestamp: new Date().toISOString()
            });

            return data;
        } catch (err) {
            error.value = err.message;
            throw err;
        } finally {
            loading.value = false;
        }
    };

    return {
        loading: computed(() => loading.value),
        error: computed(() => error.value),
        messages: computed(() => messages.value),
        sendMessage
    };
}
```

## 🧪 Testing Your Deployed API

### Health Check

```bash
curl https://your-project.up.railway.app/health
```

### Get Available Models

```bash
curl https://your-project.up.railway.app/models
```

### Send a Chat Message

```bash
curl -X POST "https://your-project.up.railway.app/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello from Railway!"}'
```

### Advanced Chat Request

```bash
curl -X POST "https://your-project.up.railway.app/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Explain quantum computing in simple terms",
       "model": "mixtral-8x7b-32768",
       "max_tokens": 500,
       "temperature": 0.8
     }'
```

## 📊 Monitoring and Maintenance

### Railway Dashboard Features

1. **Deployment Logs**: Monitor build and runtime logs
2. **Metrics**: View CPU, memory, and request metrics
3. **Environment Variables**: Manage configuration securely
4. **Custom Domains**: Add your own domain names
5. **Database Integration**: Add databases if needed

### Viewing Logs

```bash
# Via Railway CLI
railway logs

# Or view in Railway dashboard
# Go to your project → "Logs" tab
```

### Scaling

Railway automatically scales your application based on traffic. For high-traffic applications, consider:

1. **Upgrade to Pro plan** for more resources
2. **Optimize your code** for better performance
3. **Add caching** for frequently requested data
4. **Monitor usage patterns** to predict scaling needs

## 🔒 Security Best Practices

### Environment Variables

1. **Never commit API keys** to your repository
2. **Use Railway's environment variables** for sensitive data
3. **Regularly rotate API keys** for security
4. **Monitor API usage** in Groq console

### CORS Configuration

For production deployments, configure specific origins:

```bash
# Environment variables
ALLOWED_ORIGINS=https://your-frontend-domain.com,https://app.yourdomain.com
```

### Rate Limiting

Consider implementing rate limiting in your JavaScript application:

```javascript
class RateLimiter {
    constructor(maxRequests = 10, windowMs = 60000) {
        this.requests = [];
        this.maxRequests = maxRequests;
        this.windowMs = windowMs;
    }

    canMakeRequest() {
        const now = Date.now();
        this.requests = this.requests.filter(time => now - time < this.windowMs);

        if (this.requests.length >= this.maxRequests) {
            return false;
        }

        this.requests.push(now);
        return true;
    }
}

const rateLimiter = new RateLimiter();

async function safeChat(message) {
    if (!rateLimiter.canMakeRequest()) {
        throw new Error('Rate limit exceeded. Please wait before sending another message.');
    }

    return await chatWithAI(message);
}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Build Failures

**Problem**: Application fails to build
```
Solution:
1. Check build logs in Railway dashboard
2. Ensure requirements.txt is properly formatted
3. Verify Python version compatibility
4. Check for missing dependencies
```

#### 2. Runtime Errors

**Problem**: Application crashes after deployment
```
Solution:
1. Check application logs in Railway dashboard
2. Verify GROQ_API_KEY is set correctly
3. Test locally with same environment variables
4. Check for port binding issues
```

#### 3. CORS Issues

**Problem**: Frontend can't connect to API
```
Solution:
1. Check ALLOWED_ORIGINS environment variable
2. Verify frontend is using HTTPS (Railway provides SSL)
3. Test API endpoints directly with curl
4. Check browser console for CORS errors
```

#### 4. Timeout Issues

**Problem**: Requests timeout
```
Solution:
1. Increase timeout in JavaScript client
2. Check Railway plan limits
3. Optimize API response times
4. Consider upgrading Railway plan
```

### Debug Commands

```bash
# Check Railway project status
railway status

# View environment variables
railway variables

# Restart deployment
railway up --detach
```

## 💰 Pricing and Plans

### Railway Pricing Tiers

- **Hobby Plan** (Free): 512MB RAM, 1GB disk, limited hours
- **Pro Plan** ($5/month): 1GB RAM, 10GB disk, unlimited hours
- **Team Plans**: Additional resources and collaboration features

### Cost Optimization

1. **Monitor usage** in Railway dashboard
2. **Optimize code** to reduce resource usage
3. **Use appropriate plan** for your needs
4. **Set up alerts** for usage limits

## 🔄 Continuous Deployment

### Git-based Deployments

Railway automatically deploys when you push to your main branch:

```bash
# Make changes
git add .
git commit -m "Improve error handling"
git push origin main

# Railway will automatically deploy the changes
```

### Environment Branches

Create separate Railway projects for different environments:

```bash
# Production: main branch
# Staging: staging branch
# Development: dev branch
```

## 📞 Support Resources

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Railway Community**: [community.railway.app](https://community.railway.app)
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Groq Documentation**: [console.groq.com/docs](https://console.groq.com/docs)

## 🎯 Production Checklist

Before going live, ensure:

- [ ] **API Key Configured**: GROQ_API_KEY set in Railway
- [ ] **Health Checks Working**: `/health` endpoint returns 200
- [ ] **CORS Configured**: Appropriate origins allowed
- [ ] **Error Handling Tested**: API handles errors gracefully
- [ ] **Documentation Updated**: API docs accessible at `/docs`
- [ ] **Monitoring Setup**: Railway dashboard configured
- [ ] **Domain Configured**: Custom domain (if using)
- [ ] **SSL Certificate**: HTTPS working properly
- [ ] **Performance Tested**: API responds within acceptable time
- [ ] **Backup Plan**: Know how to rollback if needed

## 🚀 Next Steps

After successful deployment:

1. **Test All Endpoints**: Verify full functionality
2. **Monitor Performance**: Watch metrics and logs
3. **Set Up Alerts**: Configure notifications for issues
4. **Document API URL**: Share with frontend developers
5. **Plan Scaling**: Monitor usage and upgrade as needed

Your Groq FastAPI Chatbot is now ready for production deployment on Railway! 🎉

---

**Built with ❤️ using FastAPI, Groq, and Railway**
