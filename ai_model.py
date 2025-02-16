
from groq import Groq

GROQ_API_KEY = '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'

def get_resp(prompt, context) -> str:

    client = Groq(
        api_key=GROQ_API_KEY,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"You are a friendly assitant named Cosmo. Here is some context from the user, you must must fetch data from a url if one is provided: {context} Here is your prompt: {prompt}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content
