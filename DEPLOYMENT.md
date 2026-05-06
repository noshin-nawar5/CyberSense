# 🚀 Deployment Guide - CyberSense

Complete step-by-step guide to deploy CyberSense to production.

---

## 📋 Pre-Deployment Checklist

- [ ] Models trained and saved
- [ ] Backend tested locally
- [ ] Frontend tested locally
- [ ] GitHub repository created
- [ ] Render account created
- [ ] Vercel account created

---

## Part 1: Backend Deployment to Render

### Step 1: Prepare Your Repository

1. **Push to GitHub**:
```bash
cd CyberSense-CSE445
git init
git add .
git commit -m "Initial commit - CyberSense project"
git branch -M main
git remote add origin https://github.com/yourusername/CyberSense-CSE445.git
git push -u origin main
```

### Step 2: Setup Render

1. **Create Account**: Go to [render.com](https://render.com) and sign up with GitHub

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select `CyberSense-CSE445` repository
   - Click "Connect"

3. **Configure Service**:
   ```
   Name:               cybersense-api
   Region:             Oregon (US West) or closest to you
   Branch:             main
   Root Directory:     backend
   Runtime:            Python 3
   Build Command:      pip install -r requirements.txt
   Start Command:      gunicorn app.main:app --bind 0.0.0.0:$PORT
   ```

4. **Select Plan**:
   - Free tier (for testing)
   - Or Starter ($7/month) for better performance

5. **Environment Variables** (Optional):
   ```
   Add if needed:
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   ```

6. **Advanced Settings**:
   - Auto-Deploy: Yes (deploys on every git push)
   - Health Check Path: `/api/health`

7. **Create Web Service**: Click "Create Web Service"

8. **Wait for Deployment**: 
   - Monitor build logs
   - First deployment takes 5-10 minutes
   - You'll get a URL like: `https://cybersense-api.onrender.com`

### Step 3: Upload Model Files

Since model files are too large for Git, you have 3 options:

#### Option A: Render Disk Storage (Recommended)

1. Go to your service dashboard
2. Click "Disks" in left sidebar
3. Create a new disk:
   ```
   Name: models-disk
   Mount Path: /opt/render/project/src/backend/models
   Size: 1GB
   ```
4. Upload models via Render Shell or SFTP

#### Option B: Download from External Storage

1. Upload models to Google Drive/Dropbox
2. Create download script in `backend/download_models.py`:

```python
import requests
import os

def download_model(url, filename):
    """Download model from external storage"""
    response = requests.get(url)
    filepath = os.path.join('models', filename)
    with open(filepath, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")

# Add your model URLs
MODELS = {
    'best_model.joblib': 'YOUR_GOOGLE_DRIVE_LINK',
    'tfidf_vectorizer.joblib': 'YOUR_GOOGLE_DRIVE_LINK',
}

if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    for filename, url in MODELS.items():
        download_model(url, filename)
```

3. Update Build Command:
```
pip install -r requirements.txt && python download_models.py
```

#### Option C: Git LFS (Large File Storage)

1. Install Git LFS locally:
```bash
git lfs install
```

2. Track model files:
```bash
git lfs track "*.joblib"
git add .gitattributes
```

3. Add and commit models:
```bash
git add backend/models/*.joblib
git commit -m "Add model files"
git push
```

### Step 4: Test Backend

```bash
# Test health endpoint
curl https://cybersense-api.onrender.com/api/health

# Test prediction
curl -X POST https://cybersense-api.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test message"}'
```

### Step 5: Configure CORS

Update `backend/app/main.py` line 18-24 with your Vercel domain (after frontend deployment):

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://your-app.vercel.app",  # Add your Vercel domain
            "https://*.vercel.app"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

Commit and push:
```bash
git add backend/app/main.py
git commit -m "Update CORS configuration"
git push
```

Render will auto-deploy the changes.

---

## Part 2: Frontend Deployment to Vercel

### Step 1: Update API URL

1. Edit `frontend/public/index.html`
2. Find line 283 (inside `<script>` tag)
3. Update API_URL:

```javascript
// BEFORE
const API_URL = 'https://your-backend.onrender.com/api';

// AFTER (use your actual Render URL)
const API_URL = 'https://cybersense-api.onrender.com/api';
```

4. Commit changes:
```bash
git add frontend/public/index.html
git commit -m "Update API URL for production"
git push
```

### Step 2: Deploy to Vercel (Option A - Dashboard)

1. **Create Account**: Go to [vercel.com](https://vercel.com) and sign up with GitHub

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Click "Import"

3. **Configure Project**:
   ```
   Project Name:       cybersense
   Framework Preset:   Other
   Root Directory:     frontend
   Build Command:      (leave empty)
   Output Directory:   public
   Install Command:    (leave empty)
   ```

4. **Environment Variables**: None needed for static site

5. **Deploy**: Click "Deploy"

6. **Wait**: Deployment takes 1-2 minutes

7. **Get URL**: You'll get a URL like `https://cybersense.vercel.app`

### Step 3: Deploy to Vercel (Option B - CLI)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? cybersense
# - In which directory is your code located? ./
# - Want to override settings? Yes
#   - Build Command? (leave empty)
#   - Output Directory? public
#   - Development Command? (leave empty)

# Production deployment
vercel --prod
```

### Step 4: Configure Custom Domain (Optional)

1. Go to Vercel dashboard → Your project → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Wait for SSL certificate (automatic)

### Step 5: Test Frontend

1. Visit your Vercel URL: `https://cybersense.vercel.app`
2. Try example texts
3. Verify predictions work
4. Check browser console for errors

---

## Part 3: Post-Deployment

### 1. Update README

Update these sections in `README.md`:

```markdown
🌐 **Live Demo:** 
- Frontend: https://cybersense.vercel.app
- API: https://cybersense-api.onrender.com
```

### 2. Test Full Flow

```bash
# 1. Open frontend
https://cybersense.vercel.app

# 2. Enter test text
"You're amazing! Keep it up!"

# 3. Click Analyze

# 4. Verify result shows
✅ No Cyberbullying Detected
Confidence: 95%
```

### 3. Monitor Performance

**Render Dashboard**:
- Check logs for errors
- Monitor response times
- Set up alerts

**Vercel Dashboard**:
- Check analytics
- Monitor page speed
- Review deployment logs

### 4. Set Up Monitoring (Optional)

**Backend Health Check**:
```bash
# Add to cron or monitoring service
curl https://cybersense-api.onrender.com/api/health
```

**UptimeRobot** (Free):
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Add monitor for your API
3. Get alerts if API goes down

---

## Part 4: Continuous Deployment

### Automatic Deployments

Both Render and Vercel auto-deploy on git push:

```bash
# Make changes
vim frontend/public/index.html

# Commit and push
git add .
git commit -m "Update UI styling"
git push

# Vercel and Render automatically deploy
```

### Manual Deployments

**Render**:
1. Go to dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

**Vercel**:
```bash
cd frontend
vercel --prod
```

---

## Part 5: Troubleshooting

### Backend Issues

#### Issue: Build Failed
**Check**:
- `requirements.txt` is correct
- All imports are available
- Python version matches `runtime.txt`

**Solution**:
```bash
# Test locally first
cd backend
pip install -r requirements.txt
python app/main.py
```

#### Issue: Models Not Loading
**Check**:
- Models are in `backend/models/`
- File permissions are correct
- Disk is mounted (if using Render Disk)

**Solution**:
- Verify in Render Shell:
```bash
ls -la backend/models/
```

#### Issue: CORS Errors
**Check**:
- CORS origins include your Vercel domain
- Vercel URL is correct (https, not http)

**Solution**:
```python
# In main.py, add both with and without subdomain
"origins": [
    "https://cybersense.vercel.app",
    "https://*.vercel.app"
]
```

### Frontend Issues

#### Issue: API Not Reachable
**Check**:
- Backend is running (check Render)
- API_URL is correct in index.html
- CORS is configured

**Solution**:
```javascript
// Test in browser console
fetch('https://cybersense-api.onrender.com/api/health')
  .then(r => r.json())
  .then(console.log)
```

#### Issue: Predictions Not Displaying
**Check**:
- Browser console for JavaScript errors
- Network tab for failed requests
- Response format matches expected structure

**Solution**:
- Add console.log in JavaScript
- Check API response format

---

## Part 6: Free Tier Limitations

### Render Free Tier

- ✅ 750 hours/month
- ✅ Automatic HTTPS
- ⚠️ Spins down after 15 min inactivity
- ⚠️ Cold start takes 30-60 seconds
- ⚠️ No custom domains on free tier

**Workaround for cold starts**:
- Use cron job to ping every 14 minutes
- Upgrade to paid plan ($7/month)

### Vercel Free Tier

- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Custom domains
- ✅ No cold starts (static site)

---

## Part 7: Scaling & Optimization

### Backend Optimization

1. **Add Caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def predict_text(text):
    # Prediction logic
    pass
```

2. **Add Rate Limiting**:
```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/predict', methods=['POST'])
@limiter.limit("10 per minute")
def predict():
    # Prediction logic
    pass
```

3. **Enable Gzip**:
```python
from flask_compress import Compress
Compress(app)
```

### Frontend Optimization

1. **Minify HTML/CSS/JS** (already optimized)
2. **Add Loading States** (already implemented)
3. **Enable CDN** (automatic on Vercel)

---

## Part 8: Cost Estimation

### Free Tier (Recommended for starting)
- **Backend (Render)**: $0
- **Frontend (Vercel)**: $0
- **Total**: $0/month

**Limitations**:
- Cold starts on backend
- 750 hours/month on Render

### Production Tier
- **Backend (Render Starter)**: $7/month
- **Frontend (Vercel Pro)**: $20/month (optional)
- **Total**: $7-27/month

**Benefits**:
- No cold starts
- Better performance
- Custom domains
- More bandwidth

---

## 🎉 Deployment Complete!

Your app is now live:
- **Frontend**: https://cybersense.vercel.app
- **Backend**: https://cybersense-api.onrender.com
- **GitHub**: https://github.com/yourusername/CyberSense-CSE445

### Next Steps:
1. Share with friends and get feedback
2. Monitor usage and performance
3. Add new features
4. Train better models
5. Star the repo ⭐

---

## 📧 Need Help?

- Check logs in Render/Vercel dashboards
- Review error messages carefully
- Test locally first
- Search GitHub issues
- Ask on Stack Overflow with tags: `flask`, `vercel`, `render`

---

**Happy Deploying! 🚀**
