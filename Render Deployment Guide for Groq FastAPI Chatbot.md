# Render Deployment Guide for Groq FastAPI Chatbot

This guide provides step-by-step instructions for deploying your Groq FastAPI Chatbot to Render, a modern cloud platform that makes deployment simple and scalable.

## 🌐 Why Render?

Render is an excellent choice for deploying FastAPI applications because it offers:
- **Free tier available** with automatic SSL certificates
- **Git-based deployments** with automatic builds
- **Environment variable management** for secure API key storage
- **Health check monitoring** with automatic restarts
- **Custom domains** and scaling options
- **Zero-downtime deployments** with rollback capabilities

## 📋 Prerequisites

Before deploying to Render, ensure you have:

1. **Groq API Key**: Get one from [console.groq.com](https://console.groq.com)
2. **Git Repository**: Your project code in a Git repository (GitHub, GitLab, or Bitbucket)
3. **Render Account**: Sign up at [render.com](https://render.com)

## 🚀 Deployment Methods

### Method 1: Using render.yaml (Recommended)

This method uses the included `render.yaml` file for Infrastructure as Code deployment.

#### Step 1: Prepare Your Repository

1. **Push your code to Git**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Groq FastAPI Chatbot"
   git branch -M main
   git remote add origin https://github.com/yourusername/groq-fastapi-chatbot.git
   git push -u origin main
   ```

2. **Verify render.yaml exists** in your repository root (already included)

#### Step 2: Deploy to Render

1. **Log in to Render Dashboard**: Visit [dashboard.render.com](https://dashboard.render.com)

2. **Create New Service**:
   - Click "New +" button
   - Select "Blueprint"
   - Connect your Git repository
   - Select the repository containing your chatbot code

3. **Configure Blueprint**:
   - Render will automatically detect the `render.yaml` file
   - Review the service configuration
   - Click "Apply" to create the service

4. **Set Environment Variables**:
   - In the service dashboard, go to "Environment"
   - Add your `GROQ_API_KEY` (this is the only required manual step)
   - Other variables are pre-configured in render.yaml

5. **Deploy**:
   - Render will automatically build and deploy your application
   - Monitor the build logs in the dashboard
   - Once deployed, you'll get a public URL like: `https://your-app-name.onrender.com`

### Method 2: Manual Web Service Creation

If you prefer manual configuration:

#### Step 1: Create Web Service

1. **Go to Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your Git repository
   - Select your repository

#### Step 2: Configure Service

**Basic Settings**:
- **Name**: `groq-fastapi-chatbot` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)

**Build & Deploy Settings**:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Advanced Settings**:
- **Health Check Path**: `/health`
- **Auto-Deploy**: `Yes` (for automatic deployments on git push)

#### Step 3: Environment Variables

Add these environment variables in the Render dashboard:

| Key | Value | Required |
|-----|-------|----------|
| `GROQ_API_KEY` | Your actual Groq API key | ✅ Yes |
| `GROQ_DEFAULT_MODEL` | `llama-3.1-8b-instant` | No |
| `HOST` | `0.0.0.0` | No |
| `DEBUG` | `false` | No |
| `MAX_MESSAGE_LENGTH` | `4000` | No |
| `DEFAULT_MAX_TOKENS` | `1024` | No |
| `DEFAULT_TEMPERATURE` | `0.7` | No |
| `ALLOWED_ORIGINS` | `*` | No |
| `LOG_LEVEL` | `INFO` | No |

#### Step 4: Deploy

1. Click "Create Web Service"
2. Render will build and deploy your application
3. Monitor the deployment in the logs section
4. Once complete, access your API at the provided URL

## 🔧 Configuration Details

### render.yaml Explanation

```yaml
services:
  - type: web                    # Web service type
    name: groq-fastapi-chatbot  # Service name
    env: python                 # Python environment
    plan: free                  # Free tier (upgrade as needed)
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:                    # Environment variables
      - key: GROQ_API_KEY
        sync: false             # Manual entry required
    healthCheckPath: /health    # Health monitoring endpoint
    autoDeploy: true           # Auto-deploy on git push
```

### Port Configuration

Render automatically provides the `$PORT` environment variable. The application is configured to use this port, so no manual port configuration is needed.

### Health Checks

The `/health` endpoint is configured for Render's health monitoring. This ensures:
- Automatic restart if the service becomes unhealthy
- Load balancer health checks
- Deployment verification

## 🌍 Accessing Your Deployed API

Once deployed, your API will be available at:
- **Base URL**: `https://your-service-name.onrender.com`
- **API Documentation**: `https://your-service-name.onrender.com/docs`
- **Health Check**: `https://your-service-name.onrender.com/health`

### Testing Your Deployed API

```bash
# Test the deployed API
curl -X POST "https://your-service-name.onrender.com/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello from Render!"}'

# Check health
curl "https://your-service-name.onrender.com/health"

# View available models
curl "https://your-service-name.onrender.com/models"
```

## 🔒 Security Best Practices

### Environment Variables

1. **Never commit API keys** to your repository
2. **Use Render's environment variables** for sensitive data
3. **Set `sync: false`** for sensitive variables in render.yaml
4. **Regularly rotate API keys** for security

### CORS Configuration

For production, consider restricting CORS origins:

```bash
# In Render environment variables
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### HTTPS

Render automatically provides SSL certificates for all services, ensuring your API is served over HTTPS.

## 📊 Monitoring and Maintenance

### Render Dashboard Features

1. **Deployment Logs**: Monitor build and runtime logs
2. **Metrics**: View CPU, memory, and request metrics
3. **Health Checks**: Monitor service health status
4. **Environment Variables**: Manage configuration securely
5. **Custom Domains**: Add your own domain names

### Automatic Deployments

With `autoDeploy: true`, Render will automatically:
- Build and deploy when you push to the main branch
- Run health checks before switching traffic
- Provide rollback capabilities if deployment fails

### Scaling

Render offers easy scaling options:
- **Vertical Scaling**: Upgrade to higher-tier plans for more resources
- **Horizontal Scaling**: Add multiple instances (paid plans)
- **Auto-scaling**: Automatic scaling based on traffic (enterprise plans)

## 🐛 Troubleshooting

### Common Issues

#### 1. Build Failures

**Problem**: Dependencies fail to install
```
Solution: Check requirements.txt format and Python version compatibility
```

#### 2. Start Command Errors

**Problem**: Application fails to start
```
Solution: Verify the start command matches your project structure:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### 3. Environment Variable Issues

**Problem**: GROQ_API_KEY not found
```
Solution: 
1. Check environment variables in Render dashboard
2. Ensure GROQ_API_KEY is set and not empty
3. Verify API key is valid at console.groq.com
```

#### 4. Health Check Failures

**Problem**: Service marked as unhealthy
```
Solution:
1. Check /health endpoint returns 200 status
2. Verify application is listening on correct port
3. Review application logs for errors
```

### Debugging Steps

1. **Check Build Logs**:
   - Go to Render dashboard
   - Select your service
   - View "Events" tab for build logs

2. **Monitor Runtime Logs**:
   - Check "Logs" tab for runtime errors
   - Look for startup messages and error traces

3. **Test Health Endpoint**:
   ```bash
   curl https://your-service-name.onrender.com/health
   ```

4. **Verify Environment Variables**:
   - Check "Environment" tab in dashboard
   - Ensure all required variables are set

## 💰 Pricing and Plans

### Free Tier Limitations

Render's free tier includes:
- **750 hours/month** of runtime
- **Automatic sleep** after 15 minutes of inactivity
- **Cold start delays** when waking from sleep
- **Limited bandwidth** and storage

### Upgrading for Production

For production use, consider upgrading to:
- **Starter Plan ($7/month)**: No sleep, faster builds
- **Standard Plan ($25/month)**: More resources, better performance
- **Pro Plan ($85/month)**: High performance, priority support

## 🔄 Continuous Deployment

### Automatic Deployments

With the current configuration, deployments happen automatically when you:
1. Push code to your main branch
2. Render detects changes
3. Builds and tests the new version
4. Deploys with zero downtime

### Manual Deployments

You can also trigger manual deployments:
1. Go to your service dashboard
2. Click "Manual Deploy"
3. Select the branch/commit to deploy

## 🌐 Custom Domains

### Adding Your Domain

1. **In Render Dashboard**:
   - Go to your service settings
   - Click "Custom Domains"
   - Add your domain (e.g., `api.yourdomain.com`)

2. **Configure DNS**:
   - Add CNAME record pointing to your Render service
   - Render will automatically provision SSL certificate

3. **Update CORS** (if needed):
   ```bash
   ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
   ```

## 📈 Performance Optimization

### Render-Specific Optimizations

1. **Choose Optimal Region**: Select region closest to your users
2. **Use Appropriate Plan**: Upgrade for better performance
3. **Enable Persistent Disks**: For file storage (if needed)
4. **Configure Health Checks**: Ensure proper monitoring

### Application Optimizations

1. **Connection Pooling**: Already configured in the application
2. **Async Operations**: FastAPI handles this automatically
3. **Response Caching**: Consider implementing for repeated queries
4. **Request Validation**: Already implemented with Pydantic

## 🎯 Production Checklist

Before going live, ensure:

- [ ] **API Key Configured**: GROQ_API_KEY set in environment variables
- [ ] **Health Checks Working**: `/health` endpoint returns 200
- [ ] **CORS Configured**: Appropriate origins allowed
- [ ] **Error Handling Tested**: API handles errors gracefully
- [ ] **Documentation Updated**: API docs accessible at `/docs`
- [ ] **Monitoring Setup**: Render dashboard configured
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

## 📞 Support Resources

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **Render Community**: [community.render.com](https://community.render.com)
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Groq Documentation**: [console.groq.com/docs](https://console.groq.com/docs)

Your Groq FastAPI Chatbot is now ready for production deployment on Render! 🎉

