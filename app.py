
# IMPORTS
import streamlit as st
from ai_model import *
from fetch_youtube_data import *

# VARIABLES
# This will hold any website data the user wants to give to the AI as context
AI_CONTEXT = ''

st.set_page_config(layout='wide')

# Setup a sidebar to enter a youtube url

st.write("_Click on the top left arrow to give Cosmo website links or Youtube links!_")
st.divider()

with st.sidebar:
    url_type = st.sidebar.radio(
        "Select URl Type",
        options=["Web URL", "Youtube URL"]
    )

    url = st.sidebar.text_input("Enter URL")

    if url:
        with st.spinner("Fetching..."):
            if url_type == 'Youtube URL':
                # Try and fetch the transcipt
                TRANSCRIPT = fetch_youtube_transcipt(url)
                if TRANSCRIPT == 'Not a valid Youtube Link':
                    st.error("Uh oh! This doesn't seem to be a valid Youtube link.")
                elif TRANSCRIPT == "ERROR":
                    st.error("Something went wrong... transcripts may be disabled for this video :(")
                else:
                    st.success("Transcipt fetched!")
                    AI_CONTEXT = TRANSCRIPT
                
            elif url_type == 'Web URL':
                AI_CONTEXT = url


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
    st.session_state.messages = [{"role":"assistant","content":"Hello! I'm Cosmo.How can I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar='./images/cosmo.png'):
        st.markdown(message["content"])



prompt = st.chat_input("Type message...")\



if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar='./images/cosmo.png'):
        response = get_resp(prompt, AI_CONTEXT)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

