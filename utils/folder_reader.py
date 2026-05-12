import os


def get_files_from_folder(folder_path, extensions=(".pdf", ".docx")):
    if not os.path.exists(folder_path):
        raise Exception("Folder path does not exist")

    if not os.path.isdir(folder_path):
        raise Exception("Provided path is not a folder")

    files = []
    for filename in sorted(os.listdir(folder_path)):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path) and filename.lower().endswith(extensions):
            files.append(full_path)

    return files
