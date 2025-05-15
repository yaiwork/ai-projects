import os
import openai
#from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")
def summarize_text(text, model="gpt-4"): # gpt-3.5-turbo
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful summarizer."},
            {"role": "user", "content": f"Summarize this text:\n\n{text}"}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()


def chat_with_summary(summary, user_message, chat_history=None, model="gpt-4"): #gpt-3.5-turbo
    messages = [{"role": "system", "content": "You are a helpful assistant answering follow-up questions about a text summary."}]
    messages.append({"role": "assistant", "content": f"The summary of the text is:\n\n{summary}"})

    if chat_history:
        messages.extend(chat_history)

    messages.append({"role": "user", "content": user_message})

    response = openai.chat.completions.create( # client
        model=model,
        messages=messages,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
