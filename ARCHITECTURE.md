# 🏗️ CyberSense Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (Browser - Any Device)                       │
└──────────────────────────┬──────────────────────────────────────┘
                          │
                          │ HTTPS
                          │
┌─────────────────────────▼──────────────────────────────────────┐
│                    FRONTEND (Vercel)                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  • HTML/CSS/JavaScript                                  │    │
│  │  • Responsive Design                                    │    │
│  │  • Real-time Predictions                               │    │
│  │  • Error Handling                                       │    │
│  │  • Mobile Friendly                                      │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────┘
                          │
                          │ REST API (JSON)
                          │ CORS Enabled
                          │
┌─────────────────────────▼──────────────────────────────────────┐
│                     BACKEND (Render)                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           Flask REST API (Gunicorn)                    │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │  Endpoints:                                   │     │    │
│  │  │  • GET  /api/health                          │     │    │
│  │  │  • POST /api/predict                         │     │    │
│  │  │  • POST /api/batch-predict                   │     │    │
│  │  └──────────────────────────────────────────────┘     │    │
│  └────────────────────────┬───────────────────────────────┘    │
│                           │                                     │
│  ┌────────────────────────▼───────────────────────────────┐    │
│  │         Text Preprocessing Pipeline                    │    │
│  │  • Lowercasing                                         │    │
│  │  • URL/Mention Removal                                 │    │
│  │  • Tokenization (TreebankWordTokenizer)               │    │
│  │  • Stopword Removal                                    │    │
│  │  • Lemmatization                                       │    │
│  └────────────────────────┬───────────────────────────────┘    │
│                           │                                     │
│  ┌────────────────────────▼───────────────────────────────┐    │
│  │            ML Model Inference                          │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │  Models:                                      │     │    │
│  │  │  • TF-IDF Vectorizer                         │     │    │
│  │  │  • Trained Classifier (SVM/LR/RF)            │     │    │
│  │  │  • SVD (Optional)                             │     │    │
│  │  │  • TextBlob Features (Optional)               │     │    │
│  │  └──────────────────────────────────────────────┘     │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
┌─────────┐
│  User   │
│ Types   │
│  Text   │
└────┬────┘
     │
     │ 1. Submit Text
     ▼
┌─────────────────┐
│   Frontend      │
│  • Validate     │
│  • Show Loading │
└────┬────────────┘
     │
     │ 2. POST /api/predict
     │    { "text": "..." }
     ▼
┌─────────────────────┐
│   Backend API       │
│  • Receive Request  │
│  • Validate Input   │
└────┬────────────────┘
     │
     │ 3. Clean Text
     ▼
┌─────────────────────┐
│  Preprocessing      │
│  • Remove URLs      │
│  • Tokenize         │
│  • Lemmatize        │
└────┬────────────────┘
     │
     │ 4. Transform
     ▼
┌─────────────────────┐
│  Feature Extraction │
│  • TF-IDF           │
│  • SVD (optional)   │
└────┬────────────────┘
     │
     │ 5. Predict
     ▼
┌─────────────────────┐
│   ML Model          │
│  • Classify         │
│  • Get Confidence   │
└────┬────────────────┘
     │
     │ 6. Format Response
     ▼
┌─────────────────────┐
│   Backend API       │
│  • Add Metadata     │
│  • Return JSON      │
└────┬────────────────┘
     │
     │ 7. Response
     │    { "prediction": "...",
     │      "confidence": 0.95 }
     ▼
┌─────────────────────┐
│   Frontend          │
│  • Parse Response   │
│  • Show Result      │
│  • Display UI       │
└────┬────────────────┘
     │
     │ 8. Display
     ▼
