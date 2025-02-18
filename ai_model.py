
from groq import Groq

GROQ_API_KEY = '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'

def get_resp(prompt: str, context : str, prevchat : str) -> str:

    client = Groq(
        api_key=GROQ_API_KEY
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"You are a friendly assitant named Cosmo. Your answer to any question must relate to the content of the url if one is provided. You will also be given a prompt. You will also be given your previous conversation. CONTEXT: {context} PROMPT: {prompt} PREVIOUS CHATS: {prevchat}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content
