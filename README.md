# 🎙 Yaaba AI Voice Translator - Streamlit Version

A bilingual speech-to-speech translator built with Streamlit that translates between French and Mooré (a major West-African language) using advanced AI models.

## ✨ Features

- **🎤 Voice Translation**: Record speech and get instant translations with audio output
- **📝 Text Translation**: Type text for translation with speech synthesis
- **🔄 Bidirectional**: Supports both French → Mooré and Mooré → French
- **🎵 Audio Output**: Hear translations spoken aloud using text-to-speech
- **💾 State Persistence**: Results remain visible during your session
- **📱 Mobile Friendly**: Responsive design that works on all devices

## 🚀 Quick Start

### Option 1: Deploy to Streamlit Community Cloud (FREE)

1. **Fork/Clone this repository**
2. **Push to your GitHub account**
3. **Go to [share.streamlit.io](https://share.streamlit.io)**
4. **Connect your repository**
5. **Deploy!**

Your app will be available at: `https://your-username-yaaba-voice-translator.streamlit.app`

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/yaaba-voice-translator.git
cd yaaba-voice-translator/streamlit-version

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 File Structure

```
streamlit-version/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── deployment-guide.md      # Detailed deployment instructions
├── config.toml              # Streamlit configuration (optional)
└── .streamlit/              # Streamlit config directory
    └── config.toml          # App-specific settings
```

## 🔧 Technology Stack

- **Frontend**: Streamlit
- **Speech Recognition**: OpenAI Whisper (small model)
- **Translation**: Custom NLLB model (`mafromedia/yaaba-fr-mo-nllb600M`)
- **Text-to-Speech**: Coqui TTS (`xtts_v2`)
- **Audio Processing**: SoundFile, LibROSA
- **ML Framework**: PyTorch, Transformers

## 🎯 Usage

### Voice Translation
1. Select translation direction (French → Mooré or Mooré → French)
2. Click the audio input widget and record your speech
3. Click "🔄 Translate Voice" to process
4. View detected text, translation, and play audio output

### Text Translation
1. Switch to the "📝 Text Translation" tab
2. Select translation direction
3. Type your text in the input area
4. Click "🔄 Translate Text"
5. View translation and play audio output

## ⚙️ Configuration

### Model Settings
You can modify the models used by editing these variables in `app.py`:

```python
# Speech-to-text model size options: tiny, base, small, medium, large
whisper_model = whisper.load_model("small")

# Translation model
translation_model_name = "mafromedia/yaaba-fr-mo-nllb600M"

# Text-to-speech model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
```

### Performance Optimization
For CPU-only deployment, add this to the top of `app.py`:
```python
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
```

For smaller memory footprint:
```python
# Use tiny Whisper model
whisper_model = whisper.load_model("tiny")
```

## 🌐 Deployment Options

### 1. Streamlit Community Cloud (Recommended)
- **Cost**: Free
- **Features**: Automatic HTTPS, custom domains, GitHub integration
- **Limits**: Resource limitations for free tier

### 2. Heroku
- **Cost**: ~$7/month (Eco dyno)
- **Features**: More resources, custom domains
- **Setup**: Requires additional configuration files

### 3. AWS/GCP/Azure
- **Cost**: Variable based on usage
- **Features**: Full control, scalability
- **Setup**: Requires containerization

### 4. Self-hosted
- **Cost**: Your infrastructure costs
- **Features**: Complete control
- **Setup**: Direct deployment on your servers

## 📊 Performance Notes

- **First load**: 5-10 minutes (models downloading)
- **CPU inference**: ~30-60 seconds per translation
- **GPU inference**: ~5-15 seconds per translation
- **Memory usage**: ~4-8GB RAM depending on models

## 🐛 Troubleshooting

### Common Issues

1. **Models not loading**
   - Check internet connection
   - Verify model names are correct
   - Ensure sufficient disk space

2. **Audio recording not working**
   - Ensure HTTPS deployment (required for microphone)
   - Check browser permissions
   - Try different browsers

3. **Memory errors**
   - Use smaller models (e.g., `whisper.load_model("tiny")`)
   - Deploy on higher-memory instances

4. **Slow performance**
   - Upgrade to GPU-enabled hosting
   - Use model quantization
   - Implement model caching

### Debug Mode
Enable debug logging by adding to `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔄 Updates and Maintenance

### Updating Your App
1. Modify code locally
2. Push changes to GitHub
3. Streamlit Cloud auto-redeploys
4. Monitor deployment logs

### Adding New Features
- New language pairs: Update `LANGUAGE_CODES` dictionary
- New models: Modify model loading functions
- UI improvements: Update Streamlit components

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0.

## 🙏 Acknowledgments

- **OpenAI** for Whisper
- **Meta** for NLLB base models
- **Coqui AI** for TTS
- **Streamlit** for the amazing framework
- **Hugging Face** for model hosting

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: Built by GO AI Corp – Yaaba AI Initiative

---

**🌍 Empowering African languages through artificial intelligence**

## 📈 Roadmap

- [ ] Add more African languages
- [ ] Implement voice activity detection
- [ ] Add batch translation
- [ ] Mobile app version
- [ ] API endpoints
- [ ] Multi-speaker support

## 🎨 Customization

The app uses custom CSS for styling. You can modify the appearance by editing the CSS in the `st.markdown()` sections of `app.py`.

### Color Scheme
- Primary: `#667eea` to `#764ba2` (gradient)
- Background: `#f8f9fa`
- Text: `#555`
- Border: `#eee`

Enjoy building bridges between languages! 🌉