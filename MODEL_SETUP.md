# 📦 Model Setup Instructions

Since trained models are too large for GitHub (`.joblib` files excluded in `.gitignore`), you need to either:
1. Train models yourself, OR
2. Download pre-trained models

---

## Option 1: Train Models Yourself (Recommended)

### Step 1: Setup Environment

```bash
# Navigate to project root
cd CyberSense-CSE445

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install numpy pandas scikit-learn nltk textblob jupyter notebook
```

### Step 2: Download NLTK Data

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

### Step 3: Run Training Notebook

```bash
# Start Jupyter
jupyter notebook

# Open Main.ipynb
# Run all cells (Runtime → Run All)
# This will:
# - Load and preprocess data
# - Train multiple ML models
# - Save best models to backend/models/
```

### Step 4: Verify Models Created

```bash
ls -lh backend/models/

# You should see:
# best_model.joblib
# tfidf_vectorizer.joblib
# svd_scaler.joblib (optional)
# svd_truncated.joblib (optional)
# tb_scaler.joblib (optional)
```

### Expected Training Time

| Dataset Size | Time (CPU) | Time (GPU) |
|--------------|------------|------------|
| 64K samples  | 30-45 min  | 10-15 min  |

---

## Option 2: Download Pre-trained Models

### Step 1: Host Models Externally

Upload your trained models to:
- **Google Drive** (Recommended - Free, 15GB)
- **Dropbox** 
- **Amazon S3**
- **GitHub Releases** (with Git LFS)

### Step 2: Get Shareable Links

**Google Drive**:
1. Upload `.joblib` files
2. Right-click → Get link
3. Change to "Anyone with the link"
4. Copy link ID from URL

Example URL:
```
https://drive.google.com/file/d/1ABC123XYZ/view?usp=sharing
                              ↑
                        This is the ID
```

### Step 3: Create Download Script

Create `backend/download_models.sh`:

```bash
#!/bin/bash

# Create models directory
mkdir -p backend/models

# Download from Google Drive
# Replace FILE_IDs with your actual IDs

echo "Downloading models..."

# Best model
wget --no-check-certificate \
  'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_1' \
  -O backend/models/best_model.joblib

# TF-IDF Vectorizer
wget --no-check-certificate \
  'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_2' \
  -O backend/models/tfidf_vectorizer.joblib

# SVD Scaler (optional)
wget --no-check-certificate \
  'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_3' \
  -O backend/models/svd_scaler.joblib

echo "✓ Models downloaded successfully!"
```

Make executable and run:
```bash
chmod +x backend/download_models.sh
./backend/download_models.sh
```

### Step 4: Python Download Script (Alternative)

Create `backend/download_models.py`:

```python
import os
import requests
from tqdm import tqdm

def download_file_from_google_drive(file_id, destination):
    """Download file from Google Drive"""
    
    URL = "https://drive.google.com/uc?export=download"
    
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    
    # Handle large files
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            params = {'id': file_id, 'confirm': value}
            response = session.get(URL, params=params, stream=True)
    
    # Save file
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    
    with open(destination, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
            for chunk in response.iter_content(block_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    
    print(f"✓ Downloaded: {destination}")

# Model file IDs from Google Drive
MODELS = {
    'best_model.joblib': 'YOUR_GOOGLE_DRIVE_FILE_ID_1',
    'tfidf_vectorizer.joblib': 'YOUR_GOOGLE_DRIVE_FILE_ID_2',
    'svd_scaler.joblib': 'YOUR_GOOGLE_DRIVE_FILE_ID_3',
    'svd_truncated.joblib': 'YOUR_GOOGLE_DRIVE_FILE_ID_4',
    'tb_scaler.joblib': 'YOUR_GOOGLE_DRIVE_FILE_ID_5',
}

if __name__ == '__main__':
    # Create models directory
    os.makedirs('backend/models', exist_ok=True)
    
    print("Downloading models from Google Drive...\n")
    
    for filename, file_id in MODELS.items():
        if file_id != 'YOUR_GOOGLE_DRIVE_FILE_ID_X':  # Skip placeholder
            destination = os.path.join('backend', 'models', filename)
            print(f"Downloading {filename}...")
            download_file_from_google_drive(file_id, destination)
            print()
    
    print("✓ All models downloaded successfully!")
```

Run:
```bash
pip install requests tqdm
python backend/download_models.py
```

---

## Option 3: Use Git LFS (Large File Storage)

### Setup Git LFS

```bash
# Install Git LFS (one-time)
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt-get install git-lfs

# Windows
# Download from: https://git-lfs.github.com/

# Initialize
git lfs install
```

