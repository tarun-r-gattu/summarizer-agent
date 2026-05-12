import requests
from utils.chunking import chunk_text
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"

load_dotenv(env_path)

def call_llm(prompt):
    url = os.getenv("DATABRICKS_ENDPOINT")
    headers = {
        "Authorization": f"Bearer {os.getenv("DATABRICKS_API_KEY")}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful summarization assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def summarize_content(text):
    # MAX_CHARS = 15000  # adjust based on modelz
    # if len(text) > MAX_CHARS:
    #     text = text[:MAX_CHARS]

    prompt = f"""
    Summarize the following document.

    Focus on:
    - Key points
    - Important details
    - Conclusions

    Keep the summary concise and well-structured.

    Document:
    {text}
    """

    result = call_llm(prompt)

    return result["choices"][0]["message"]["content"]

    # =============== CHUNKING MODE ================
    # chunks = chunk_text(text)
    
    # summaries = []
    
    # for chunk in chunks:
    #     prompt = f"Summarize the following:\n\n{chunk}"
    #     result = call_llm(prompt)
    #     summaries.append(result["choices"][0]["message"]["content"])
    
    # combined = "\n".join(summaries)

    # final_prompt = f"Provide a concise summary of the following:\n{combined}"
    # final_summary = call_llm(final_prompt)

    # return final_summary["choices"][0]["message"]["content"]