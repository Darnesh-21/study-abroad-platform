# Deployment Guide

## Overview

This guide covers deploying the Study Abroad Platform to production.

## Deployment Options

### Option 1: Vercel (Frontend) + Render (Backend) [Recommended]

#### Backend on Render

1. **Create Render Account**
   - Visit https://render.com
   - Sign up with GitHub

2. **Create PostgreSQL Database**
   - Dashboard → New → PostgreSQL
   - Name: study-abroad-db
   - Copy the Internal Database URL

3. **Create Web Service**
   - Dashboard → New → Web Service
   - Connect your repository
   - Settings:
     - Name: study-abroad-api
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   ```
   DATABASE_URL=<your-postgres-url>
   SECRET_KEY=<generate-strong-random-key>
   GEMINI_API_KEY=<your-gemini-key>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment
   - Copy the service URL (e.g., https://study-abroad-api.onrender.com)

#### Frontend on Vercel

1. **Create Vercel Account**
   - Visit https://vercel.com
   - Sign up with GitHub

2. **Import Project**
   - Dashboard → New Project
   - Import your GitHub repository
   - Select `frontend` directory as root

3. **Configure**
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`

4. **Add Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://study-abroad-api.onrender.com/api
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for build
   - Your site will be live at: https://your-app.vercel.app

### Option 2: Railway (Full Stack)

1. **Create Railway Account**
   - Visit https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Dashboard → New Project → Deploy from GitHub

3. **Add PostgreSQL**
   - Add service → Database → PostgreSQL

4. **Deploy Backend**
   - Add service → GitHub Repo
   - Select your repository
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables (same as Render)

5. **Deploy Frontend**
   - Add service → GitHub Repo
   - Select your repository
   - Root Directory: `frontend`
   - Add NEXT_PUBLIC_API_URL pointing to backend service

### Option 3: AWS/Azure/GCP

#### AWS Setup

**Backend (EC2 + RDS)**:
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip postgresql-client

# Clone repository
git clone <your-repo>
cd study-abroad-platform/backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup systemd service
sudo nano /etc/systemd/system/study-abroad.service
```

Service file:
```ini
[Unit]
Description=Study Abroad API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/study-abroad-platform/backend
Environment="PATH=/home/ubuntu/study-abroad-platform/backend/venv/bin"
EnvironmentFile=/home/ubuntu/study-abroad-platform/backend/.env
ExecStart=/home/ubuntu/study-abroad-platform/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl start study-abroad
sudo systemctl enable study-abroad
```

**Frontend (S3 + CloudFront)**:
```bash
# Build
npm run build

# Upload to S3
aws s3 sync out/ s3://your-bucket-name

# Configure CloudFront distribution
```

## Environment Variables

### Production Backend (.env)

```env
# Database (Use production database URL)
DATABASE_URL=postgresql://user:password@host:5432/database

# Security (CRITICAL: Change these!)
SECRET_KEY=<use-openssl-rand-hex-64>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI
GEMINI_API_KEY=<your-gemini-api-key>

# CORS (Update with your frontend domain)
ALLOWED_ORIGINS=https://your-domain.com
```

### Production Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.com/api
```

## Pre-Deployment Checklist

### Backend
- [ ] Update SECRET_KEY to strong random value
- [ ] Configure production database
- [ ] Set up CORS for production frontend
- [ ] Test all API endpoints
- [ ] Verify Gemini API key works
- [ ] Seed university data
- [ ] Enable HTTPS
- [ ] Set up monitoring

### Frontend
- [ ] Update API_URL to production backend
- [ ] Build and test production build locally
- [ ] Check for console errors
- [ ] Test authentication flow
- [ ] Verify all pages load correctly
- [ ] Test responsive design
- [ ] Enable analytics (optional)

## Security Best Practices

1. **Never commit .env files**
   - Add to .gitignore
   - Use environment variables in deployment platform

2. **Use Strong Secret Keys**
   ```bash
   # Generate secret key
   openssl rand -hex 64
   ```

3. **Enable HTTPS**
   - Render/Vercel provide automatic HTTPS
   - For custom domains, use Let's Encrypt

4. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Restrict IP access

5. **API Rate Limiting**
   - Add rate limiting middleware
   - Protect against abuse

## Post-Deployment

### 1. Seed Database

```bash
# Visit in browser or use curl
curl https://your-backend-url.com/api/universities/seed
```

### 2. Test Complete Flow

1. Visit frontend URL
2. Sign up new account
3. Complete onboarding
4. View dashboard
5. Test AI counselor
6. Shortlist universities

### 3. Monitor Logs

**Render**:
- Dashboard → Service → Logs

**Vercel**:
- Dashboard → Deployment → Function Logs

**Railway**:
- Service → Logs

### 4. Set Up Monitoring

- Sentry for error tracking
- Google Analytics for user tracking
- Uptime monitoring (UptimeRobot)

## Scaling Considerations

### Backend
- Add Redis for caching
- Use CDN for static files
- Implement connection pooling
- Add background job queue

### Frontend
- Enable Next.js Image Optimization
- Use CDN for assets
- Implement lazy loading
- Add service worker for offline support

### Database
- Set up read replicas
- Enable connection pooling
- Add database indexes
- Regular backups

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: curl ${{ secrets.RENDER_DEPLOY_HOOK }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

## Domain Setup

### Custom Domain

1. **Purchase Domain** (Namecheap, GoDaddy, etc.)

2. **Configure DNS**
   - Frontend: CNAME to Vercel
   - Backend: CNAME to Render

3. **Update Environment Variables**
   - Update CORS in backend
   - Update API URL in frontend

## Troubleshooting

### Database Connection Issues
- Check DATABASE_URL format
- Verify database is accessible
- Check firewall rules

### API CORS Errors
- Update CORS origins in FastAPI
- Check frontend API URL

### Build Failures
- Check dependency versions
- Verify environment variables
- Review build logs

## Costs Estimate

### Free Tier Options
- Vercel: Free for personal projects
- Render: Free tier available (sleeps after inactivity)
- Railway: $5 credit/month
- Gemini AI: Free tier with limits

### Paid Options
- Render Pro: $7/month (backend)
- Vercel Pro: $20/month (frontend)
- Database: $7-20/month
- **Total**: ~$35-50/month

## Maintenance

### Regular Tasks
- Monitor error logs
- Update dependencies
- Backup database
- Review API usage
- Update university data
- Monitor AI API costs

### Updates
```bash
# Backend
pip list --outdated
pip install --upgrade <package>

# Frontend
npm outdated
npm update
```

## Support Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- Next.js Docs: https://nextjs.org/docs
- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs

---

**Good luck with your deployment! **
