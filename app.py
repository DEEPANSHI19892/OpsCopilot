
import streamlit as st
import fitz
import os
import tempfile

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(
    page_title="OpsCopilot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 OpsCopilot")
st.write("AI Operations Copilot for documents and daily work.")

api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password"
)

if api_key:

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )

    option = st.sidebar.selectbox(
        "Choose a feature",
        [
            "Document Q&A",
            "Meeting Intelligence",
            "Email Generator"
        ]
    )

    if option == "Document Q&A":

        uploaded_file = st.file_uploader(
            "Upload a PDF document",
            type=["pdf"]
        )

        if uploaded_file:

            pdf_bytes = uploaded_file.read()

            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            text = ""

            for page in doc:
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

            question = st.text_input(
                "Ask a question about your document"
            )

            if question:

                documents = retriever.invoke(question)

                context = "\n\n".join(
                    doc.page_content
                    for doc in documents
                )

                prompt = f"""
                Answer the question using only the context below.

                Context:
                {context}

                Question:
                {question}

                If the answer is not in the context,
                say that the information was not found.
                """

                response = llm.invoke(prompt)

                st.subheader("Answer")
                st.write(response.content)

    elif option == "Meeting Intelligence":

        notes = st.text_area(
            "Paste meeting notes"
        )

        if st.button("Analyze Meeting"):

            prompt = f"""
            Analyze these meeting notes.

            Provide:
            1. Summary
            2. Key Decisions
            3. Action Items
            4. Deadlines

            Meeting Notes:
            {notes}
            """

            response = llm.invoke(prompt)

            st.write(response.content)

    elif option == "Email Generator":

        instruction = st.text_area(
            "Describe the email you want to write"
        )

        if st.button("Generate Email"):

            prompt = f"""
            Write a professional business email based on:

            {instruction}

            Include subject, greeting, message and closing.
            """

            response = llm.invoke(prompt)

            st.write(response.content)

else:

    st.info("Enter your Gemini API key from the sidebar to start.")
