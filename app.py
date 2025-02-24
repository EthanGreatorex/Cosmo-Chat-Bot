# IMPORTS
import streamlit as st
import requests
from pathlib import Path

# Custom imports
from ai_model import *
from fetch_youtube_data import *
from web_crawler import *
from pdf_to_text import *




# Functions
def show_cosmo(AI_CONTEXT, isFile, fileType):
    with st._main:
        st.divider()
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
            if fileType == 'youtube':
                st.session_state.messages = [{"role":"assistant","content":"Hello again! I have received your YouTube context! How can I help?😊"}]
            elif fileType == 'url':
                st.session_state.messages = [{"role":"assistant","content":"Hello again! I have received your website as context! How can I help?😊"}]
            elif fileType == 'nothing':
                st.session_state.messages = [{"role":"assistant","content":"Hello again! I see you didn't give me any context but that's fine!! How can I help?😊"}]
            else:
                st.session_state.messages = [{"role":"assistant","content":"Hello again! I have received your file as context! How can I help?😊"}]

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

# CODE RUN FIRST
#-------------------------------------------------------------------------------

# VARIABLES
# This will hold any website data the user wants to give to the AI as context

AI_CONTEXT = ''



st.set_page_config(layout='wide', page_title='Cosmo', page_icon='images/cosmo.png', initial_sidebar_state='collapsed',)


st.image(image='images/cosmo.png', width=150)
st.info("Hello there! I'm Cosmo 😀")
st.info("I'm here to help you with any questions you may have! 🤔")
st.info("Click on the top left arrow to get started! ↖️↖️")



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
        options=['None',"HTML","Markdown", "Youtube URL","Chat with Cosmo"],
        index=0
    )


    st.divider()
    st.subheader("Upload File")
    file_upload = st.file_uploader("", type=['pdf','csv','txt'])

    st.divider()
    st.write("###### _Original logo design created by stockgiu on [FreePik](%s)_" % 'https://www.freepik.com/author/stockgiu')
    if file_upload is not None:
        with st.spinner("Processing.."):
            if Path(file_upload.name).suffix == '.pdf':
                AI_CONTEXT = convert_pdf_to_txt(file_upload)
                st.success("Context Uploaded!")
                st.write("_Remove pdf file to access website url features_")
                show_cosmo(AI_CONTEXT,True,'pdf')
            elif Path(file_upload.name).suffix == '.txt':
                AI_CONTEXT = file_upload.read().decode('utf-8')
                st.success("Context Uploaded!")
                st.write("_Remove txt file to access website url features_")
                show_cosmo(AI_CONTEXT,True,'txt')
            elif Path(file_upload.name).suffix == '.csv':
                AI_CONTEXT = file_upload.read().decode('utf-8')
                st.success("Context Uploaded!")
                st.write("_Remove csv file to access website url features_")
                show_cosmo(AI_CONTEXT,True,'csv')

    if not file_upload:
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
                            with st._main:
                                st.image('images/cosmo.png', width=150)
                                st.info("✖️Im sorry! I got kicked out by YouTube 😢✖️")
                        else:
                            st.success("Transcipt fetched!")
                            AI_CONTEXT = TRANSCRIPT
                            show_cosmo(AI_CONTEXT,False,'youtube')
                            if url:
                                st.success("Context Uploaded!")
                    else:
                        with st._main:
                            st.divider()
                            st.image('images/cosmo.png', width=150)
                            st.info("✖️No URL provided!✖️")
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
                                st.image('images/cosmo.png', width=150)
                                st.info("Here is what I have found for you! 🕵️‍♂️")
                                st.subheader("HTML Result")
                                st.write(html_data)
                    else:
                        with st._main:
                            st.divider()
                            st.image('images/cosmo.png', width=150)
                            st.info("✖️No URL provided!✖️")
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
                                st.image('images/cosmo.png', width=150)
                                st.info("Here is what I have found for you! 🕵️‍♂️")
                                st.subheader("Markdown Result")
                                st.write(markdown_data)
                    else:
                        with st._main:
                            st.divider()
                            st.image('images/cosmo.png', width=150)
                            st.info("✖️No URL provided!✖️")
                
                elif context_type == 'Chat with Cosmo':
                    if url:
                        type = 'url'
                        st.success("Context Uploaded!")
                        AI_CONTEXT = url
                    else:
                        type = 'nothing'
                        AI_CONTEXT = ''
                
                    show_cosmo(AI_CONTEXT, False,type)

