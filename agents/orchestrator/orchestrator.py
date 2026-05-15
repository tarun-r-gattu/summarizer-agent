from agents.summarizer.service import SummarizerService


class Orchestrator:

    def __init__(self):
        self.summarizer = SummarizerService()

    def summarize_folder(self, files):
        return self.summarizer.summarize_files(files)

    def explain_file(self, file_obj):
        return self.summarizer.explain_file(file_obj)