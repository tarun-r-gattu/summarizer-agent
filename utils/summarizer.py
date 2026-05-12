import requests
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"

load_dotenv(env_path)

def has_llm_config():
    return bool(os.getenv("DATABRICKS_ENDPOINT")) and bool(os.getenv("DATABRICKS_API_KEY"))


def mock_summary(text, mode="summary", error=None):
    file_count = text.count("File:")
    if mode == "explain":
        title_line = next((line for line in text.splitlines() if line.startswith("File:")), None)
        doc_label = title_line or "This file"
        explanation = (
            f"MOCK EXPLANATION\n\n"
            f"{doc_label} appears to describe a document with several key sections. "
            "The explanation is a placeholder until a real LLM API key is configured. "
            "It highlights likely themes, structure, and concluding points."
        )
        if error:
            explanation += f"\n\n[Mock fallback due to: {error}]"
        return explanation

    summary = (
        f"MOCK SUMMARY\n\n"
        f"This is a placeholder folder summary for {file_count or 'the selected'} file(s). "
        "A real summary will appear when the LLM API key is configured. "
        "It would otherwise condense the main points, key findings, and overall structure."
    )
    if error:
        summary += f"\n\n[Mock fallback due to: {error}]"
    return summary


def call_llm(prompt):
    url = os.getenv("DATABRICKS_ENDPOINT")
    headers = {
        "Authorization": f"Bearer {os.getenv('DATABRICKS_API_KEY')}",
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
    response.raise_for_status()
    return response.json()


def summarize_text(text, mode="summary"):
    if not has_llm_config():
        return mock_summary(text, mode=mode)

    if mode == "explain":
        prompt = f"""
        Provide a detailed explanation of the following document.
        - Highlight key ideas
        - Describe structure, purpose, and important sections
        - Explain notable terms and conclusions
        - Keep the explanation clear and informative

        Document:
        {text}
        """
    else:
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

    try:
        result = call_llm(prompt)
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return mock_summary(text, mode=mode, error=str(e))


def summarize_content(text):
    return summarize_text(text, mode="summary")
