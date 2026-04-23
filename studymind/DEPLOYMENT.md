# StudyMind Deployment Guide

## Quick Deployment Steps

### Option 1: Railway.app (Recommended - Easiest)

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy Project**
   ```bash
   npm i -g @railway/cli
   railway login
   cd studymind
   railway up
   ```

3. **Set Environment Variables**
   ```bash
   railway variables
   ```
   Add:
   - `OPENAI_API_KEY=sk-...`
   - `SECRET_KEY=your-secret-key`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-domain.railway.app`

4. **Your app is live!**
   Railway automatically assigns a domain.

### Option 2: Render.com

1. **Push to GitHub**
2. **Create Render Account**: https://render.com
3. **New Web Service** → Connect GitHub repo
4. **Configure:**
   - Runtime: Python 3.11
   - Build: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - Start: `gunicorn studymind_project.wsgi`
5. **Add environment variables**
6. **Deploy**

### Option 3: PythonAnywhere

1. **Create Account**: https://www.pythonanywhere.com
2. **Upload your code**
3. **Create Web App** (Django 4.2)
4. **Point to your code directory**
5. **Set environment variables**
6. **Reload**

## Environment Variables

```env
# Django Settings
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# OpenAI
OPENAI_API_KEY=sk-your-api-key

# Optional Database
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

## Post-Deployment

1. **Create Admin User**
   ```bash
   python manage.py createsuperuser
   ```

2. **Visit Admin Panel**
   - Go to `/admin`
   - Log in with your credentials

3. **Test Features**
   - Register a new account
   - Create a study material
   - Test AI features

## Monitoring

Railway provides:
- Build logs
- Deployment logs
- Environment variable management
- Auto-scaling
- Error tracking

## Custom Domain

1. In Railway dashboard
2. Go to Settings
3. Add custom domain
4. Update DNS records as instructed

## Cost Estimates

- **Railway**: Free tier available, scales as needed
- **Render**: Free tier for static sites, paid for dynamic
- **PythonAnywhere**: Free tier limited, paid plans from $5/month

## Support

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- PythonAnywhere Help: https://help.pythonanywhere.com
