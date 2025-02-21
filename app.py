
# IMPORTS
import streamlit as st
import requests

# Custom imports
from ai_model import *
from fetch_youtube_data import *
from web_crawler import *
from pdf_to_text import *


# Functions
def show_cosmo(AI_CONTEXT, ispdf):
    with st._main:
        st.markdown(
            """
        <style>
            .st-emotion-cache-janbn0 {
                flex-direction: row-reverse;
                text-align: right;
                background-color:  #140b23;
            }


        </style>
        """,
            unsafe_allow_html=True,
        )


        if "messages" not in st.session_state:
            st.session_state.messages = [{"role":"assistant","content":"Hello! How can I assist you today?😊"}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar='./images/cosmo.png'):
                st.markdown(message["content"])



        prompt = st.chat_input("Type message...")



        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar='./images/cosmo.png'):
                response = get_resp(prompt, AI_CONTEXT, st.session_state.messages, ispdf)
                if response.startswith('ERROR'):
                    st.write("⛔ Context is too large! Please reduce the size of the context.")
                else:
                    st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# VARIABLES
# This will hold any website data the user wants to give to the AI as context
AI_CONTEXT = ''

st.set_page_config(layout='wide')

st.image(image='images/cosmo.png', width=70)
st.title("Hello! I'm Cosmo 😀")

st.info("_Would you like to give me some context?_")
st.info("_Click on the top left arrow to upload a website link or pdf file!_")
st.divider()

with st.sidebar:
    
    st.title("📃Cosmo Context🌐")
    st.divider()
    st.write('##### _YouTube may block the request to access transcripts_')
    st.divider()

    st.subheader("Website Target")
    url = st.sidebar.text_input("Enter URL")
    st.divider()

    st.subheader("Output Options")
    context_type = st.sidebar.radio(
        "",
        options=["HTML","Markdown", "Youtube URL","Chat with Cosmo"]
    )

    st.divider()
    st.subheader("Upload PDF")
    pdf_file = st.file_uploader("", type=['pdf'])
    if pdf_file:
        with st.spinner("Converting to text..."):
            AI_CONTEXT = convert_pdf_to_txt(pdf_file)
            st.success("Context Uploaded!")
            st.write("_Remove pdf file to access website url features_")
            show_cosmo(AI_CONTEXT,True)

    if not pdf_file:
        if context_type:
            with st.spinner("Fetching..."):
                if context_type == 'Youtube URL':
                    if url:
                        # Try and fetch the transcipt
                        TRANSCRIPT = fetch_youtube_transcipt(url)
                        if TRANSCRIPT == 'Not a valid Youtube Link':
                            st.error("Uh oh! This doesn't seem to be a valid Youtube link.")
                        elif TRANSCRIPT == "ERROR":
                            st.error("Request blocked by YouTube")
                        else:
                            st.success("Transcipt fetched!")
                            AI_CONTEXT = TRANSCRIPT
                            show_cosmo(AI_CONTEXT,False)
                            if url:
                                st.success("Context Uploaded!")
                    
                elif context_type == 'HTML':
                    if url:
                        # Check to see if the link exists

                        try:
                            response = requests.get(url)
                            if response.status_code == 200:
                                st.success("Website verified!")
                        except Exception:
                            st.error("That webpage doesn't seem to exist.")
                        else:
                            html_data = crawl_website([url], 'html')
                            for i in range(len(html_data)):
                                if html_data[i][1] == None:
                                    st.error(f"Failed to crawl {html_data[i][0]}")
                                    flag = False
                                else:
                                    st.success(f"Successfully crawled: {html_data[i][0]}")
                            with st._main:
                                st.subheader("HTML Result")
                                st.write(html_data)
                elif context_type == 'Markdown':
                    if url:
                        # Check to see if the link exists
                        try:
                            response = requests.get(url)
                            if response.status_code == 200:
                                st.success("Website verified!")
                        except Exception:
                            st.error("That webpage doesn't seem to exist.")
                        else:
                            markdown_data = crawl_website([url], 'markdown')
                            for i in range(len(markdown_data)):
                                if markdown_data[i][1] == None:
                                    st.error(f"Failed to crawl {markdown_data[i][0]}")
                                    flag = False
                                else:
                                    st.success(f"Successfully crawled: {markdown_data[i][0]}")
                            with st._main:
                                st.subheader("Markdown Result")
                                st.write(markdown_data)
                
                elif context_type == 'Chat with Cosmo':
                    AI_CONTEXT = url
                    
                    show_cosmo(AI_CONTEXT, False)
                    if url:
                        st.success("Context Uploaded!")
                



