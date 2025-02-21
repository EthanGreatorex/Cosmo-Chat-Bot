
from groq import Groq

GROQ_API_KEY = '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'

def get_resp(prompt: str, context : str, prevchat : str, ispdf) -> str:

    client = Groq(
        api_key=GROQ_API_KEY
    )

    if not ispdf:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"You are a friendly assitant named Cosmo. Your answer to any question must relate to the content of the url, markdown or user context if one is provided. Use nice formatting such as bullet points.Make use of emojis to enhance user experience but don't use a lot. You will also be given a prompt. You will also be given your previous conversation. CONTEXT: {context} PROMPT (may be a document in text form): {prompt} PREVIOUS CHATS: {prevchat}",
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
        except Exception:
            return "ERROR"
        else:
            return chat_completion.choices[0].message.content
    else:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"You are a friendly assitant named Cosmo. The user has uploaded a pdf file and I have converted it into text for you. You will receive a prompt, the context of the pdf file and the previous conversations you have had. Use nice formatting in your reponse through bullet points and emojis. CONTEXT: {context} PROMPT: {prompt} PREVIOUS CHATS: {prevchat}",
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
        except Exception:
            return "ERROR"
        else:
            return chat_completion.choices[0].message.content
