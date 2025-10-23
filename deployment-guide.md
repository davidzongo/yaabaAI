# Yaaba AI Voice Translator - Streamlit Deployment Guide

## 🚀 Deployment Options Overview

| Platform | Cost | Difficulty | Performance | Best For |
|----------|------|------------|-------------|----------|
| **Streamlit Cloud** | Free | ⭐ Easy | Good | Testing, demos |
| **Heroku** | $7/month | ⭐⭐ Medium | Better | Small production |
| **Railway** | $5/month | ⭐⭐ Medium | Better | Modern deployment |
| **Google Cloud Run** | Pay-per-use | ⭐⭐⭐ Hard | Best | High traffic |
| **AWS ECS** | Variable | ⭐⭐⭐ Hard | Best | Enterprise |

---

## 🎯 Option 1: Streamlit Community Cloud (Recommended)

### Prerequisites
- GitHub account
- Streamlit account (free at [share.streamlit.io](https://share.streamlit.io))

### Step 1: Prepare Repository
```bash
# Create new repo on GitHub
# Upload the streamlit-version/ folder contents to your repo root

# Your repo structure should look like:
# your-repo/
# ├── app.py
# ├── requirements.txt
# ├── README.md
# └── deployment-guide.md
```

### Step 2: Deploy
1. **Visit** [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with GitHub
3. **Click "New app"**
4. **Configure**:
   - Repository: `your-username/yaaba-voice-translator`
   - Branch: `main`
   - Main file: `app.py`
   - App URL: `yaaba-voice-translator`
5. **Click "Deploy!"**

### Step 3: Monitor Deployment
- **Build time**: 10-15 minutes (first time)
- **Status**: Check logs tab for progress
- **URL**: `https://your-username-yaaba-voice-translator.streamlit.app`

### Streamlit Cloud Configuration
Create `.streamlit/config.toml` for advanced settings:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#555555"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

---

## 🔧 Option 2: Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Step 1: Additional Files
Create these files in your `streamlit-version/` directory:

**Procfile**:
```
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh**:
```bash
#!/bin/bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@example.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

**runtime.txt**:
```
python-3.9.18
```

### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create yaaba-voice-translator

# Set buildpacks for audio support
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git

# Set environment variables
heroku config:set TRANSFORMERS_CACHE=/tmp/transformers_cache
heroku config:set HF_HOME=/tmp/huggingface_cache

# Deploy
git add .
git commit -m "Deploy Yaaba AI to Heroku"
git push heroku main
```

### Step 3: Scale and Monitor
```bash
# Scale to 1 dyno
heroku ps:scale web=1

# View logs
heroku logs --tail

# Open app
heroku open
```

---

## ⚡ Option 3: Railway Deployment

### Prerequisites
- Railway account ([railway.app](https://railway.app))
- GitHub repo with your code

### Step 1: Connect Repository
1. **Go to** [railway.app](https://railway.app)
2. **Click "Start a New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository**

### Step 2: Configure
Railway auto-detects Streamlit apps. If needed, set:
- **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- **Environment Variables**:
  ```
  PORT=8501
  TRANSFORMERS_CACHE=/tmp/transformers_cache
  HF_HOME=/tmp/huggingface_cache
  ```

### Step 3: Deploy
- **Automatic**: Railway deploys on every push
- **Manual**: Click "Deploy" in dashboard
- **URL**: Provided in Railway dashboard

---

## 🏗️ Option 4: Docker + Cloud Run

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Build and Deploy to Google Cloud Run
```bash
# Build image
docker build -t yaaba-voice-translator .

# Tag for Google Container Registry
docker tag yaaba-voice-translator gcr.io/YOUR_PROJECT_ID/yaaba-voice-translator

# Push to registry
docker push gcr.io/YOUR_PROJECT_ID/yaaba-voice-translator

# Deploy to Cloud Run
gcloud run deploy yaaba-voice-translator \
  --image gcr.io/YOUR_PROJECT_ID/yaaba-voice-translator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2 \
  --timeout 3600
```

---

## 🔍 Performance Optimization

### For CPU-Only Deployment
Add to `app.py`:
```python
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Use smaller models
@st.cache_resource
def load_models():
    whisper_model = whisper.load_model("tiny")  # Instead of "small"
    # ... rest of function
```

### Memory Optimization
```python
# Add memory cleanup
import gc
import torch

def cleanup_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

# Call after each translation
cleanup_memory()
```

### Model Caching
```python
# Pre-download models (add to requirements.txt)
# huggingface-hub[cli]

# Then in Dockerfile or startup script:
# python -c "import whisper; whisper.load_model('small')"
# python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('mafromedia/yaaba-fr-mo-nllb600M')"
```

---

## 🐛 Troubleshooting

### Common Deployment Issues

#### 1. Build Timeout
**Error**: Build takes too long
**Solution**: 
- Use smaller models in requirements.txt
- Pre-build Docker image with models cached
- Increase build timeout settings

#### 2. Memory Limits
**Error**: Out of memory during model loading
**Solution**:
```python
# Use model quantization
model = AutoModelForSeq2SeqLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # Use half precision
    device_map="auto"
)
```

#### 3. Audio Issues
**Error**: Microphone not working
**Solution**:
- Ensure HTTPS deployment
- Check browser permissions
- Test with uploaded audio files

#### 4. Model Download Fails
**Error**: Can't download models
**Solution**:
```python
# Add retry logic
import time
from huggingface_hub import HfApi

def download_with_retry(model_name, max_retries=3):
    for i in range(max_retries):
        try:
            return AutoTokenizer.from_pretrained(model_name)
        except Exception as e:
            if i == max_retries - 1:
                raise e
            time.sleep(10)
```

### Platform-Specific Issues

#### Streamlit Cloud
- **Resource limits**: Use smaller models
- **Timeout issues**: Optimize model loading
- **Storage limits**: Clear temporary files

#### Heroku
- **Slug size**: Reduce dependencies
- **Memory limits**: Use Eco/Basic dynos
- **Build time**: Use Docker deployment

#### Railway
- **Build failures**: Check logs in dashboard
- **Port issues**: Ensure PORT environment variable
- **Domain setup**: Configure custom domains in settings

---

## 📊 Monitoring and Analytics

### Built-in Monitoring
```python
# Add to app.py
import streamlit as st
from datetime import datetime

# Usage tracking
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0

def track_usage():
    st.session_state.usage_count += 1
    # Log to external service if needed
    print(f"Translation #{st.session_state.usage_count} at {datetime.now()}")
```

### External Monitoring
- **Streamlit Cloud**: Built-in analytics dashboard
- **Heroku**: Heroku Metrics
- **Railway**: Built-in monitoring
- **Google Cloud**: Cloud Monitoring

---

## 🔄 CI/CD Pipeline

### GitHub Actions for Streamlit Cloud
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Test app
      run: |
        python -c "import streamlit; print('Streamlit OK')"
        python -c "import torch; print('PyTorch OK')"
    
    # Streamlit Cloud auto-deploys on push to main
```

---

## 🎉 Final Checklist

Before deploying, ensure:

- [ ] **Code tested locally**: `streamlit run app.py` works
- [ ] **Requirements complete**: All dependencies listed
- [ ] **Model names correct**: No typos in model identifiers
- [ ] **Environment variables set**: If using external APIs
- [ ] **Memory limits considered**: Models fit in available RAM
- [ ] **HTTPS configured**: For microphone access
- [ ] **Error handling**: Graceful failure modes
- [ ] **Documentation updated**: README and guides current

**🚀 Ready to deploy!** Choose your preferred platform and follow the guide above.

---

**Built by GO AI Corp – Yaaba AI Initiative**  
*Empowering African languages through artificial intelligence*