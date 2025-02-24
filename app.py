# Optimized Streamlit App

import streamlit as st
import requests
from pathlib import Path

# Custom imports
from ai_model import *
from fetch_youtube_data import *
from web_crawler import *
from pdf_to_text import *

# Cache for expensive operations
@st.cache_data
def get_pdf_text(file):
    return convert_pdf_to_txt(file)

@st.cache_data
def get_youtube_transcript(url):
    return fetch_youtube_transcipt(url)

@st.cache_data
def crawl_website_data(urls, mode):
    return crawl_website(urls, mode)

# Chat Functionality
def show_cosmo(AI_CONTEXT, isFile, fileType):
    st.markdown(
        """
        <style>
            .st-emotion-cache-janbn0 {
                flex-direction: row-reverse;
                text-align: right;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if "messages" not in st.session_state:
        initial_message = {
            "youtube": "Hello again! I have received your YouTube context! How can I help?😊",
            "url": "Hello again! I have received your website as context! How can I help?😊",
            "nothing": "Hello again! I see you didn't give me any context but that's fine!! How can I help?😊",
            "default": "Hello again! I have received your file as context! How can I help?😊",
        }
        st.session_state.messages = [
            {"role": "assistant", "content": initial_message.get(fileType, initial_message["default"])}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar='./images/cosmo.png'):
            st.markdown(message["content"])


    prompt = st.chat_input("Type message...")


    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar='./images/cosmo.png'):
            response, tokens_used, time_taken = get_resp(prompt, AI_CONTEXT, st.session_state.messages, isFile, fileType)
            if response.startswith('ERROR'):
                st.markdown("⛔ Context is too large! Please reduce the size of the context.")
            elif response.startswith('TOKENS USED'):
                st.markdown("⛔ Tokens used up! Please try again later.")
            else:
                st.markdown(response)
                st.markdown(f"_Tokens used: {tokens_used}_")
                st.markdown(f"_Time taken: {time_taken} seconds_")
        st.session_state.messages.append({"role": "assistant", "content": response})

# Main Application
#-------------------------------------------------------------------------------

st.set_page_config(layout='wide', page_title='Cosmo', page_icon='images/cosmo.png', initial_sidebar_state='collapsed')

st.image(image='images/cosmo.png', width=150)
st.info("Hello there! I'm Cosmo 😀")
st.info("I'm here to help you with any questions you may have! 🤔")
st.info("Click on the top left arrow to get started! ↖️↖️")
st.divider()


with st.sidebar:
    st.image(image='images/cosmo.png', width=90)
    st.info("Hey! This is the context bar...🌐")
    st.info("Select an option to get started!🥳")

    st.divider()

    st.subheader("Website Target")
    url = st.sidebar.text_input("Enter URL")
    st.divider()

    st.subheader("Output Options")
    context_type = st.sidebar.radio(
        "",
        options=['None', "HTML", "Markdown", "Youtube URL", "Chat with Cosmo"],
        index=0
    )

    st.divider()
    st.subheader("Upload File")
    file_upload = st.file_uploader("", type=['pdf', 'csv', 'txt'])

    st.divider()
    st.write("###### _Original logo design created by stockgiu on [FreePik](%s)_" % 'https://www.freepik.com/author/stockgiu')

AI_CONTEXT = ''

if file_upload is not None:
    with st.spinner("Processing.."):
        file_extension = Path(file_upload.name).suffix
        if file_extension == '.pdf':
            AI_CONTEXT = get_pdf_text(file_upload)
            st.success("Context Uploaded!")
            st.write("_Remove pdf file to access website url features_")
            show_cosmo(AI_CONTEXT, True, 'pdf')
        elif file_extension in ['.txt', '.csv']:
            AI_CONTEXT = file_upload.read().decode('utf-8')
            st.success("Context Uploaded!")
            st.write(f"_Remove {file_extension} file to access website url features_")
            show_cosmo(AI_CONTEXT, True, file_extension[1:])

if not file_upload and context_type:
    with st.spinner("Fetching..."):
        if context_type == 'Youtube URL' and url:
            TRANSCRIPT = get_youtube_transcript(url)
            if TRANSCRIPT in ['Not a valid Youtube Link', 'ERROR']:
                st.error("Request has been blocked by YouTube!")
            else:
                AI_CONTEXT = TRANSCRIPT
                st.success("Transcript fetched!")
                show_cosmo(AI_CONTEXT, False, 'youtube')

        elif context_type in ['HTML', 'Markdown'] and url:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                st.success("Website verified!")
                data = crawl_website_data([url], context_type.lower())
                for page, result in data:
                    if result is None:
                        st.error(f"Failed to crawl {page}")
                    else:
                        st.success(f"Successfully crawled: {page}")
                st.write(data)
            except Exception:
                st.error("That webpage doesn't seem to exist or is unreachable.")

        elif context_type == 'Chat with Cosmo':
            if url:
                AI_CONTEXT = url
                st.success("Context Uploaded!")
                typeof = 'url'
            else:
                typeof = 'nothing'
            show_cosmo(AI_CONTEXT, False, typeof)