┌─────────┐
│  User   │
│  Sees   │
│ Result  │
└─────────┘
```

---

## Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                   │
├─────────────────────────────────────────────────────────┤
│  • HTML5          - Structure                           │
│  • CSS3           - Styling (Dark Theme)                │
│  • JavaScript ES6 - Interactivity                       │
│  • Fetch API      - HTTP Requests                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                    │
├─────────────────────────────────────────────────────────┤
│  • Flask 3.0      - Web Framework                       │
│  • Flask-CORS     - Cross-Origin Support                │
│  • Gunicorn       - WSGI HTTP Server                    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER                     │
├─────────────────────────────────────────────────────────┤
│  • NLTK           - Text Processing                     │
│  • TextBlob       - Sentiment Analysis                  │
│  • NumPy          - Numerical Operations                │
│  • Pandas         - Data Handling                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                     ML/AI LAYER                         │
├─────────────────────────────────────────────────────────┤
│  • Scikit-learn   - ML Models & Preprocessing           │
│  • TF-IDF         - Feature Extraction                  │
│  • SVD            - Dimensionality Reduction            │
│  • Joblib         - Model Serialization                 │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                 DEPLOYMENT & DEVOPS                     │
├─────────────────────────────────────────────────────────┤
│  • Vercel         - Frontend Hosting                    │
│  • Render         - Backend Hosting                     │
│  • GitHub Actions - CI/CD Pipeline                      │
│  • Docker         - Containerization                    │
│  • Git/GitHub     - Version Control                     │
└─────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌────────────────────────────────────────────────────────┐
│                     GITHUB                             │
│  • Source Code Repository                              │
│  • Version Control                                     │
│  • CI/CD Triggers                                      │
└──────────┬──────────────────────┬──────────────────────┘
           │                      │
           │ Auto-Deploy          │ Auto-Deploy
           │ on Push              │ on Push
           │                      │
┌──────────▼──────────┐   ┌──────▼──────────────────────┐
│      VERCEL         │   │        RENDER               │
│  ┌──────────────┐   │   │  ┌──────────────────────┐   │
│  │  Frontend    │   │   │  │  Backend API         │   │
│  │  Build &     │   │   │  │  Build & Deploy      │   │
│  │  Deploy      │   │   │  │  Docker Container    │   │
│  └──────────────┘   │   │  └──────────────────────┘   │
│                     │   │                             │
│  CDN Distribution   │   │  Auto-Scaling               │
│  HTTPS Enabled      │   │  HTTPS Enabled              │
│  Custom Domain      │   │  Health Checks              │
└─────────────────────┘   └─────────────────────────────┘
```

---

## Request Flow Example

### Example: Analyzing "You're amazing!"

```
Step 1: User Input
├─ User types: "You're amazing!"
└─ Frontend validates (non-empty, <5000 chars)

Step 2: API Request
├─ POST https://api.onrender.com/api/predict
└─ Body: { "text": "You're amazing!" }

Step 3: Preprocessing
├─ Lowercase: "you're amazing!"
├─ Expand contractions: "you are amazing!"
├─ Remove punctuation: "you are amazing"
├─ Tokenize: ["you", "are", "amazing"]
├─ Remove stopwords: ["amazing"]
└─ Result: "amazing"

Step 4: Feature Extraction
├─ TF-IDF vectorization
├─ Convert to numerical features
└─ Feature vector: [0, 0, 0.85, 0, ...]

Step 5: Prediction
├─ Pass to trained model
├─ Model outputs: [0.95, 0.05]
└─ Prediction: not_cyberbullying (95% confidence)

Step 6: Response
├─ Format JSON response
└─ Return: {
    "prediction": "not_cyberbullying",
    "confidence": 0.95,
    "timestamp": "2024-01-01T12:00:00"
  }

Step 7: Display
├─ Frontend receives response
├─ Shows green checkmark ✅
├─ Displays: "No Cyberbullying Detected"
└─ Shows confidence bar at 95%
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────┐
│              SECURITY LAYERS                    │
├─────────────────────────────────────────────────┤
│  1. HTTPS/TLS                                   │
│     • Encrypted communication                   │
│     • Automatic via Vercel & Render             │
├─────────────────────────────────────────────────┤
│  2. CORS Protection                             │
│     • Allowed origins only                      │
│     • Configured in Flask                       │
├─────────────────────────────────────────────────┤
│  3. Input Validation                            │
│     • Length limits (5000 chars)                │
│     • Type checking                             │
│     • Sanitization                              │
├─────────────────────────────────────────────────┤
│  4. Environment Variables                       │
│     • No secrets in code                        │
│     • .env for local                            │
│     • Platform env vars for production          │
├─────────────────────────────────────────────────┤
│  5. Error Handling                              │
│     • No sensitive info in errors               │
│     • Sanitized error messages                  │
│     • Logging without PII                       │
└─────────────────────────────────────────────────┘
```

---

## Scalability

```
Current Capacity (Free Tier):
├─ Frontend (Vercel)
│  ├─ Unlimited deployments
│  ├─ 100GB bandwidth/month
│  └─ Global CDN
│
└─ Backend (Render)
   ├─ 750 hours/month
   ├─ Auto-sleep after 15 min
   └─ Cold start: ~30 seconds

Scaling Options:
├─ Render Starter Plan ($7/mo)
│  ├─ No cold starts
│  ├─ 400GB bandwidth
│  └─ More compute resources
│
├─ Add Caching Layer
│  ├─ Redis for predictions
│  └─ Reduce computation
│
└─ Load Balancing
   ├─ Multiple backend instances
   └─ Auto-scaling
```

---

This architecture provides:
✅ Separation of concerns
✅ Horizontal scalability
✅ Easy deployment
✅ Cost-effective (free tier available)
✅ Production-ready
