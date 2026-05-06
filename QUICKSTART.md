# ⚡ Quick Start Guide - CyberSense

Get CyberSense running in 5 minutes!

---

## 🚀 Fastest Path to Running App

### Option 1: Use Pre-built (No Training Required)

```bash
# 1. Clone repo
git clone https://github.com/yourusername/CyberSense-CSE445.git
cd CyberSense-CSE445

# 2. Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

# 3. Run backend (demo mode - no models needed)
python app/main.py
# Backend running at http://localhost:5000

# 4. In new terminal, run frontend
cd frontend
python -m http.server 3000 --directory public
# Frontend running at http://localhost:3000

# 5. Open browser
open http://localhost:3000
```

**Note**: Without models, it runs in DEMO MODE using keyword detection.

---

## 📦 With Trained Models

### Step 1: Train Models (30-45 minutes)

```bash
# Install Jupyter
pip install jupyter notebook

# Run training notebook
jupyter notebook notebooks/Main.ipynb

# Click: Kernel → Restart & Run All
# Wait for all cells to complete
# Models saved to backend/models/
```

### Step 2: Verify Models

```bash
ls -lh backend/models/

# You should see:
# best_model.joblib
# tfidf_vectorizer.joblib
```

### Step 3: Run App (Same as Option 1, steps 3-5)

---

## 🌐 Deploy to Production

### Backend (Render) - 5 minutes

1. Go to [render.com](https://render.com)
2. New Web Service → Connect GitHub repo
3. Configure:
   - Root: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app.main:app`
4. Deploy

**Your API**: `https://your-app.onrender.com`

### Frontend (Vercel) - 2 minutes

1. Go to [vercel.com](https://vercel.com)
2. Import GitHub repo
3. Configure:
   - Root: `frontend`
   - Output: `public`
4. Update `frontend/public/index.html` line 283:
   ```javascript
   const API_URL = 'https://your-app.onrender.com/api';
   ```
5. Deploy

**Your App**: `https://your-app.vercel.app`

---

## ✅ Verification

### Test Backend
```bash
curl http://localhost:5000/api/health
# Should return: {"status": "healthy"}
```

### Test Frontend
1. Open `http://localhost:3000`
2. Type: "You are amazing!"
3. Click "Analyze Text"
4. Should show: ✅ No Cyberbullying Detected

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | `pip install -r requirements.txt` |
| NLTK data missing | `python -c "import nltk; nltk.download('all')"` |
| Port in use | Change port: `python app/main.py` → edit code to use 5001 |
| Can't connect | Check firewall, verify URL |
| CORS error | Update CORS origins in `backend/app/main.py` |

---

## 📚 Next Steps

1. ✅ Read [README.md](README.md) for full documentation
2. ✅ Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
3. ✅ Read [TESTING.md](TESTING.md) for testing guide
4. ✅ Train better models with Main.ipynb
5. ✅ Customize the UI
6. ✅ Add new features

---

## 📧 Need Help?

- Check [TROUBLESHOOTING.md](README.md#troubleshooting)
- Review logs: `backend/` or Render dashboard
- Create GitHub issue
- Read documentation

---

**Time to first prediction**: ~5 minutes ⚡
**Time to production**: ~15 minutes 🚀
