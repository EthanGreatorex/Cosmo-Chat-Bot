
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
def show_cosmo(AI_CONTEXT, isFile,fileType):
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

# VARIABLES
# This will hold any website data the user wants to give to the AI as context
AI_CONTEXT = ''

st.set_page_config(layout='wide')
st.markdown(
    """
<style>
section.stMain.st-emotion-cache-bm2z3a.eht7o1d1 {
  background: url(https://images.unsplash.com/photo-1713755001325-0d19ad4d271d?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)
}

header.stAppHeader.st-emotion-cache-1fxioj7.e4hpqof0 {
  background: url(https://images.unsplash.com/photo-1713755001325-0d19ad4d271d?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)
}

div.st-emotion-cache-a6qe2i.e1c29vlm7 {
  background-color: #0b0613;
}

div.st-emotion-cache-kgpedg.e1c29vlm10 {
  background-color: #0b0613;
}

div.st-emotion-cache-1i2wz1k.e1c29vlm9 {
  background-color: #0b0613;
}

section.stSidebar.st-emotion-cache-97h5g8.e1c29vlm0 {
  background-color: #0b0613;
}

div.st-emotion-cache-1y34ygi.eht7o1d7 {
  background-color: #000000;
}

</style>
""",
    unsafe_allow_html=True,
)

st.image(image='images/cosmo.png', width=70)
st.title("Hello! I'm Cosmo 😀")

st.info("_Would you like to give me some context?_")
st.info("_Click on the top left arrow to upload a website link or a pdf, txt, csv file!_")
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
    st.subheader("Upload File")
    file_upload = st.file_uploader("", type=['pdf','csv','txt'])
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
                        else:
                            st.success("Transcipt fetched!")
                            AI_CONTEXT = TRANSCRIPT
                            show_cosmo(AI_CONTEXT,False,'url')
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
                    if url:
                        AI_CONTEXT = url

                    print(AI_CONTEXT)
                    
                    show_cosmo(AI_CONTEXT, False,'url')
                    if url:
                        st.success("Context Uploaded!")