import streamlit as st
import openai

st.set_page_config(page_title="Healthcare Translation Web App", layout="wide")

from modules import voice_to_text, translation, text_to_speech
from utils import config, error_handler, logger, db
openai.api_key = config.OPENAI_API_KEY
from auth import authenticator
from audio_recorder_streamlit import audio_recorder

# Initialize the database (creates tables if not exists)
db.init_db()

# --- Simple Login/Register (using DB) ---
user = authenticator.login_register()
if not user:
    st.warning("Please login or register to continue.")
    st.stop()

st.title("Healthcare Translation Web App with Generative AI")

# Add instruction regarding microphone permissions
st.info("If this is your first time, please click the record button once to grant microphone permission, then click again to record your message.")

# Language selection: ISO language codes
languages = {
    "English": "en-US",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE"
}
col1, col2 = st.columns(2)
with col1:
    src_lang_name = st.selectbox("Select Source Language", list(languages.keys()), index=0)
with col2:
    tgt_lang_name = st.selectbox("Select Target Language", list(languages.keys()), index=1)
src_language = languages[src_lang_name]
tgt_language = languages[tgt_lang_name]

st.write("### Step 1: Record Your Message")
st.info("Click the record button below. The first click will prompt for permission; click again to record.")

# Live audio recorder returns audio bytes (WAV format)
audio_bytes = audio_recorder()

if audio_bytes is not None:
    st.audio(audio_bytes, format="audio/wav")
    st.info("Processing audio for transcription...")
    try:
        transcript = voice_to_text.transcribe_audio(audio_bytes, language=src_language)
        st.write("**Transcribed Text:**")
        st.text_area("Transcribed Text", transcript, height=150, label_visibility="collapsed")

        st.write("### Step 2: Translate the Text")
        translated_text = translation.translate_text(transcript, source_lang=src_language, target_lang=tgt_language)
        st.write("**Translated Text:**")
        st.text_area("Translated Text", translated_text, height=150, label_visibility="collapsed")

        st.write("### Step 3: Listen to the Translation")
        if st.button("Speak"):
            audio_path = text_to_speech.text_to_audio(translated_text, lang=tgt_language.split("-")[0])
            st.audio(audio_path)

        db.insert_history(user, transcript, translated_text, src_lang_name, tgt_lang_name)
        st.success("Your translation has been saved in your history.")
    except Exception as e:
        error_handler.log_error(e)
        st.error("An error occurred while processing your request. Please try again.")

# display user history
if st.checkbox("Show My History"):
    history = db.get_history(user)
    if history:
        st.write("### Your Translation History")
        for rec in history:
            st.markdown(f"**Date:** {rec['timestamp']} | **Languages:** {rec['source_lang']} → {rec['target_lang']}")
            st.markdown(f"- **Original:** {rec['original_text']}")
            st.markdown(f"- **Translation:** {rec['translated_text']}")
            st.markdown("---")
    else:
        st.info("No history found.")
