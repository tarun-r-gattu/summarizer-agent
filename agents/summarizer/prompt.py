def folder_summary_prompt(text: str) -> str:
    return f"""
You are a document summarizer.

Your task:
Summarize multiple documents into one clear overview.

Instructions:
- Combine insights across all documents
- Avoid repetition
- Keep it concise and structured

Output format:
1. Overview
2. Key Points
3. Conclusion

Documents:
{text}
"""


def file_explain_prompt(text: str) -> str:
    return f"""
You are an expert analyst.

Your task:
Explain this document clearly and in depth.

Instructions:
- Summarize the document
- Highlight key ideas
- Explain important details

Output format:
1. Summary
2. Key Concepts
3. Detailed Explanation

Document:
{text}
"""