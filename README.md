# 🛡️ CyberSense - Cyberbullying Detection System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)

An AI-powered cyberbullying detection platform that classifies harmful online text using Machine Learning and Deep Learning models, integrated with a modern web interface.

🌐 **Live Demo:** [Frontend on Vercel](https://your-app.vercel.app) | [API on Render](https://your-api.onrender.com)

---

## 📌 Project Overview

Cyberbullying is a growing issue across social media, gaming platforms, and online communities. CyberSense uses advanced NLP and ML techniques to automatically detect harmful content and help create safer online spaces.

### Key Features

✅ **Binary Classification** - Detects cyberbullying vs non-cyberbullying text  
✅ **Advanced NLP** - Text preprocessing, tokenization, lemmatization  
✅ **Multiple ML Models** - Logistic Regression, SVM, Random Forest, Naive Bayes, Decision Tree  
✅ **Deep Learning** - CNN and LSTM models for sequence analysis  
✅ **Feature Engineering** - TF-IDF, TextBlob sentiment, GloVe embeddings  
✅ **REST API** - Flask backend with comprehensive endpoints  
✅ **Modern UI** - Responsive web interface with real-time predictions  
✅ **Production Ready** - Deployed on Render (Backend) and Vercel (Frontend)

---

## 🏗️ Architecture

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   Frontend      │──────▶│   Backend API   │──────▶│   ML Models     │
│   (Vercel)      │       │   (Render)      │       │   (Joblib)      │
│                 │       │                 │       │                 │
│ - HTML/CSS/JS   │       │ - Flask         │       │ - Scikit-learn  │
│ - Responsive    │       │ - CORS          │       │ - TF-IDF        │
│ - Real-time     │       │ - Preprocessing │       │ - TextBlob      │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

---

## 📁 Project Structure

```
CyberSense-CSE445/
│
├── backend/                      # Backend API (Render)
│   ├── app/
│   │   ├── main.py              # Flask application
│   │   └── preprocessing.py     # Text cleaning module
│   ├── models/                  # Trained models (not in git)
│   │   ├── .gitkeep
│   │   ├── best_model.joblib
│   │   └── tfidf_vectorizer.joblib
│   ├── requirements.txt         # Python dependencies
│   ├── Procfile                 # Render deployment config
│   └── runtime.txt              # Python version
│
├── frontend/                     # Frontend (Vercel)
│   ├── public/
│   │   └── index.html           # Main web interface
│   ├── vercel.json              # Vercel configuration
│   └── package.json             # NPM metadata
│
├── notebooks/
│   └── Main.ipynb               # Training notebook
│
├── data/
│   └── Dataset-updated.csv      # Training dataset (64K samples)
│
├── .gitignore
├── README.md
└── DEPLOYMENT.md                # Detailed deployment guide
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip
- Git
- (Optional) Virtual environment tool

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/CyberSense-CSE445.git
cd CyberSense-CSE445
```

### 2. Train Models (Optional - Skip if using pre-trained)

```bash
cd notebooks
jupyter notebook Main.ipynb
# Run all cells to train models
# Models will be saved to backend/models/
```

### 3. Setup Backend (Local)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"

# Run development server
python app/main.py
```

Backend will run on `http://localhost:5000`

### 4. Setup Frontend (Local)

```bash
cd frontend

# Option 1: Simple HTTP server
python -m http.server 3000 --directory public

# Option 2: Using npm (if you have Node.js)
npm run dev
```

Frontend will run on `http://localhost:3000`

---

## 🌐 Deployment

### Backend Deployment (Render)

1. **Create Render Account**: Go to [render.com](https://render.com)

2. **New Web Service**:
   - Connect your GitHub repository
   - Select the `backend` folder
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app.main:app`

3. **Environment Variables**:
   ```
   PYTHON_VERSION=3.11.9
   ```

4. **Add Model Files**:
   - Upload trained models to Render disk storage
   - Or use model download script (see `MODEL_SETUP.md`)

5. **Deploy**: Click "Create Web Service"

Your API will be available at: `https://your-app.onrender.com`

### Frontend Deployment (Vercel)

1. **Install Vercel CLI** (optional):
   ```bash
   npm install -g vercel
   ```

2. **Deploy via Vercel Dashboard**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Root Directory: `frontend`
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: `public`

3. **Update API URL**:
   - Edit `frontend/public/index.html`
   - Line 283: Change `API_URL` to your Render backend URL
   ```javascript
   const API_URL = 'https://your-backend.onrender.com/api';
   ```

4. **Deploy**: Click "Deploy"

Your frontend will be available at: `https://your-app.vercel.app`

---

## 📊 Dataset

- **Source**: Cyberbullying tweets dataset
- **Size**: 64,076 samples
- **Labels**: `cyberbullying` / `not_cyberbullying`
- **Features**: Text content
- **Location**: `data/Dataset-updated.csv`

---

## 🤖 Models

### Machine Learning Models

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|---------|----------|
| Logistic Regression | 94.2% | 93.8% | 94.5% | 94.1% |
| SVM | 94.5% | 94.1% | 94.8% | 94.4% |
| Random Forest | 93.8% | 93.2% | 94.1% | 93.6% |
| Naive Bayes | 91.5% | 90.8% | 92.1% | 91.4% |
| Decision Tree | 89.2% | 88.5% | 89.8% | 89.1% |

### Deep Learning Models

| Model | Accuracy | Architecture |
|-------|----------|--------------|
| CNN | 93.1% | Conv1D → MaxPooling → Dense |
| LSTM | 92.8% | LSTM → Dropout → Dense |

*Note: Results may vary based on training data and hyperparameters*

---

## 🔌 API Endpoints

### Base URL: `https://your-backend.onrender.com`

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "models": {
    "main_model": true,
    "tfidf_vectorizer": true
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 2. Predict Single Text
```http
POST /api/predict
Content-Type: application/json

{
  "text": "Your text here"
}
```

**Response:**
```json
{
  "prediction": "not_cyberbullying",
  "confidence": 0.95,
  "cleaned_text": "text here",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 3. Batch Prediction
```http
POST /api/batch-predict
Content-Type: application/json

{
  "texts": ["text1", "text2", "text3"]
}
```

**Response:**
```json
{
  "results": [
    {
      "index": 0,
      "prediction": "not_cyberbullying",
      "confidence": 0.95
    }
  ],
  "count": 3,
  "timestamp": "2024-01-01T12:00:00"
}
```

---

## 🧹 Text Preprocessing Pipeline

1. **Lowercasing** - Convert all text to lowercase
2. **URL Removal** - Remove http/https links
3. **Mention/Hashtag Handling** - Remove @ mentions, clean # tags
4. **HTML Entity Removal** - Clean &amp; and similar entities
5. **Contraction Expansion** - Convert "don't" → "do not"
6. **Punctuation Removal** - Remove special characters
7. **Character Normalization** - Reduce repeated characters (looove → loove)
8. **Tokenization** - TreebankWordTokenizer
9. **Stopword Removal** - Remove common words
10. **Lemmatization** - Convert to base form (running → run)

---

## 🧪 Testing

### Test Backend Locally

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test message"}'
```

### Test Frontend

1. Open `http://localhost:3000` in browser
2. Try example texts
3. Check browser console for errors
4. Verify predictions display correctly

---

## 📝 Development

### Adding New Models

1. Train model in `notebooks/Main.ipynb`
2. Save model using joblib:
   ```python
   import joblib
   joblib.dump(model, 'backend/models/your_model.joblib')
   ```
3. Load in `backend/app/main.py`
4. Update inference logic

### Modifying Preprocessing

Edit `backend/app/preprocessing.py`:
- Add new cleaning rules
- Adjust stopwords
- Change tokenization strategy

### Customizing UI

Edit `frontend/public/index.html`:
- Modify styles (CSS in `<style>` tag)
- Update layout (HTML structure)
- Change behavior (JavaScript at bottom)

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: Models not loading  
**Solution**: Ensure model files are in `backend/models/` or configure model download

**Problem**: NLTK data errors  
**Solution**: Run `python -c "import nltk; nltk.download('all')"`

**Problem**: CORS errors  
**Solution**: Update CORS origins in `backend/app/main.py` line 18-24

### Frontend Issues

**Problem**: API not reachable  
**Solution**: Update `API_URL` in `index.html` line 283

**Problem**: Predictions not showing  
**Solution**: Check browser console for errors, verify backend is running

---

## 📚 Technologies Used

### Backend
- **Flask** - Web framework
- **Scikit-learn** - ML models
- **NLTK** - Text preprocessing
- **TextBlob** - Sentiment analysis
- **NumPy/Pandas** - Data processing
- **Joblib** - Model serialization
- **Gunicorn** - Production server

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (custom, no frameworks)
- **Vanilla JavaScript** - Interactivity
- **Fetch API** - HTTP requests

### Deployment
- **Render** - Backend hosting
- **Vercel** - Frontend hosting
- **Git/GitHub** - Version control

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Contributors

- **Your Name** - *Initial work* - [GitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Dataset providers
- Scikit-learn and TensorFlow communities
- CSE445 course instructors
- Open source contributors

---

## 📧 Contact

For questions or feedback:
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)
- Project Link: [https://github.com/yourusername/CyberSense-CSE445](https://github.com/yourusername/CyberSense-CSE445)

---

## 🔮 Future Improvements

- [ ] Multi-class classification (types of cyberbullying)
- [ ] Real-time monitoring dashboard
- [ ] User authentication and history
- [ ] Model retraining pipeline
- [ ] Mobile application
- [ ] Browser extension
- [ ] Multi-language support
- [ ] Explainable AI features

---

**⭐ Star this repo if you find it useful!**
