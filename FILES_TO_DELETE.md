# 🗑️ FILES TO DELETE FROM GITHUB REPO

## ❌ REMOVE THESE FILES (Unnecessary/Redundant)

### 1. Prediction Output Files (Generated, not source code)
```
✗ test_predictions_only.csv       - Generated output
✗ test_predictions_mapped.csv     - Generated output  
✗ external_lstm_predictions.csv   - Generated output
```
**Reason:** These are generated results from model runs, not source code. Users can generate these themselves.

---

### 2. Test Data Files (Should be in /data folder)
```
✗ test-1.csv                      - Move to data/ folder or delete
✗ test-2.csv                      - Move to data/ folder or delete
```
**Reason:** If needed, organize in proper data folder structure.

---

### 3. Model Serialization Files (Too Large for Git)
```
✗ svd_scaler.joblib              - 100KB+ binary file
✗ svd_truncated.joblib           - Large binary file
✗ tb_scaler.joblib               - Binary file
```
**Reason:** 
- Too large for GitHub (should use Git LFS if needed)
- Users should train their own models
- Can be hosted separately (Google Drive/S3)
**Alternative:** Provide download link in README

---

### 4. Wrong Filename
```
✗ _gitignore                      - Wrong name (underscore instead of dot)
```
**Reason:** Should be `.gitignore` (will create correct one)

---

### 5. Duplicate README/Requirements
```
✗ README.md (duplicate)           - You have 2 copies
✗ requirements.txt (duplicate)    - You have 2 copies  
✗ text_preprocessing.py (duplicate) - You have 2 copies
```
**Reason:** Keep only one version of each

---

## ✅ KEEP THESE FILES

### Essential Source Code
```
✓ Main.ipynb                      - Main training notebook
✓ text_preprocessing.py           - Keep ONE copy
✓ README.md                       - Keep ONE copy (updated)
✓ requirements.txt                - Keep ONE copy (updated)
```

### Data (Organize properly)
```
✓ Dataset-updated.csv             - Main dataset (essential)
```

---

## 📋 FINAL CLEANUP COMMANDS

Run these commands to clean your repo:

```bash
# Remove generated prediction files
rm test_predictions_only.csv
rm test_predictions_mapped.csv
rm external_lstm_predictions.csv

# Remove test files (or move to data/)
rm test-1.csv test-2.csv

# Remove large binary model files
rm *.joblib

# Remove wrong gitignore
rm _gitignore

# Remove duplicates (keep only one of each)
# Check which ones are newer/better and keep those
```

---

## 📁 RECOMMENDED GITHUB STRUCTURE

```
CyberSense-CSE445/
│
├── backend/                      # Backend API (Deploy to Render)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── model_inference.py
│   │   └── preprocessing.py
│   ├── models/
│   │   └── .gitkeep            # Empty folder (models downloaded separately)
│   ├── requirements.txt
│   ├── Procfile
│   └── runtime.txt
│
├── frontend/                     # Frontend (Deploy to Vercel)
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── vercel.json
│
├── notebooks/
│   └── Main.ipynb              # Training notebook
│
├── data/
│   └── Dataset-updated.csv     # Main dataset
│
├── .gitignore
├── README.md
└── MODEL_DOWNLOAD.md           # Instructions to download trained models
```

---

## 🎯 FILES SUMMARY

| Action | Count | Files |
|--------|-------|-------|
| **DELETE** | 8-10 | Predictions CSVs, test CSVs, .joblib files, wrong gitignore, duplicates |
| **KEEP** | 4 | Main.ipynb, Dataset-updated.csv, README.md, requirements.txt |
| **CREATE NEW** | 15+ | Backend API, Frontend app, deployment configs |

---

## ⚠️ IMPORTANT NOTES

1. **Model Files:** Too large for GitHub. Options:
   - Use Git LFS (Large File Storage)
   - Host on Google Drive/Dropbox
   - Users train their own
   - Download from releases section

2. **Dataset:** At 64K rows, CSV should be fine for GitHub
   - If >100MB, consider Git LFS or external hosting

3. **Duplicates:** You uploaded some files twice - keep only the best version

4. **Organize by deployment:** Separate backend and frontend for easier deployment to Render and Vercel

---

## 🚀 NEXT STEPS

1. Delete unnecessary files
2. Organize remaining files into backend/frontend structure
3. Create deployment configurations for Render and Vercel
4. Update README with model download instructions
5. Push to GitHub

