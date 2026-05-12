import os

def get_files_from_folder(folder_path):
    if not os.path.exists(folder_path):
        raise Exception("Folder path does not exist")

    files = []

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        if os.path.isfile(full_path) and filename.endswith((".pdf", ".docx")):
            files.append(full_path)

    return files