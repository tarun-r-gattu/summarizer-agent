import streamlit as st
import html
import os
import re
from utils.folder_reader import get_files_from_folder
from utils.folder_summarizer import summarize_folder_overall, explain_file
from utils.parser import read_pdf, read_docx
from utils.summarizer import summarize_content

# Page config
st.set_page_config(
    page_title="Document Summarizer",
    page_icon="📄",
    layout="wide"
)

# Header
st.title("Document Summarizer Agent")
st.caption("Enter a folder path or select all files in a folder, then search or summarize.")

# Sidebar
st.sidebar.header("⚙️ Settings")
expand_all = st.sidebar.checkbox("Expand all explanations", value=False)

# Initialize session state
if "folder_path" not in st.session_state:
    st.session_state.folder_path = ""
if "folder_files" not in st.session_state:
    st.session_state.folder_files = []
if "folder_source" not in st.session_state:
    st.session_state.folder_source = ""
if "folder_summary" not in st.session_state:
    st.session_state.folder_summary = ""
if "file_explanations" not in st.session_state:
    st.session_state.file_explanations = {}
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "summary_generated" not in st.session_state:
    st.session_state.summary_generated = False
if "folder_error" not in st.session_state:
    st.session_state.folder_error = ""


def get_file_name(file_obj):
    if hasattr(file_obj, "name"):
        return file_obj.name
    return os.path.basename(file_obj)


def search_files(files, pattern):
    if not pattern:
        return []

    try:
        compiled = re.compile(pattern, re.IGNORECASE)
        return [f for f in files if compiled.search(get_file_name(f))]
    except re.error:
        lowercase = pattern.lower()
        return [f for f in files if lowercase in get_file_name(f).lower()]


def summarize_selected_files(files):
    combined_texts = []
    failed_files = []

    for uploaded_file in files:
        try:
            uploaded_file.seek(0)
            if uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
                text = read_pdf(uploaded_file)
            elif uploaded_file.type in [
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "application/msword"
            ] or uploaded_file.name.lower().endswith(".docx"):
                text = read_docx(uploaded_file)
            else:
                raise Exception("Unsupported file type")

            if text:
                combined_texts.append(f"File: {uploaded_file.name}\n{text}")
        except Exception as e:
            failed_files.append(f"{uploaded_file.name}: {str(e)}")

    if not combined_texts:
        raise Exception("No readable files were found in the selected files.")

    combined_document = "\n\n".join(combined_texts)
    summary = summarize_content(combined_document)

    if failed_files:
        summary += "\n\nSome files could not be read:\n" + "\n".join(failed_files)

    return summary


def explain_selected_file(file_obj):
    if hasattr(file_obj, "name"):
        file_obj.seek(0)
        if file_obj.type == "application/pdf" or file_obj.name.lower().endswith(".pdf"):
            text = read_pdf(file_obj)
        elif file_obj.type in [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword"
        ] or file_obj.name.lower().endswith(".docx"):
            text = read_docx(file_obj)
        else:
            raise Exception("Unsupported file type")
        from utils.summarizer import summarize_text
        return summarize_text(text, mode="explain")

    raise Exception("Cannot explain unsupported object type")


st.subheader("Summarize Documents in a Folder")

st.write("Use either a folder path or select all files from a folder. The folder summary appears to the right once it is generated.")

left_col, right_col = st.columns([2, 3])

