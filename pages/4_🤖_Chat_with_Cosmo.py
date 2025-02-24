import streamlit as st
from ai_model import get_resp

st.set_page_config(
    layout="wide",
)

def show_cosmo(AI_CONTEXT):
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! How can I help you today? 😊"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar='./images/cosmo.png'):
            st.markdown(message["content"])

    prompt = st.chat_input("Type your message here:")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar='./images/cosmo.png'):
            response, tokens_used, time_taken = get_resp(prompt, AI_CONTEXT, st.session_state.messages)
            if response.startswith('ERROR'):
                st.markdown("⛔ Context is too large! Please reduce the size of the context.")
            elif response.startswith('TOKENS USED'):
                st.markdown("⛔ Tokens used up! Please try again later.")
            else:
                st.markdown(response)
                st.markdown(f"_Tokens used: {tokens_used}_")
                st.markdown(f"_Time taken: {time_taken} seconds_")
        st.session_state.messages.append({"role": "assistant", "content": response})


if "AI_CONTEXT" not in st.session_state:
        AI_CONTEXT = ""
else:
    AI_CONTEXT = st.session_state["AI_CONTEXT"]

show_cosmo(AI_CONTEXT)
