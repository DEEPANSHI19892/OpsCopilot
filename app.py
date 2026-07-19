import streamlit as st
import fitz

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="OpsCopilot",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# CUSTOM UI DESIGN
# =========================================================

st.markdown("""
<style>

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Main content width */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar border */
    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
    }

    /* Feature cards */
    .feature-card {
        padding: 20px;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        margin-bottom: 15px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Document Intelligence"


# =========================================================
# USERS FROM STREAMLIT SECRETS
# =========================================================

USERS = {
    st.secrets["ADMIN_USERNAME"]: st.secrets["ADMIN_PASSWORD"],
    st.secrets["DEMO_USERNAME"]: st.secrets["DEMO_PASSWORD"],
    st.secrets["USER_USERNAME"]: st.secrets["USER_PASSWORD"]
}


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.markdown(
        """
        <div style="text-align:center; padding-top:80px;">
            <h1>🤖 OpsCopilot</h1>
            <p style="color:#6b7280; font-size:1.3rem;">
               AI Operations Copilot for Workplace Productivity<br>
AI Operations Copilot for Documents, Meetings and Business Communication
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("🔐 Sign in")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if username in USERS and USERS[username] == password:

                st.session_state.logged_in = True

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )


# =========================================================
# DOCUMENT PROCESSING
# =========================================================

def process_document(uploaded_file):

    # Read uploaded PDF
    pdf_bytes = uploaded_file.read()

    # Open PDF
    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    # Extract text
    text = ""

    for page in document:

        text += page.get_text()

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create FAISS vector database
    vectorstore = FAISS.from_texts(
        chunks,
        embedding=embeddings
    )

    # Create retriever
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 3
        }
    )

    return document, chunks, retriever


# =========================================================
# SIDEBAR
# =========================================================

def sidebar():

    with st.sidebar:

        st.markdown(
            """
            <h2>🤖 OpsCopilot</h2>
            <p style="color:#6b7280;">
            AI Operations Workspace
            </p>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.caption("WORKSPACE")

        if st.button(
            "📄  Document Intelligence",
            use_container_width=True
        ):

            st.session_state.page = "Document Intelligence"

        if st.button(
            "📝  Meeting Intelligence",
            use_container_width=True
        ):

            st.session_state.page = "Meeting Intelligence"

        if st.button(
            "✉️  Email Generator",
            use_container_width=True
        ):

            st.session_state.page = "Email Generator"

        st.divider()

        st.caption("ACCOUNT")

        if st.button(
            "🚪  Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.rerun()


# =========================================================
# DOCUMENT INTELLIGENCE
# =========================================================

def document_intelligence(llm):

    st.title("📄 Document Intelligence")

    st.write(
        "Upload a PDF and ask questions using "
        "Retrieval-Augmented Generation."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"]
    )

    if uploaded_file:

        with st.spinner(
            "Processing document..."
        ):

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

                st.divider()

                question = st.text_input(
                    "💬 Ask a question about your document"
                )

                if question:

                    with st.spinner(
                        "Finding answer..."
                    ):

                        # Retrieve relevant document chunks
                        documents = retriever.invoke(
                            question
                        )

                        # Create context
                        context = "\n\n".join(
                            doc.page_content
                            for doc in documents
                        )

                        # RAG prompt
                        prompt = f"""
You are OpsCopilot, an AI Operations Assistant.

Answer the question using only the provided context.

If the answer is not available in the context,
clearly say that the information was not found
in the document.

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
                            "📚 View Retrieved Sources"
                        ):

                            for i, doc in enumerate(
                                documents,
                                1
                            ):

                                st.markdown(
                                    f"**Source {i}**"
                                )

                                st.write(
                                    doc.page_content
                                )

            except Exception as error:

                st.error(
                    "Unable to process this document."
                )

                st.caption(
                    str(error)
                )


# =========================================================
# MEETING INTELLIGENCE
# =========================================================

def meeting_intelligence(llm):

    st.title("📝 Meeting Intelligence")

    st.write(
        "Convert meeting notes into structured summaries "
        "and actionable tasks."
    )

    st.divider()

    notes = st.text_area(
        "Paste your meeting notes",
        height=250,
        placeholder="Paste your meeting notes here..."
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


# =========================================================
# EMAIL GENERATOR
# =========================================================

def email_generator(llm):

    st.title("✉️ Email Generator")

    st.write(
        "Generate professional emails using natural language instructions."
    )

    st.divider()

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
        height=200,
        placeholder="Example: Write an email requesting one day leave..."
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


# =========================================================
# MAIN APPLICATION
# =========================================================

def main_app():

    # Load API key securely
    api_key = st.secrets["GOOGLE_API_KEY"]

    # Initialize Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )

    # Show sidebar
    sidebar()

    # Main header
    st.markdown(
        """
        <div style="padding-bottom:20px;">
            <h1>🤖 OpsCopilot</h1>
            <p style="color:#6b7280; font-size:1.05rem;">
                Your AI workspace for documents, meetings and communication
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Open selected feature
    if st.session_state.page == "Document Intelligence":

        document_intelligence(
            llm
        )

    elif st.session_state.page == "Meeting Intelligence":

        meeting_intelligence(
            llm
        )

    elif st.session_state.page == "Email Generator":

        email_generator(
            llm
        )


# =========================================================
# START APPLICATION
# =========================================================

if st.session_state.logged_in:

    main_app()

else:

    login_page()
