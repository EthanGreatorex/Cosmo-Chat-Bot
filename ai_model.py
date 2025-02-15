import os
from dotenv import load_dotenv
from groq import Groq

def get_resp(prompt) -> str:
    # Load environment variables from .env file
    load_dotenv()

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"You are a friendly assitant named Cosmo. Here is your prompt: {prompt}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content
