# 🤖 OpsCopilot

### AI Operations Copilot for Documents, Meetings and Business Communication

OpsCopilot is a Generative AI-powered productivity application designed to help users perform common business tasks using natural language.

It combines Large Language Models, Retrieval-Augmented Generation (RAG), document processing, embeddings, vector search and AI workflows into one simple workspace.

🔗 **Live Application:** [https://opscopilot-ai.streamlit.app]

---

## 🎯 Problem

Employees and teams regularly work with:

- Large PDF documents
- Meeting notes
- Business communication
- Professional emails

Manually reading documents, extracting important information from meetings and writing professional emails can consume significant time.

OpsCopilot provides a single AI workspace to simplify these everyday tasks.

---

## 💡 Solution

OpsCopilot provides three AI-powered productivity tools:

### 📄 1. Document Intelligence

Users can:

- Upload a PDF document
- Extract text from the document
- Split the text into smaller meaningful chunks
- Convert text into vector embeddings
- Store embeddings using FAISS
- Ask questions about the document
- Retrieve relevant information using RAG
- Generate answers using an LLM
- View retrieved source content

This helps users understand and search lengthy documents more efficiently.

---

### 📝 2. Meeting Intelligence

Users can paste meeting notes and generate:

- Meeting summary
- Key decisions
- Action items
- Deadlines

This converts unstructured meeting notes into structured and actionable information.

---

### ✉️ 3. Email Generator

Users can generate professional emails by providing:

- The purpose of the email
- The required tone

The application generates structured professional communication with:

- Subject
- Greeting
- Email body
- Professional closing

---

# 🏗️ System Architecture

```text
                    ┌────────────────────┐
                    │       User         │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │    Streamlit UI    │
                    └─────────┬──────────┘
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
       Document Q&A     Meeting Analysis   Email Generation
              │               │                │
              ▼               ▼                ▼
        PDF Processing       Prompt          Prompt
              │               │                │
              ▼               └────────┬───────┘
        Text Chunking                   │
              │                         ▼
              ▼                  Gemini LLM
        HuggingFace Embeddings         │
              │                         │
              ▼                         ▼
           FAISS                 AI Response
              │
              ▼
        Relevant Context
              │
              ▼
          Gemini LLM
              │
              ▼
          Final Answer
````

---

# 🔄 Document RAG Workflow

```text
PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
HuggingFace Embeddings
    ↓
FAISS Vector Database
    ↓
User Question
    ↓
Relevant Chunk Retrieval
    ↓
Context + Question
    ↓
Gemini 2.5 Flash
    ↓
Grounded Answer
```

The Document Intelligence module uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents before generating an answer.

This helps the AI answer questions using the content of the uploaded document rather than relying only on general model knowledge.

---

# 🛠️ Technology Stack

## Programming Language

* Python

## Frontend and Application Framework

* Streamlit

## Generative AI Model

* Google Gemini 2.5 Flash

## LLM Application Framework

* LangChain

## PDF Processing

* PyMuPDF

## Text Processing

* Recursive Character Text Splitter

## Embeddings

* HuggingFace Sentence Transformers

## Vector Database

* FAISS

## Development Environment

* Google Colab

## Version Control

* GitHub

## Deployment

* Streamlit Cloud

---

# 🔐 Security

The application uses Streamlit Secrets to protect sensitive credentials.

API keys and login credentials are not hardcoded in the public source code.

The following sensitive information is securely managed:

* Google Gemini API key
* Admin credentials
* Demo credentials
* User credentials

This helps prevent sensitive information from being exposed in the GitHub repository.

---

# 📁 Project Structure

```text
OpsCopilot/
│
├── app.py
├── requirements.txt
└── README.md
```

---

# 🚀 How to Run the Application

## 1. Clone the Repository

```bash
git clone [https://github.com/DEEPANSHI19892/OpsCopilot]
```

Navigate to the project directory:

```bash
cd OpsCopilot
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Streamlit Secrets

Create a Streamlit secrets configuration with the required credentials:

```toml
GOOGLE_API_KEY = "your_google_api_key"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "your_admin_password"

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "your_demo_password"

USER_USERNAME = "user"
USER_PASSWORD = "your_user_password"
```

---

## 4. Run the Application

```bash
streamlit run app.py
```

The application will start locally in your browser.

---

# 📊 Key Features

| Feature                     | Technology               |
| --------------------------- | ------------------------ |
| PDF Text Extraction         | PyMuPDF                  |
| Text Chunking               | LangChain                |
| Semantic Embeddings         | HuggingFace              |
| Vector Search               | FAISS                    |
| Document Question Answering | RAG                      |
| LLM Response Generation     | Gemini 2.5 Flash         |
| Meeting Analysis            | Prompt Engineering + LLM |
| Email Generation            | Prompt Engineering + LLM |
| User Authentication         | Streamlit Session State  |
| Secret Management           | Streamlit Secrets        |
| Deployment                  | Streamlit Cloud          |

---

# 🧠 How the Application Works

## Document Intelligence

```text
User uploads PDF
        ↓
Text is extracted
        ↓
Text is divided into chunks
        ↓
Chunks are converted into embeddings
        ↓
Embeddings are stored in FAISS
        ↓
User asks a question
        ↓
Relevant chunks are retrieved
        ↓
Retrieved context is sent to Gemini
        ↓
AI generates a relevant answer
```

---

## Meeting Intelligence

```text
Meeting Notes
      ↓
User Input
      ↓
Prompt Engineering
      ↓
Gemini 2.5 Flash
      ↓
Structured Output
      ↓
Summary + Decisions + Action Items + Deadlines
```

---

## Email Generator

```text
User Instruction
      ↓
Select Email Tone
      ↓
Prompt Construction
      ↓
Gemini 2.5 Flash
      ↓
Professional Email
```

---

# 🎓 Internship Learning Demonstrated

This project demonstrates practical knowledge of:

* Generative AI
* Large Language Models
* LLM API Integration
* Prompt Engineering
* Machine Learning Fundamentals
* Deep Learning Fundamentals
* Artificial Neural Networks
* Transformers
* Text Mining
* Model Fine-Tuning Concepts
* LangChain
* Retrieval-Augmented Generation
* Vector Embeddings
* Vector Databases
* AI Application Development

---

# 📈 Future Improvements

Possible future improvements include:

* Multi-document RAG
* Conversation memory
* User-specific workspaces
* Persistent database storage
* Advanced authentication
* Role-based access control
* Support for additional document formats
* Document comparison
* Improved source citations
* Enterprise deployment

---

# 🧪 Development Environment

Google Colab was used during the development and experimentation phase for:

* Testing AI and LLM concepts
* Experimenting with LangChain
* Testing RAG components
* Testing embeddings and vector search
* Developing and testing application functionality

The final application is connected to GitHub and deployed using Streamlit Cloud.

---

# 🌐 Deployment

The application is deployed using:

```text
GitHub
    ↓
Streamlit Cloud
    ↓
Live OpsCopilot Application
```

🔗 **Live Application:** [https://opscopilot-ai.streamlit.app/#ai-operations-copilot]

---

# 📌 Project Highlights

* Built a complete Generative AI application
* Implemented a working RAG pipeline
* Used semantic embeddings for document search
* Implemented FAISS vector similarity search
* Integrated Google Gemini LLM
* Built multiple AI productivity tools
* Added login-based access
* Used secure secret management
* Deployed the application online
* Created a practical AI workspace for everyday business tasks

---

# 👨‍💻 Project Information

### Project Name

**OpsCopilot**

### Project Type

Generative AI Productivity Application

### Developed During

Generative AI Internship

### Primary Focus

AI-powered document intelligence and workplace productivity

---
