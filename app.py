import streamlit as st
import fitz

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Page configuration
st.set_page_config(
    page_title="OpsCopilot",
    page_icon="🤖",
    layout="wide"
)


# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Demo login
USERS = {
    "admin": "opscopilot123",
    "demo": "demo123"
}


# Login page
def login_page():

    st.title("🤖 OpsCopilot")
    st.subheader("AI Operations Copilot")

    st.write(
        "A Generative AI assistant for document intelligence "
        "and everyday business operations."
    )

    st.divider()

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("🔐 Login", use_container_width=True):

        if username in USERS and USERS[username] == password:

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error("Invalid username or password.")


# Document processing
def process_document(uploaded_file):

    pdf_bytes = uploaded_file.read()

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in document:
        text += page.get_text()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(
        chunks,
        embedding=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    return document, chunks, retriever


# Main application
def main_app():

    api_key = st.secrets["GOOGLE_API_KEY"]

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )

    st.title("🤖 OpsCopilot")

    st.caption(
        "AI-powered document intelligence and workplace productivity assistant"
    )

    with st.sidebar:

        st.header("⚙️ Workspace")

        st.write("Welcome to OpsCopilot.")

        if st.button("🚪 Logout"):

            st.session_state.logged_in = False
            st.rerun()

    tab1, tab2, tab3 = st.tabs(
        [
            "📄 Document Intelligence",
            "📝 Meeting Intelligence",
            "✉️ Email Generator"
        ]
    )

    # Document Intelligence
    with tab1:

        st.header("📄 Document Intelligence")

        st.write(
            "Upload a PDF and ask questions using "
            "Retrieval-Augmented Generation."
        )

        uploaded_file = st.file_uploader(
            "Upload a PDF document",
            type=["pdf"]
        )

        if uploaded_file:

            with st.spinner("Processing document..."):

                try:

                    document, chunks, retriever = process_document(
                        uploaded_file
                    )

                    st.success(
                        "Document processed successfully."
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "📄 Pages",
                        len(document)
                    )

                    col2.metric(
                        "🧩 Text Chunks",
                        len(chunks)
                    )

                    col3.metric(
                        "🔍 Retrieval",
                        "Active"
                    )

                    question = st.text_input(
                        "Ask a question about your document"
                    )

                    if question:

                        with st.spinner(
                            "Finding answer..."
                        ):

                            documents = retriever.invoke(
                                question
                            )

                            context = "\n\n".join(
                                doc.page_content
                                for doc in documents
                            )

                            prompt = f"""
You are OpsCopilot, an AI Operations Assistant.

Answer the question using only the provided context.

If the answer is not available in the context,
say that the information was not found in the document.

Context:
{context}

Question:
{question}

Give a clear and concise answer.
"""

                            response = llm.invoke(
                                prompt
                            )

                            st.subheader(
                                "💡 Answer"
                            )

                            st.write(
                                response.content
                            )

                            with st.expander(
                                "📚 Retrieved Sources"
                            ):

                                for i, doc in enumerate(
                                    documents,
                                    1
                                ):

                                    st.write(
                                        f"**Source {i}**"
                                    )

                                    st.write(
                                        doc.page_content
                                    )

                except Exception:

                    st.error(
                        "Unable to process the document. "
                        "Please try another PDF."
                    )

    # Meeting Intelligence
    with tab2:

        st.header("📝 Meeting Intelligence")

        st.write(
            "Convert meeting notes into clear actions and decisions."
        )

        notes = st.text_area(
            "Paste your meeting notes",
            height=250
        )

        if st.button(
            "🧠 Analyze Meeting",
            use_container_width=True
        ):

            if not notes.strip():

                st.warning(
                    "Please enter meeting notes first."
                )

            else:

                with st.spinner(
                    "Analyzing meeting..."
                ):

                    prompt = f"""
Analyze the following meeting notes.

Return the response using these sections:

## Summary

## Key Decisions

## Action Items

## Deadlines

Meeting Notes:
{notes}
"""

                    response = llm.invoke(
                        prompt
                    )

                    st.markdown(
                        response.content
                    )

    # Email Generator
    with tab3:

        st.header("✉️ Email Generator")

        st.write(
            "Generate professional emails using natural language instructions."
        )

        tone = st.selectbox(
            "Select Email Tone",
            [
                "Professional",
                "Formal",
                "Friendly",
                "Concise"
            ]
        )

        instruction = st.text_area(
            "What should the email say?",
            height=200
        )

        if st.button(
            "✉️ Generate Email",
            use_container_width=True
        ):

            if not instruction.strip():

                st.warning(
                    "Please enter an email instruction first."
                )

            else:

                with st.spinner(
                    "Writing email..."
                ):

                    prompt = f"""
Write a {tone.lower()} professional email.

User instruction:
{instruction}

Include:

Subject:
Greeting:
Email Body:
Professional Closing:
"""

                    response = llm.invoke(
                        prompt
                    )

                    st.markdown(
                        response.content
                    )


# Start application
if st.session_state.logged_in:

    main_app()

else:

    login_page()
