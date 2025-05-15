import streamlit as st
from summarize import summarize_text, chat_with_summary
import fitz  # PyMuPDF
from docx import Document
from langdetect import detect

st.set_page_config(page_title="Multi-Format Summarizer Chatbot", layout="centered")
st.title("📄 AI Text Summarizer & Chatbot")

st.write("Upload a `.txt`, `.pdf`, or `.docx` file to generate a summary and chat with it.")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "summary" not in st.session_state:
    st.session_state.summary = None

# File processing function
def extract_text(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "txt":
        text = uploaded_file.read().decode("utf-8")
    elif file_type == "pdf":
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in pdf_doc])
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

# File uploader
uploaded_file = st.file_uploader("📁 Choose a file", type=["txt", "pdf", "docx"])

if uploaded_file:
    text, lang = extract_text(uploaded_file)

    if not text:
        st.error("❌ Unsupported or empty file.")
    else:
        trimmed_text = text[:4000]
        st.subheader("📄 Extracted Text Preview")
        st.text_area("Full Text", trimmed_text, height=250)

        if st.button("🧠 Generate Summary"):
            with st.spinner("Summarizing..."):
                st.session_state.summary = summarize_text(trimmed_text)
                st.session_state.chat_history = []  # reset chat on new summary
                st.success("✅ Summary created!")

# Chat section
if st.session_state.summary:
    st.subheader("📝 Summary")
    st.write(st.session_state.summary)

    st.divider()
    st.subheader("💬 Chat with the Summary")

    user_prompt = st.chat_input("Ask a question about the summary...")

    if user_prompt:
        with st.spinner("Thinking..."):
            reply = chat_with_summary(
                st.session_state.summary,
                user_prompt,
                st.session_state.chat_history
            )

        # Store messages
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # Render chat messages (ChatGPT-style)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