### Track Model Files

```bash
# Track all .joblib files
git lfs track "*.joblib"

# Add .gitattributes
git add .gitattributes

# Add models
git add backend/models/*.joblib

# Commit
git commit -m "Add model files via Git LFS"

# Push
git push origin main
```

### Download Models from LFS

When others clone:
```bash
git clone https://github.com/yourusername/CyberSense-CSE445.git
cd CyberSense-CSE445
git lfs pull
```

**Note**: GitHub LFS has 1GB free storage, then $5/month for 50GB.

---

## Option 4: Use GitHub Releases

### Create Release with Models

```bash
# Create release on GitHub
# Go to: https://github.com/yourusername/CyberSense-CSE445/releases
# Click "Create a new release"
# Tag: v1.0.0
# Title: "CyberSense v1.0 - Trained Models"
# Upload .joblib files as assets
```

### Download from Release

```bash
# Download specific model
wget https://github.com/yourusername/CyberSense-CSE445/releases/download/v1.0.0/best_model.joblib \
  -O backend/models/best_model.joblib
```

Or use Python:
```python
import requests

RELEASE_URL = "https://github.com/yourusername/CyberSense-CSE445/releases/download/v1.0.0/"
MODELS = ['best_model.joblib', 'tfidf_vectorizer.joblib']

for model in MODELS:
    url = RELEASE_URL + model
    response = requests.get(url)
    with open(f'backend/models/{model}', 'wb') as f:
        f.write(response.content)
    print(f"Downloaded: {model}")
```

---

## Verifying Models

After downloading/training, verify models work:

```python
import joblib
import os

# Check files exist
models_dir = 'backend/models'
required_models = ['best_model.joblib', 'tfidf_vectorizer.joblib']

for model_file in required_models:
    path = os.path.join(models_dir, model_file)
    if os.path.exists(path):
        print(f"✓ {model_file} found ({os.path.getsize(path) / 1024:.1f} KB)")
        
        # Try loading
        try:
            model = joblib.load(path)
            print(f"  ✓ Loaded successfully")
        except Exception as e:
            print(f"  ✗ Error loading: {e}")
    else:
        print(f"✗ {model_file} NOT FOUND")
```

---

## Model File Sizes (Approximate)

| File | Size | Description |
|------|------|-------------|
| best_model.joblib | 50-200 KB | Trained classifier |
| tfidf_vectorizer.joblib | 500 KB - 2 MB | TF-IDF vectorizer |
| svd_truncated.joblib | 100-500 KB | SVD dimensionality reduction |
| svd_scaler.joblib | 10-50 KB | SVD feature scaler |
| tb_scaler.joblib | 10-50 KB | TextBlob feature scaler |

**Total**: ~2-5 MB

---

## For Render Deployment

After getting models, you need to make them available on Render:

### Method 1: Include in Repository (Git LFS)
```bash
# Use Git LFS as described in Option 3
git lfs track "*.joblib"
git add backend/models/*.joblib
git push
```

### Method 2: Download on Build
Add to `backend/requirements.txt`:
```
requests
tqdm
```

Add to Render Build Command:
```bash
pip install -r requirements.txt && python download_models.py
```

### Method 3: Render Disk Storage
1. Go to Render dashboard
2. Add persistent disk
3. Upload models via Shell/SFTP
4. Mount to `/opt/render/project/src/backend/models`

---

## Quick Start Commands

```bash
# Train models locally
jupyter notebook notebooks/Main.ipynb

# Verify models exist
ls -lh backend/models/

# Test backend with models
cd backend
python app/main.py

# Test prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "test message"}'
```

---

## Troubleshooting

**Problem**: `FileNotFoundError: models/best_model.joblib`

**Solutions**:
1. Run training notebook first
2. Download models from external source
3. Check file paths are correct
4. Ensure models directory exists: `mkdir -p backend/models`

**Problem**: `Model file corrupted`

**Solutions**:
1. Re-download model
2. Re-train model
3. Check file size matches expected
4. Verify joblib version compatibility

**Problem**: `Old model version`

**Solutions**:
1. Re-train with current scikit-learn version
2. Update scikit-learn to match training version
3. Check version compatibility in error message

---

## 📧 Need Models?

If you need the pre-trained models, contact the repository owner or train your own using the included notebook.

**Training is recommended** as it ensures:
- Latest scikit-learn compatibility
- Custom hyperparameter tuning
- Understanding of the model pipeline
- Ability to retrain with new data

---

**Happy Training! 🚀**
