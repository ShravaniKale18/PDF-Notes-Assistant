# 📚 PDF Notes Assistant

<!-- A Flask-based Retrieval-Augmented Generation (RAG) application for studying PDF documents. -->

[![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-green)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/LLM-Groq-orange)](https://groq.com/)

A **PDF Notes Assistant** that helps students study smarter by uploading PDF documents and asking questions about their content. It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate context-based answers.

<!-- Replace this section with a screenshot of your application when available. -->

---

## ✨ Features

- 📄 **PDF Upload:** Upload PDF documents through a simple web interface.
- 🔍 **Document Processing:** Extract text from PDFs and split it into smaller chunks.
- 🧠 **Semantic Search:** Generate embeddings and retrieve relevant document content.
- 🤖 **AI-Powered Answers:** Ask questions about your uploaded PDFs using a Groq-hosted language model.
- 📚 **Study Assistance:** Use your documents to review concepts and prepare for exams.
- 🌐 **Flask Web Interface:** Interact with the application through your browser.
- 🧩 **RAG Architecture:** Combine document retrieval with language-model responses.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web application framework |
| LangChain | RAG pipeline and component integration |
| PyPDF | PDF text extraction |
| Hugging Face Embeddings | Convert text into vector representations |
| ChromaDB | Vector storage and similarity search |
| Groq | Language model inference |
| HTML and CSS | Frontend interface |

## 🏗️ How It Works

<!-- High-level workflow of the PDF question-answering system. -->

```text
          Upload PDF Documents
                   |
                   v
             Extract Text
                   |
                   v
             Split into Chunks
                   |
                   v
          Generate Embeddings
                   |
                   v
            Store in ChromaDB
                   |
                   v
             Ask a Question
                   |
                   v
          Retrieve Relevant Chunks
                   |
                   v
          Send Context to the LLM
                   |
                   v
             Generate Answer
```

## 📂 Project Structure

```text
PDF-Notes-Assistant/
│
├── app.py                 # Flask application and routes
├── rag_pipeline.py        # PDF processing and RAG pipeline
├── requirements.txt       # Python dependencies
├── .env                   # API key configuration (not committed)
├── .gitignore             # Files excluded from Git
│
├── templates/
│   └── index.html         # Main HTML page
│
├── static/
│   └── style.css          # Application styling
│
└── uploads/               # Uploaded PDF documents (not committed)
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ShravaniKale18/PDF-Notes-Assistant.git
cd PDF-Notes-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it according to your operating system.

**Linux / macOS**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If installation fails because of disk space or PyTorch dependency issues, check your available disk space and install compatible CPU-only dependencies where appropriate.

### 4. Configure the API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get an API key from the [Groq Console](https://console.groq.com/).

<!-- SECURITY: Never commit your real API key or upload your .env file to GitHub. -->

Make sure `.env` is listed in `.gitignore`.

If your application does not load environment variables automatically, configure them in your Python application using `python-dotenv` or export the variable in your terminal.

### 5. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## 🚀 How to Use

1. Start the Flask application.
2. Open the local URL in your browser.
3. Upload one or more PDF documents.
4. Wait for the documents to be processed.
5. Enter a question about the uploaded content.
6. Read the generated answer.

**Example questions:**

- What are the main topics covered in this document?
- Explain a concept discussed in the PDF.
- Generate important exam questions from the available content.
- Summarize the key points from a topic.

<!-- Answers depend on the content retrieved from the uploaded PDFs. -->

## 🔐 Security Notes

- Never commit `.env` or expose API keys in source code.
- Keep uploaded documents and generated local data out of version control unless they are intentionally meant to be public.
- Do not commit virtual environments, Python cache files, or other unnecessary generated files.
- Rotate any API key that has accidentally been exposed.

## 🔮 Future Improvements

<!-- Update this list as new features are implemented. -->

- [ ] Display uploaded document names in the interface.
- [ ] Add PDF deletion and document management.
- [ ] Display source document names and page references with answers.
- [ ] Improve retrieval coverage for questions about entire chapters.
- [ ] Add chat history and follow-up questions.
- [ ] Improve error handling and user feedback.
- [ ] Deploy the application online.
- [ ] Add automated tests.

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

## 👩‍💻 Author

**Shravani Kale**

GitHub: [@ShravaniKale18](https://github.com/ShravaniKale18)

## 📄 License

<!-- Add a LICENSE file before selecting or claiming a project license. -->

No license has been specified yet. Add a `LICENSE` file if you want to define how others may use, modify, and distribute this project.

---

⭐ If you find this project useful, consider giving the repository a star!
