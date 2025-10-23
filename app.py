import streamlit as st

# Set page config
st.set_page_config(
    page_title="🎙 Yaaba AI Voice Translator",
    page_icon="🎙",
    layout="wide"
)

# Custom CSS for styling
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
</style>
""", unsafe_allow_html=True)

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
    
    # Show that app is loading
    st.info("🚀 App deployed successfully! AI models are loading... This is a test version.")
    
    # Create tabs for future functionality
    tab1, tab2 = st.tabs(["🎤 Voice Translation", "📝 Text Translation"])
    
    with tab1:
        st.subheader("Voice Translation")
        st.info("🔄 AI models are being loaded. Full functionality will be available shortly.")
        
        # Placeholder for voice functionality
        direction = st.radio(
            "Translation Direction",
            ["French → Mooré", "Mooré → French"],
            index=0
        )
        
        st.text_area("Detected Text", placeholder="Your spoken words will appear here...", height=100)
        st.text_area("Translation", placeholder="Translation will appear here...", height=100)
    
    with tab2:
        st.subheader("Text Translation")
        st.info("🔄 AI models are being loaded. Full functionality will be available shortly.")
        
        # Placeholder for text functionality
        text_direction = st.radio(
            "Translation Direction",
            ["French → Mooré", "Mooré → French"],
            index=0,
            key="text_direction"
        )
        
        text_input = st.text_area(
            "Enter text to translate:",
            placeholder="Type your text here...",
            height=100
        )
        
        if st.button("🔄 Translate Text"):
            st.success("Translation feature will be activated once AI models are fully loaded!")
    
    # Footer
    st.markdown("""
    <div class="footer-credit">
        <p>Built by <strong>GO AI Corp</strong> – <em>Yaaba AI Initiative</em></p>
        <p>Empowering African languages through artificial intelligence</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()