with left_col:
    folder_path = st.text_input("Enter folder path", value=st.session_state.folder_path, placeholder="C:\\path\\to\\folder")
    if st.button("Load Folder"):
        if not folder_path:
            st.error("Please enter a folder path.")
        else:
            try:
                st.session_state.folder_path = folder_path.strip()
                st.session_state.folder_files = get_files_from_folder(st.session_state.folder_path)
                st.session_state.folder_source = "path"
                st.session_state.folder_summary = ""
                st.session_state.file_explanations = {}
                st.session_state.search_results = []
                st.session_state.search_query = ""
                st.session_state.summary_generated = False
                st.session_state.folder_error = ""
                st.success(f"Loaded {len(st.session_state.folder_files)} supported files from folder.")
            except Exception as e:
                st.session_state.folder_files = []
                st.session_state.folder_error = str(e)
                st.error(st.session_state.folder_error)

    uploaded_files = st.file_uploader(
        "Or select all files from a folder",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Select all files in your folder using the file picker. Search and summarize will work on selected files."
    )

    if uploaded_files:
        st.session_state.folder_files = uploaded_files
        st.session_state.folder_source = "upload"
        st.session_state.folder_path = ""
        st.session_state.folder_summary = ""
        st.session_state.file_explanations = {}
        st.session_state.search_results = []
        st.session_state.search_query = ""
        st.session_state.summary_generated = False
        st.session_state.folder_error = ""
        st.success(f"Selected {len(uploaded_files)} files from folder.")

    if st.session_state.folder_files:
        st.markdown(f"**Loaded files:** {len(st.session_state.folder_files)}")
        with st.expander("Show loaded file list", expanded=False):
            for file_obj in st.session_state.folder_files:
                st.write(f"- {get_file_name(file_obj)}")

    summarize_disabled = len(st.session_state.folder_files) == 0
    if st.button("Summarize Folder", disabled=summarize_disabled):
        if st.session_state.folder_source == "path":
            source_label = "folder path"
        else:
            source_label = "selected files"

        try:
            with st.spinner("🔍 Summarizing the folder contents..."):
                if st.session_state.folder_source == "path":
                    st.session_state.folder_summary = summarize_folder_overall(st.session_state.folder_path)
                else:
                    st.session_state.folder_summary = summarize_selected_files(st.session_state.folder_files)
                st.session_state.summary_generated = True
                st.session_state.file_explanations = {}
                st.success(f"Folder summary generated successfully from {source_label}.")
        except Exception as e:
            st.session_state.folder_error = str(e)
            st.error(f"Error: {st.session_state.folder_error}")

with right_col:
    st.markdown("### Folder Summary")
    if st.session_state.summary_generated:
        summary_text = st.session_state.folder_summary
        st.text_area(
            "Folder summary",
            value=summary_text,
            height=360,
            disabled=True,
            label_visibility="collapsed",
        )

        escaped_summary = (
            html.escape(summary_text)
            .replace('\\', '\\\\')
            .replace('\n', '\\n')
            .replace('"', '\\"')
        )
        # st.markdown(
        #     f"""
        #     <button onclick="navigator.clipboard.writeText(\"{escaped_summary}\")">Copy summary</button>
        #     """,
        #     unsafe_allow_html=True,
        # )
    else:
        st.info("Folder summary will appear here after clicking Summarize Folder.")

st.markdown("---")
st.subheader("Search Files")
search_query = st.text_input(
    "Search file names (regex)",
    value=st.session_state.search_query,
    disabled=len(st.session_state.folder_files) == 0,
    placeholder="Type a file name or regex"
)
search_button = st.button("Search Files", disabled=len(st.session_state.folder_files) == 0)

if search_button:
    st.session_state.search_query = search_query
    st.session_state.search_results = search_files(st.session_state.folder_files, search_query.strip())
    if not st.session_state.search_results:
        st.info("No matching files found.")

if st.session_state.search_results:
    st.markdown("### Matching Files")
    for idx, file_obj in enumerate(st.session_state.search_results):
        file_name = get_file_name(file_obj)
        cols = st.columns([4, 1])
        cols[0].markdown(f"**{file_name}**")
        explain_key = f"explain_{idx}_{file_name}"
        if cols[1].button("Explain", key=explain_key):
            try:
                if st.session_state.folder_source == "path":
                    st.session_state.file_explanations[file_obj] = explain_file(file_obj)
                else:
                    st.session_state.file_explanations[file_name] = explain_selected_file(file_obj)
            except Exception as e:
                st.error(f"Error generating explanation: {str(e)}")

        if st.session_state.folder_source == "path":
            expl_key = file_obj
        else:
            expl_key = file_name

        if expl_key in st.session_state.file_explanations:
            with st.expander(f"Deeper Explanation - {file_name}", expanded=expand_all):
                st.write(st.session_state.file_explanations[expl_key])

if not st.session_state.folder_files:
    st.info("Enter a folder path or select files from a folder to enable search and summarization.")
