
# IMPORTS
import streamlit as st
from ai_model import *


st.set_page_config(layout='wide')


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
    st.session_state.messages = [{"role":"assistant","content":"Hello! I'm Cosmo. How can I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar='./images/cosmo.png'):
        st.markdown(message["content"])



prompt = st.chat_input("Type message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar='./images/cosmo.png'):
        response = get_resp(prompt)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

