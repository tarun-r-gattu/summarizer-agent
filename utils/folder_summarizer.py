from utils.parser import read_pdf, read_docx
from utils.folder_reader import get_files_from_folder
from utils.summarizer import summarize_content


def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return read_pdf(file_path)
    elif file_path.endswith(".docx"):
        return read_docx(file_path)
    else:
        return None


def summarize_folder(folder_path):
    file_paths = get_files_from_folder(folder_path)
    # file_paths = file_paths[:5]  # limit for testing
    results = {}

    for file_path in file_paths:
        try:
            text = extract_text(file_path)

            if text:
                summary = summarize_content(text)
                results[file_path] = summary
        except Exception as e:
            results[file_path] = f"Error: {str(e)}"

    return results