# 🚨 Streamlit Deployment Troubleshooting

## Issue: "installer returned a non-zero exit code"

This error typically occurs due to:
1. **Dependency conflicts** in requirements.txt
2. **Platform-specific packages** that can't install
3. **Memory/resource limitations** during build

## ✅ Quick Fixes

### Fix 1: Use Minimal Requirements (Recommended)
Replace your `requirements.txt` with `requirements-minimal.txt`:

```bash
# Rename the minimal requirements file
mv requirements-minimal.txt requirements.txt
```

### Fix 2: Platform-Specific Deployment

#### For Streamlit Community Cloud:
- Only need: `app.py` and `requirements.txt`
- Remove: `Procfile`, `setup.sh`, `runtime.txt`
- Streamlit Cloud handles configuration automatically

#### For Heroku:
- Keep all files as they are (now fixed)
- The markdown formatting has been removed

### Fix 3: Dependency Resolution
If still getting errors, try this ultra-minimal requirements.txt:

```
streamlit>=1.28.0
torch>=2.0.0
transformers>=4.30.0
openai-whisper>=20231117
TTS>=0.15.0
huggingface-hub>=0.16.0
numpy>=1.24.0
```

## 🔍 Debugging Steps

### Step 1: Check Build Logs
Look for specific error messages like:
- `ERROR: Failed building wheel for [package]`
- `No matching distribution found for [package]`
- `Could not install packages due to an OSError`

### Step 2: Platform Detection
**Streamlit Community Cloud**: 
- URL ends with `.streamlit.app`
- Uses automatic Python environment

**Heroku**:
- URL ends with `.herokuapp.com`
- Uses buildpacks and Procfile

**Railway/Render**:
- Uses Docker or similar containerization

### Step 3: Common Package Issues

#### TTS Package Issues:
```
# Replace TTS>=0.15.0 with:
coqui-tts>=0.15.0
# OR remove TTS entirely for testing
```

#### PyTorch Issues:
```
# Use CPU-only version:
torch>=2.0.0 --index-url https://download.pytorch.org/whl/cpu
```

#### Whisper Issues:
```
# Use specific version:
openai-whisper==20231117
```

## 🚀 Deployment Commands

### For Streamlit Community Cloud:
1. Push fixed files to GitHub
2. Streamlit will auto-redeploy
3. Monitor logs in dashboard

### For Heroku:
```bash
# Commit the fixes
git add .
git commit -m "Fix deployment dependencies"
git push heroku main

# Check logs
heroku logs --tail
```

### For Other Platforms:
Most platforms auto-detect changes and redeploy.

## ⚡ Emergency Minimal App

If all else fails, here's a minimal working version:

**requirements.txt**:
```
streamlit>=1.28.0
transformers>=4.30.0
torch>=2.0.0
```

**app.py** (add at top):
```python
import streamlit as st

# Disable heavy models for testing
DEMO_MODE = True

if DEMO_MODE:
    st.warning("Demo mode: Heavy AI models disabled for deployment testing")
    # Replace model loading with placeholders
```

## 📞 Next Steps

1. **Try minimal requirements first**
2. **Remove unnecessary files** if deploying to Streamlit Cloud
3. **Check specific error messages** in deployment logs
4. **Test locally** with the same requirements.txt

The files have been fixed and you should be able to redeploy successfully! 🎉