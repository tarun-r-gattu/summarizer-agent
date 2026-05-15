from agents.summarizer.agent import SummarizerAgent
from utils.parser import read_pdf, read_docx


class SummarizerService:

    def __init__(self):
        self.agent = SummarizerAgent()

    def _read_file(self, file_obj):
        if hasattr(file_obj, "type"):
            # Uploaded file
            file_obj.seek(0)

            if file_obj.name.lower().endswith(".pdf"):
                return read_pdf(file_obj)

            elif file_obj.name.lower().endswith(".docx"):
                return read_docx(file_obj)

            else:
                raise Exception("Unsupported file type")

        else:
            # File path
            if file_obj.lower().endswith(".pdf"):
                return read_pdf(file_obj)

            elif file_obj.lower().endswith(".docx"):
                return read_docx(file_obj)

            else:
                raise Exception("Unsupported file type")

    def summarize_files(self, files):
        texts = []
        failed = []

        for f in files:
            try:
                text = self._read_file(f)

                if text:
                    texts.append(text)
            except Exception as e:
                failed.append(str(f))

        if not texts:
            raise Exception("No readable content found.")

        combined_text = "\n\n".join(texts)

        # IMPORTANT: this is where chunking will go later
        summary = self.agent.summarize_text(combined_text)

        if failed:
            summary += "\n\nFailed files:\n" + "\n".join(failed)

        return summary

    def explain_file(self, file_obj):
        text = self._read_file(file_obj)

        if not text:
            raise Exception("File is empty")

        return self.agent.explain_text(text)
