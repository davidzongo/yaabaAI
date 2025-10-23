import streamlit as st
import torch
import whisper
import soundfile as sf
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from TTS.api import TTS
import tempfile
import os
from datetime import datetime
import io

# Set page config
st.set_page_config(
    page_title="🎙 Yaaba AI Voice Translator",
    page_icon="🎙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .description-text {
        text-align: center;
        font-size: 16px;
        color: #555;
        margin: 20px 0;
        line-height: 1.6;
    }
    
    .footer-credit {
        text-align: center;
        font-size: 12px;
        color: #888;
        margin-top: 30px;
        padding: 10px;
        border-top: 1px solid #eee;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    .translation-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for models
@st.cache_resource
def load_models():
    """Load all AI models with caching"""
    with st.spinner("🔄 Loading AI models... This may take a few minutes on first run."):
        try:
            # Load Whisper model
            whisper_model = whisper.load_model("small")
            
            # Load translation model
            translation_model_name = "mafromedia/yaaba-fr-mo-nllb600M"
            translation_tokenizer = AutoTokenizer.from_pretrained(translation_model_name)
            translation_model = AutoModelForSeq2SeqLM.from_pretrained(translation_model_name)
            
            # Load TTS model
            tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
            
            return whisper_model, translation_tokenizer, translation_model, tts
            
        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
            return None, None, None, None

# Language mapping
LANGUAGE_CODES = {
    "French": "fra_Latn",
    "Mooré": "mos_Latn"
}

def transcribe_audio(audio_data, whisper_model):
    """Convert speech to text using Whisper"""
    try:
        if audio_data is None:
            return "No audio provided"
        
        # Save audio data to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            sf.write(tmp_file.name, audio_data, 16000)  # Assuming 16kHz sample rate
            result = whisper_model.transcribe(tmp_file.name)
            os.unlink(tmp_file.name)  # Clean up
            
        return result["text"].strip()
    except Exception as e:
        return f"Error in transcription: {str(e)}"

def translate_text(text, source_lang, target_lang, tokenizer, model):
    """Translate text using the custom NLLB model"""
    try:
        if not text.strip():
            return "No text to translate"
        
        # Get language codes
        src_code = LANGUAGE_CODES[source_lang]
        tgt_code = LANGUAGE_CODES[target_lang]
        
        # Tokenize input
        inputs = tokenizer(
            text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=512
        )
        
        # Set target language
        tokenizer.src_lang = src_code
        
        # Generate translation
        with torch.no_grad():
            generated_tokens = model.generate(
                **inputs,
                forced_bos_token_id=tokenizer.lang_code_to_id[tgt_code],
                max_length=512,
                num_beams=5,
                early_stopping=True
            )
        
        # Decode translation
        translation = tokenizer.batch_decode(
            generated_tokens, 
            skip_special_tokens=True
        )[0]
        
        return translation.strip()
    except Exception as e:
        return f"Translation error: {str(e)}"

def text_to_speech(text, language, tts_model):
    """Convert text to speech using Coqui TTS"""
    try:
        if not text.strip() or "error" in text.lower():
            return None
        
        # Create temporary file for audio output
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            output_path = tmp_file.name
        
        # Generate speech
        lang_code = "fr" if language == "French" else "en"  # Fallback to English for Mooré
        
        tts_model.tts_to_file(
            text=text,
            file_path=output_path,
            language=lang_code
        )
        
        return output_path
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")
        return None

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎙 Yaaba AI – French ↔ Mooré Voice Translator</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Description
    st.markdown("""
    <div class="description-text">
        <p>Bridge the gap between African and global languages with AI-powered translation. 
        Yaaba AI enables seamless communication between French and Mooré (Moore), 
        one of West Africa's major languages, through advanced speech recognition, 
        neural machine translation, and text-to-speech synthesis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load models
    whisper_model, translation_tokenizer, translation_model, tts = load_models()
    
    if not all([whisper_model, translation_tokenizer, translation_model, tts]):
        st.error("Failed to load AI models. Please refresh the page and try again.")
        return
    
    # Create tabs
    tab1, tab2 = st.tabs(["🎤 Voice Translation", "📝 Text Translation"])
    
    with tab1:
        st.subheader("Voice Translation")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Language direction selector
            direction = st.radio(
                "Translation Direction",
                ["French → Mooré", "Mooré → French"],
                index=0
            )
            
            # Audio input
            st.write("Record your voice:")
            audio_data = st.audio_input("Record audio")
            
            # Process button
            if st.button("🔄 Translate Voice", key="voice_translate"):
                if audio_data is not None:
                    # Read audio data
                    audio_bytes = audio_data.read()
                    audio_array, sample_rate = sf.read(io.BytesIO(audio_bytes))
                    
                    # Determine languages
                    if direction == "French → Mooré":
                        source_lang, target_lang = "French", "Mooré"
                    else:
                        source_lang, target_lang = "Mooré", "French"
                    
                    with st.spinner("Processing your audio..."):
                        # Step 1: Transcribe
                        with st.spinner("🎧 Converting speech to text..."):
                            transcribed_text = transcribe_audio(audio_array, whisper_model)
                        
                        # Step 2: Translate
                        if "Error" not in transcribed_text:
                            with st.spinner("🔄 Translating text..."):
                                translated_text = translate_text(
                                    transcribed_text, source_lang, target_lang, 
                                    translation_tokenizer, translation_model
                                )
                            
                            # Step 3: Synthesize speech
                            if "error" not in translated_text.lower():
                                with st.spinner("🔊 Generating speech..."):
                                    audio_output = text_to_speech(translated_text, target_lang, tts)
                        
                        # Store results in session state
                        st.session_state.voice_detected = transcribed_text
                        st.session_state.voice_translated = translated_text if "Error" not in transcribed_text else ""
                        st.session_state.voice_audio = audio_output if "Error" not in transcribed_text and "error" not in translated_text.lower() else None
                else:
                    st.warning("Please record some audio first!")
        
        with col2:
            # Results
            st.write("**Detected Text:**")
            if 'voice_detected' in st.session_state:
                st.markdown(f'<div class="translation-box">{st.session_state.voice_detected}</div>', 
                           unsafe_allow_html=True)
            else:
                st.info("Your spoken words will appear here...")
            
            st.write("**Translation:**")
            if 'voice_translated' in st.session_state:
                st.markdown(f'<div class="translation-box">{st.session_state.voice_translated}</div>', 
                           unsafe_allow_html=True)
            else:
                st.info("Translation will appear here...")
            
            # Audio output
            if 'voice_audio' in st.session_state and st.session_state.voice_audio:
                st.write("**🔊 Translation Audio:**")
                with open(st.session_state.voice_audio, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/wav")
    
    with tab2:
        st.subheader("Text Translation")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Language direction selector
            text_direction = st.radio(
                "Translation Direction",
                ["French → Mooré", "Mooré → French"],
                index=0,
                key="text_direction"
            )
            
            # Text input
            text_input = st.text_area(
                "Enter text to translate:",
                placeholder="Type your text here...",
                height=150
            )
            
            # Translate button
            if st.button("🔄 Translate Text", key="text_translate"):
                if text_input.strip():
                    # Determine languages
                    if text_direction == "French → Mooré":
                        source_lang, target_lang = "French", "Mooré"
                    else:
                        source_lang, target_lang = "Mooré", "French"
                    
                    with st.spinner("Translating your text..."):
                        # Translate
                        translated_text = translate_text(
                            text_input, source_lang, target_lang,
                            translation_tokenizer, translation_model
                        )
                        
                        # Generate speech
                        if "error" not in translated_text.lower():
                            audio_output = text_to_speech(translated_text, target_lang, tts)
                        else:
                            audio_output = None
                        
                        # Store results
                        st.session_state.text_translated = translated_text
                        st.session_state.text_audio = audio_output
                else:
                    st.warning("Please enter some text to translate!")
        
        with col2:
            # Results
            st.write("**Translation:**")
            if 'text_translated' in st.session_state:
                st.markdown(f'<div class="translation-box">{st.session_state.text_translated}</div>', 
                           unsafe_allow_html=True)
            else:
                st.info("Translation will appear here...")
            
            # Audio output
            if 'text_audio' in st.session_state and st.session_state.text_audio:
                st.write("**🔊 Translation Audio:**")
                with open(st.session_state.text_audio, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/wav")
    
    # Footer
    st.markdown("""
    <div class="footer-credit">
        <p>Built by <strong>GO AI Corp</strong> – <em>Yaaba AI Initiative</em></p>
        <p>Empowering African languages through artificial intelligence</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()