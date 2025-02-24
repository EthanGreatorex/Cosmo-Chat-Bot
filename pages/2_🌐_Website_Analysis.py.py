import streamlit as st
import requests

st.set_page_config(
    layout="wide",
)

st.image(image='images/cosmo.png', width=150)
st.info("Howdy! Here you can give me a website link to analyse! 🌐")
url = st.text_input("Enter the website URL:")

if url:
    with st.spinner("Fetching and analyzing..."):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            st.success("Website verified!")
            st.info("I've received your website! Head over to Chat with Cosmo to ask me some questions!")
            AI_CONTEXT = url
            st.session_state["AI_CONTEXT"] = AI_CONTEXT

        except Exception:
            st.error("The webpage doesn't seem to exist or is unreachable.")
