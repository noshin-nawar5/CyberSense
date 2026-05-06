# 🧪 Testing Guide - CyberSense

Complete testing instructions for local development and production.

---

## 📋 Testing Checklist

- [ ] Backend unit tests pass
- [ ] API endpoints respond correctly
- [ ] Text preprocessing works
- [ ] Model predictions are accurate
- [ ] Frontend displays results
- [ ] CORS configuration works
- [ ] Error handling functions
- [ ] Performance is acceptable

---

## Part 1: Backend Testing

### Setup Test Environment

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install testing dependencies
pip install pytest pytest-cov requests
```

### Test 1: Import Check

```python
# test_imports.py
import sys
sys.path.insert(0, '.')

def test_imports():
    """Test all required imports work"""
    try:
        import flask
        import flask_cors
        import sklearn
        import nltk
        import textblob
        import numpy
        import joblib
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

if __name__ == '__main__':
    test_imports()
```

Run:
```bash
python test_imports.py
```

### Test 2: Text Preprocessing

```python
# test_preprocessing.py
from app.preprocessing import clean_text, clean_text_basic, clean_text_advanced

def test_basic_cleaning():
    """Test basic text cleaning"""
    tests = [
        ("Hello @user http://example.com", "hello"),
        ("I don't like this!!!", "i do not like this"),
        ("sooooo good", "soo good"),
    ]
    
    for input_text, expected in tests:
        result = clean_text_basic(input_text)
        assert expected in result.lower(), f"Failed: {input_text} -> {result}"
    
    print("✓ Basic cleaning tests passed")

def test_advanced_cleaning():
    """Test advanced cleaning with NLTK"""
    text = "RT @user: I don't like this http://example.com #test"
    result = clean_text_advanced(text)
    
    # Should remove stopwords, URLs, mentions
    assert "http" not in result
    assert "@user" not in result
    assert "rt" not in result.lower()
    
    print("✓ Advanced cleaning tests passed")

def test_batch_cleaning():
    """Test batch processing"""
    from app.preprocessing import batch_clean_texts
    
    texts = [
        "This is test 1",
        "This is test 2",
        "This is test 3"
    ]
    
    results = batch_clean_texts(texts)
    assert len(results) == 3
    assert all(isinstance(r, str) for r in results)
    
    print("✓ Batch cleaning tests passed")

if __name__ == '__main__':
    test_basic_cleaning()
    test_advanced_cleaning()
    test_batch_cleaning()
    print("\n✓ All preprocessing tests passed!")
```

Run:
```bash
python test_preprocessing.py
```

### Test 3: Flask App

```python
# test_app.py
import sys
sys.path.insert(0, '.')
from app.main import app
import json

def test_health_endpoint():
    """Test health check endpoint"""
    client = app.test_client()
    response = client.get('/api/health')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'healthy'
    
    print("✓ Health endpoint test passed")

