import streamlit as st
import os
from utils.parser import read_pdf, read_docx
from utils.summarizer import summarize_content
from utils.folder_summarizer import summarize_folder

# Page config
st.set_page_config(
    page_title="Document Summarizer",
    page_icon="📄",
    layout="wide"
)

# Header
st.title("Document Summarizer Agent")
st.caption("Summarize individual documents or entire folders")

# Sidebar
st.sidebar.header("⚙️ Settings")
expand_all = st.sidebar.checkbox("Expand all summaries", value=False)

# Create Tabs
tab1, tab2 = st.tabs(["📂 Folder Summarization", "📄 Document Upload"])

# =========================
#  TAB 1: FOLDER
# =========================
with tab1:
    st.subheader("Summarize Documents in a Folder")

    folder_path = st.text_input(
        "Enter folder path",
        placeholder=""
    )

    if st.button(" Summarize Folder", use_container_width=True):
        if not folder_path:
            st.error(" Please enter a folder path")
        else:
            try:
                with st.spinner("🔍 Processing folder..."):
                    results = summarize_folder(folder_path)

                st.success(f"Processed {len(results)} files")

                cols = st.columns(1)

                for idx, (file, summary) in enumerate(results.items()):
                    filename = os.path.basename(file)

                    with cols[idx % 1]:
                        st.markdown(f"### 📄 {filename}")

                        with st.expander("View Summary", expanded=expand_all):
                            if "Error:" in summary:
                                st.error(summary)
                            else:
                                st.write(summary)

            except Exception as e:
                st.error(f"Error: {str(e)}")

# =========================
# 📄 TAB 2: SINGLE FILE
# =========================
with tab2:
    st.subheader("Upload and Summarize a Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF or Word document",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if st.button("Submit", use_container_width=True):
        if not uploaded_file:
            st.error("❌ Please upload at least one document")
        else:
            for file in uploaded_file:
                try:
                    # Extract text
                    if file.type == "application/pdf":
                        text = read_pdf(file)
                    else:
                        text = read_docx(file)

                    # Summarize on button click
                    with st.spinner(f"📊 Analyzing {file.name}..."):
                        summary = summarize_content(text)

                    st.success(f"✅ Summary generated for {file.name}")

                    with st.expander(f"View Summary - {file.name}", expanded=True):
                        st.write(summary)
                
                except Exception as e:
                    st.error(f"Error processing {file.name}: {str(e)}")

