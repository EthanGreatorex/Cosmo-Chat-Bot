import streamlit as st
from ai_model import *
import requests
from pdf_to_text import *

# FUNCTIONS
@st.cache_data
def get_pdf_text(file):
    return convert_pdf_to_txt(file)


# VARIABLES
AI_CONTEXT = ''

st.set_page_config(layout='wide', page_title='Cosmo Chatbot', page_icon='./images/cosmo.png')


if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.image(caption='Cosmo', image='./images/cosmo.png', width=100)
    st.info("Hello! I'm Cosmo 😀")
    st.info("Click the top left arrow to get started ↖️ 😀")
    st.info("Want to switch to light mode?☀️ Click on the three dots in the top right↗️")
    st.divider()


with st.sidebar:
    st.image(caption='Cosmo', image='./images/cosmo.png', width=100)
    st.info("Hello again! Provide me with some context to make our chats more meaningful🥳")
    st.divider()

   
    st.subheader("🌐Website URL🌐")
    url = st.sidebar.text_input(label="Enter URL")
    st.divider()

    st.subheader("😭Comso Config😁")
    mood_config = st.radio(label="Mood Options", options=["Happy", "Sad", "Angry"])
    st.divider()
    
    st.subheader("🗃️Upload File🗃️")
    file_upload = st.file_uploader("Upload your file:", type=['pdf', 'csv', 'txt'])

    st.divider()
    st.write("###### _Original logo design created by stockgiu on [FreePik](%s)_" % 'https://www.freepik.com/author/stockgiu')

    
    if url:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                st.success("Website verified!")
        except Exception:
            st.error("That webpage doesn't seem to exist.")
        AI_CONTEXT = url

  
    if file_upload:
        with st.spinner("Processing file..."):
            if file_upload.type == 'application/pdf':
                text = get_pdf_text(file_upload)
                AI_CONTEXT = text
            elif file_upload.type == 'text/plain':
                AI_CONTEXT = file_upload.read().decode('utf-8')
            elif file_upload.type == 'text/csv':
                AI_CONTEXT = file_upload.read().decode('utf-8')
        st.success("File processed successfully!")


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
    st.session_state.messages = [{"role": "assistant", "content": "Send me a message and I'll respond!"}]

# Display the chat history
for message in st.session_state.messages:
    if message['role'] == 'assistant':
        with st.chat_message(message["role"], avatar='./images/cosmo.png'):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


prompt = st.chat_input("Type message...")


if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Process the assistant's response
    with st.chat_message("assistant", avatar='./images/cosmo.png'):
        match mood_config:
            case "Happy":
                mood = "happy"
            case "Sad":
                mood = "sad"
            case "Angry":  
                mood = "angry"
            case _:
                mood = "happy"

        response, tokens_used, time_taken, model_used = get_resp(prompt, AI_CONTEXT, st.session_state.messages, mood)
        

        if response == 'ERROR':
            st.markdown("Whoops! I think your input was too large.")
        elif response == 'TOKENS USED':
            st.markdown("Whoops! I think I've run out of tokens! Maybe try a smaller input?")
        elif response.strip() == 'safe' or len(response) < 15:
            st.markdown("Whoops! I think your input was too large.")
        else:
            st.markdown(response)
            st.markdown("_Summary_")
            st.markdown(f"_Tokens used: {tokens_used}_")
            st.markdown(f"_Time taken: {time_taken}_")
            st.markdown(f"_Model Used: {model_used}_")

    st.session_state.messages.append({"role": "assistant", "content": response})

