import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()


class DummyLLM:
    """
    Placeholder LLM until you plug in ChatGPT.
    Replace this with ChatOpenAI later.
    """
    def invoke(self, prompt: str) -> str:
        return f"[LLM OUTPUT]\n{prompt[:300]}..."


def get_llm():
    # later replace with:
    # from langchain_openai import ChatOpenAI
    # return ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    return DummyLLM()


# def get_llm():
#     api_key = os.getenv("OPENAI_API_KEY")

#     if not api_key:
#         raise ValueError("OPENAI_API_KEY is not set in .env")

#     return ChatOpenAI(
#         api_key=api_key,        # explicitly pass it
#         model="gpt-4o-mini",
#         temperature=0.3,
#         max_tokens=2000
#     )

