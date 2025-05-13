

# app.py

import streamlit as st
from summarize import summarize_text, chat_with_summary
import fitz  # PyMuPDF for PDF reading

st.set_page_config(page_title="Multi-Format Summarizer Chatbot", layout="centered")
st.title("📄 Text Summarizer Chatbot with Chat")
st.write("Upload a `.txt` or `.pdf` file, summarize it, and ask follow-up questions.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



import fitz  # PyMuPDF
from docx import Document
from langdetect import detect

def extract_text(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "txt":
        text = uploaded_file.read().decode("utf-8")
    elif file_type == "pdf":
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_doc:
            text += page.get_text()
    elif file_type == "docx":
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        return None, None

    try:
        language = detect(text)
    except:
        language = "unknown"

    return text, language



#uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])
uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])


if uploaded_file:
    content = extract_text(uploaded_file)

    if not content:
        st.error("Unsupported or empty file.")
    else:
        trimmed_content = content[:4000]

        st.subheader("📄 Extracted Text")
        st.text_area("Full Text", trimmed_content, height=250)

        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(trimmed_content)
                st.session_state.summary = summary
                st.success("✅ Summary generated!")

        if "summary" in st.session_state:
            st.subheader("📝 Summary")
            st.write(st.session_state.summary)

            st.subheader("💬 Ask Follow-up Questions")
            user_input = st.text_input("Your Question:")

            if st.button("Send"):
                with st.spinner("Thinking..."):
                    chat_response = chat_with_summary(
                        st.session_state.summary,
                        user_input,
                        st.session_state.chat_history
                    )
                    st.session_state.chat_history.append({"role": "user", "content": user_input})
                    st.session_state.chat_history.append({"role": "assistant", "content": chat_response})

            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**Bot:** {msg['content']}")