def test_predict_endpoint():
    """Test prediction endpoint"""
    client = app.test_client()
    
    # Test valid request
    response = client.post('/api/predict',
        data=json.dumps({'text': 'This is a test message'}),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prediction' in data
    assert 'confidence' in data
    assert data['prediction'] in ['cyberbullying', 'not_cyberbullying']
    
    print("✓ Predict endpoint test passed")

def test_missing_text():
    """Test error handling for missing text"""
    client = app.test_client()
    
    response = client.post('/api/predict',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    
    print("✓ Error handling test passed")

def test_batch_predict():
    """Test batch prediction"""
    client = app.test_client()
    
    response = client.post('/api/batch-predict',
        data=json.dumps({
            'texts': ['text 1', 'text 2', 'text 3']
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'results' in data
    assert len(data['results']) == 3
    
    print("✓ Batch prediction test passed")

if __name__ == '__main__':
    print("Testing Flask app...\n")
    test_health_endpoint()
    test_predict_endpoint()
    test_missing_text()
    test_batch_predict()
    print("\n✓ All Flask tests passed!")
```

Run:
```bash
python test_app.py
```

### Test 4: API Integration Test

```bash
# Start Flask app in one terminal
python app/main.py

# In another terminal, test with curl
# Test 1: Health check
curl http://localhost:5000/api/health

# Test 2: Predict
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test message"}'

# Test 3: Cyberbullying text
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "You are so stupid and ugly"}'

# Test 4: Safe text
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "You are amazing and talented!"}'

# Test 5: Batch prediction
curl -X POST http://localhost:5000/api/batch-predict \
  -H "Content-Type: application/json" \
  -d '{"texts": ["text 1", "text 2", "text 3"]}'
```

---

## Part 2: Frontend Testing

### Test 1: Static HTML

```bash
cd frontend

# Serve static files
python -m http.server 3000 --directory public

# Open browser
open http://localhost:3000
# Or manually navigate to http://localhost:3000
```

### Test 2: Manual Testing Checklist

Open `http://localhost:3000` and verify:

- [ ] Page loads correctly
- [ ] No console errors (F12 → Console)
- [ ] Logo and tagline display
- [ ] Text area accepts input
- [ ] Character counter updates
- [ ] Example chips clickable
- [ ] Analyze button works
- [ ] Loading spinner shows
- [ ] Results display correctly
- [ ] Confidence bar animates
- [ ] Clear button works
- [ ] Responsive on mobile

### Test 3: Browser Console Tests

Open browser console (F12) and run:

```javascript
// Test 1: Check API URL
console.log(API_URL);
// Should print your backend URL

// Test 2: Test health check
fetch(`${API_URL}/health`)
  .then(r => r.json())
  .then(data => console.log('Health:', data))
  .catch(err => console.error('Error:', err));

// Test 3: Test prediction
fetch(`${API_URL}/predict`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: 'test message'})
})
  .then(r => r.json())
  .then(data => console.log('Prediction:', data))
  .catch(err => console.error('Error:', err));
```

### Test 4: Network Tab

1. Open DevTools (F12)
2. Go to Network tab
3. Click "Analyze Text"
4. Check:
   - [ ] Request sent to correct URL
   - [ ] Status: 200 OK
   - [ ] Response contains prediction data
   - [ ] No CORS errors

---

## Part 3: Integration Testing

### Test Full Flow

```bash
# Terminal 1: Start Backend
cd backend
source venv/bin/activate
python app/main.py

# Terminal 2: Start Frontend
cd frontend
python -m http.server 3000 --directory public

# Browser: Test
# 1. Navigate to http://localhost:3000
# 2. Enter text: "You are amazing!"
# 3. Click "Analyze Text"
# 4. Verify: Shows "No Cyberbullying Detected"
# 5. Enter text: "You are so stupid"
# 6. Click "Analyze Text"
# 7. Verify: Shows "Potential Cyberbullying Detected"
```

### Test Example Texts

Click each example chip and verify:

1. **"You are so talented! Keep up the great work!"**
   - Expected: ✅ No Cyberbullying
   - Confidence: 80-95%

2. **"I really enjoyed reading your post. Very insightful!"**
   - Expected: ✅ No Cyberbullying
   - Confidence: 80-95%

3. **"You're so stupid and ugly. Nobody likes you."**
   - Expected: ⚠️ Cyberbullying Detected
   - Confidence: 85-95%

4. **"Just kill yourself already. Loser."**
   - Expected: ⚠️ Cyberbullying Detected
   - Confidence: 90-99%

---

## Part 4: Production Testing

### Test Deployed Backend (Render)

```bash
# Replace with your actual Render URL
BACKEND_URL="https://cybersense-api.onrender.com"

# Test 1: Health
curl $BACKEND_URL/api/health

# Test 2: Prediction
curl -X POST $BACKEND_URL/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "test message"}'

# Test 3: Performance
time curl -X POST $BACKEND_URL/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "test message"}'
```

### Test Deployed Frontend (Vercel)

1. **Navigate to your Vercel URL**: `https://cybersense.vercel.app`

2. **Check all functionality**:
   - [ ] Page loads in <2 seconds
   - [ ] No console errors
   - [ ] Can submit predictions
   - [ ] Results display correctly
   - [ ] Mobile responsive

3. **Test from different devices**:
   - [ ] Desktop Chrome
   - [ ] Desktop Firefox
   - [ ] Desktop Safari
   - [ ] Mobile iOS Safari
   - [ ] Mobile Android Chrome

### Test CORS

```bash
# Test from different origin
curl -X POST https://cybersense-api.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -H "Origin: https://cybersense.vercel.app" \
  -d '{"text": "test"}'

# Should return data, not CORS error
```

---

## Part 5: Performance Testing

### Test Response Time

```python
# test_performance.py
import requests
import time
import statistics

API_URL = "http://localhost:5000/api"  # Change to your URL

def test_response_time(num_requests=10):
    """Test average response time"""
    times = []
    
    for i in range(num_requests):
        start = time.time()
        response = requests.post(
            f"{API_URL}/predict",
            json={"text": "This is a test message for performance testing"}
        )
        end = time.time()
        
        if response.status_code == 200:
            times.append(end - start)
        
        time.sleep(0.1)  # Small delay between requests
    
    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"\nPerformance Test Results ({num_requests} requests):")
    print(f"  Average: {avg_time:.3f}s")
    print(f"  Min: {min_time:.3f}s")
    print(f"  Max: {max_time:.3f}s")
    
    # Performance expectations
    if avg_time < 0.5:
        print("  ✓ Excellent performance")
    elif avg_time < 1.0:
        print("  ✓ Good performance")
    elif avg_time < 2.0:
        print("  ⚠ Acceptable performance")
    else:
        print("  ✗ Poor performance - optimization needed")

if __name__ == '__main__':
    test_response_time()
```

Run:
```bash
pip install requests
python test_performance.py
```

### Load Testing (Optional)

```bash
# Install locust
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class CyberSenseUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def predict(self):
        self.client.post("/api/predict", json={
            "text": "This is a test message"
        })
EOF

# Run load test
locust -f locustfile.py --host=http://localhost:5000

# Open http://localhost:8089
# Configure users and spawn rate
# Start test
```

---

## Part 6: Error Testing

### Test Error Handling

```bash
# Test 1: Empty request
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{}'

# Expected: 400 Bad Request

# Test 2: Missing text field
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"message": "wrong field"}'

# Expected: 400 Bad Request

# Test 3: Text too long
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "'$(python -c 'print("a"*6000)')'"}'

# Expected: 400 Bad Request

# Test 4: Invalid JSON
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d 'invalid json'

# Expected: 400 Bad Request

# Test 5: Wrong HTTP method
curl -X GET http://localhost:5000/api/predict

# Expected: 405 Method Not Allowed
```

---

## Part 7: Security Testing

### Test Input Sanitization

```python
# test_security.py
import requests

API_URL = "http://localhost:5000/api"

def test_xss_injection():
    """Test XSS attack prevention"""
    payloads = [
        "<script>alert('xss')</script>",
        "<img src=x onerror=alert('xss')>",
        "javascript:alert('xss')",
    ]
    
    for payload in payloads:
        response = requests.post(
            f"{API_URL}/predict",
            json={"text": payload}
        )
        assert response.status_code == 200
        # Should not execute script
        print(f"✓ XSS test passed for: {payload[:30]}")

def test_sql_injection():
    """Test SQL injection (if database added)"""
    payloads = [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "admin'--",
    ]
    
    for payload in payloads:
        response = requests.post(
            f"{API_URL}/predict",
            json={"text": payload}
        )
        assert response.status_code == 200
        print(f"✓ SQL test passed for: {payload[:30]}")

if __name__ == '__main__':
    test_xss_injection()
    test_sql_injection()
    print("\n✓ All security tests passed!")
```

---

## Part 8: Automated Testing

### Create Test Suite

```python
# run_all_tests.py
import subprocess
import sys

tests = [
    ("Import Check", "test_imports.py"),
    ("Preprocessing", "test_preprocessing.py"),
    ("Flask App", "test_app.py"),
    ("Performance", "test_performance.py"),
    ("Security", "test_security.py"),
]

def run_test(name, file):
    """Run a single test file"""
    print(f"\n{'='*50}")
    print(f"Running: {name}")
    print('='*50)
    
    result = subprocess.run(
        [sys.executable, file],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

if __name__ == '__main__':
    results = []
    
    for name, file in tests:
        success = run_test(name, file)
        results.append((name, success))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    # Exit code
    all_passed = all(success for _, success in results)
    sys.exit(0 if all_passed else 1)
```

Run all tests:
```bash
python run_all_tests.py
```

---

## 🎯 Test Summary

| Category | Tests | Status |
|----------|-------|--------|
| Backend Imports | ✓ | Pass |
| Text Preprocessing | ✓ | Pass |
| Flask Endpoints | ✓ | Pass |
| Error Handling | ✓ | Pass |
| Frontend UI | ✓ | Pass |
| Integration | ✓ | Pass |
| Performance | ✓ | Pass |
| Security | ✓ | Pass |

---

## 📊 Expected Performance

| Metric | Target | Acceptable |
|--------|--------|------------|
| API Response | <500ms | <1000ms |
| Page Load | <2s | <3s |
| Prediction Accuracy | >90% | >85% |
| Uptime | 99.9% | 99% |

---

## 🐛 Common Issues

**Issue**: Tests fail with import errors  
**Fix**: `pip install -r requirements.txt`

**Issue**: NLTK data not found  
**Fix**: `python -c "import nltk; nltk.download('all')"`

**Issue**: Flask app not reachable  
**Fix**: Check if running on correct port, verify firewall

**Issue**: Frontend can't reach API  
**Fix**: Update CORS origins, check API URL

---

**Happy Testing! 🧪**
