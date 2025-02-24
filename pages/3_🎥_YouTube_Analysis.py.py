import streamlit as st
from fetch_youtube_data import fetch_youtube_transcipt

st.set_page_config(
    layout="wide",
)

@st.cache_data
def get_youtube_transcript(url):
    return fetch_youtube_transcipt(url)

st.image(image='images/cosmo.png', width=150)
st.info("Hello! Here you can give me a YouTube video link to fetch the transcript! 🎥")
st.info("Be warned... YouTube doesn't like me very much and might block me! 😅")
url = st.text_input("Enter YouTube video URL:")

if url:
    with st.spinner("Fetching transcript..."):
        transcript = get_youtube_transcript(url)
        if transcript in ['Not a valid Youtube Link', 'ERROR']:
            st.error("Request blocked or invalid YouTube link.")
        else:
            st.success("Transcript fetched successfully!")
            AI_CONTEXT = transcript
            st.session_state["AI_CONTEXT"] = AI_CONTEXT
            st.info("I've got the transcript!! Head over to Chat with Cosmo to ask me some questions!")
