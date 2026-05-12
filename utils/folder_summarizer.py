import os
from utils.parser import read_pdf, read_docx
from utils.folder_reader import get_files_from_folder
from utils.summarizer import summarize_content, summarize_text


def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        return read_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return read_docx(file_path)
    else:
        return None


def summarize_file(file_path):
    text = extract_text(file_path)
    if not text:
        raise Exception("Unsupported file type")
    return summarize_content(text)


def explain_file(file_path):
    text = extract_text(file_path)
    if not text:
        raise Exception("Unsupported file type")
    return summarize_text(text, mode="explain")


def summarize_folder_overall(folder_path):
    file_paths = get_files_from_folder(folder_path)
    if not file_paths:
        raise Exception("No supported PDF or DOCX files were found in the folder.")

    combined_texts = []
    failed_files = []

    for file_path in file_paths:
        try:
            text = extract_text(file_path)
            if text:
                file_name = os.path.basename(file_path)
                combined_texts.append(f"File: {file_name}\n{text}")
        except Exception as e:
            failed_files.append(f"{os.path.basename(file_path)}: {str(e)}")

    if not combined_texts:
        raise Exception("No readable files were found in the selected folder.")

    combined_document = "\n\n".join(combined_texts)
    summary = summarize_content(combined_document)

    if failed_files:
        summary += "\n\nSome files could not be read:\n" + "\n".join(failed_files)

    return summary
