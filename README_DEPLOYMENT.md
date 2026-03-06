# 🚀 Deployment Guide for AI Travel Planner

## 📋 Environment Variables Setup

The AI Travel Planner requires API keys to function properly. Since `.env` files are not committed to Git (for security), you need to configure environment variables for deployment.

## 🔧 Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. **Deploy to Streamlit Cloud**
   - Connect your GitHub repository to Streamlit Cloud
   - Go to your app dashboard → Settings → Secrets

2. **Add Environment Variables**
   ```
   MISTRAL_API_KEY = aHAM6Ln9Tok4QakqqmnJx7hpn23va1oB
   ```

3. **Alternative: Use secrets.toml**
   - The `.streamlit/secrets.toml` file is already configured
   - Streamlit Cloud will automatically use these secrets

### Option 2: Other Platforms (Heroku, Vercel, etc.)

1. **Set Environment Variables** in your deployment platform:
   ```
   MISTRAL_API_KEY=aHAM6Ln9Tok4QakqqmnJx7hpn23va1oB
   ```

2. **Ensure `.env` is not required** - the app will use platform environment variables

### Option 3: Docker Deployment

1. **Create environment file**:
   ```bash
   cp .env.example .env.production
   # Add your API key to .env.production
   ```

2. **Use environment variables** in Docker:
   ```dockerfile
   ENV MISTRAL_API_KEY=aHAM6Ln9Tok4QakqqmnJx7hpn23va1oB
   ```

## 🔍 Troubleshooting

### Issue: "AI not working" on deployed version
**Solution**: Configure environment variables as shown above

### Issue: "API key not found" error
**Solution**: Add `MISTRAL_API_KEY` to your deployment platform secrets

### Issue: "Fallback mode only"
**Solution**: Ensure environment variables are properly set and restart the app

## ✅ Verification

After deployment, test the AI functionality:
1. Open the deployed app
2. Type: "Plan a 3-day trip to Paris"
3. Should generate AI-powered travel plan (not fallback data)

## 🛡️ Security Notes

- Never commit real API keys to Git
- Use platform secrets management
- Rotate API keys periodically
- Monitor API usage and costs

## 🌟 Quick Start for Streamlit Cloud

1. Push code to GitHub ✅ (already done)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository: `Abh1neshSingh/AI-Travel-Planner`
4. Add main file: `app.py`
5. Add secrets: `MISTRAL_API_KEY=aHAM6Ln9Tok4QakqqmnJx7hpn23va1oB`
6. Deploy! 🚀
