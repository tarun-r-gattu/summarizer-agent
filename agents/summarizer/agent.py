from llm.llm_provider import get_llm
from agents.summarizer.prompt import (
    folder_summary_prompt,
    file_explain_prompt,
)


class SummarizerAgent:

    def __init__(self):
        self.llm = get_llm()

    def summarize_text(self, text: str) -> str:
        """
        Hook point for future chunking.
        """
        prompt = folder_summary_prompt(text)
        return self.llm.invoke(prompt)

    def explain_text(self, text: str) -> str:
        prompt = file_explain_prompt(text)
        return self.llm.invoke(prompt)