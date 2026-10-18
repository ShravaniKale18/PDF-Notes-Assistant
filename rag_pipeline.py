
# rag_pipeline.py

import os
from operator import itemgetter

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def load_pdf(pdf_paths):
    all_pages = []

    for pdf_path in pdf_paths:
        print(f"Loading: {pdf_path}")

        pages = PyPDFLoader(pdf_path).load()

        for page in pages:
            page.metadata["source"] = os.path.basename(pdf_path)

        all_pages.extend(pages)

    if not all_pages:
        raise ValueError("No readable PDF pages found.")

    return all_pages


def chunk_documents(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = splitter.split_documents(pages)

    if not chunks:
        raise ValueError("No text chunks were created.")

    print("Total chunks:", len(chunks))
    return chunks


def create_vector_store(chunks):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # In-memory vector store for this uploaded document set.
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    return vector_store


def setup_rag_chain(vector_store):
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6}
    )

    system_prompt = """

        You are a PDF-based exam preparation assistant.

        Answer the user's request using only the retrieved PDF context provided below.

        SOURCE ACCURACY:
        - Identify topics only when they explicitly appear in the retrieved context.
        - Never assume that a topic exists in the PDF based on general knowledge or the title of the unit.
        - Do not invent topic names, advantages, challenges, questions, examples, or page numbers.
        - If the user requests important questions, generate questions based on specific facts and concepts actually present in the context.
        - Do not create generic questions such as "What are the advantages?" unless the retrieved context contains the relevant advantages.
        - If the retrieved context does not cover the entire requested unit, clearly state that the results cover only the available excerpts.
        - If there is insufficient relevant information, say so rather than guessing.

        OUTPUT FORMAT:
        - Use valid Markdown, not escaped Markdown.
        - Use headings beginning with ### followed by a space.
        - Never prefix headings with a backslash.
        - Use numbered lists for exam questions.
        - Put each question on a separate line or paragraph.
        - Do not use HTML tags or tables.
        - Do not include explanations, hints, answers, or answer-type labels unless requested.
        - Do not add topics that are not supported by the context.
        - Keep the response concise and revision-friendly.
        - each new point or questiono or any information should be separated in a new line
        Retrieved PDF context:
        {context}
    """

    rag_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])

    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    llm = ChatGroq(
        api_key=api_key,
        model="openai/gpt-oss-120b",
        temperature=0.2
    )

    def format_docs(docs):
        formatted = []

        for doc in docs:
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page")

            if isinstance(page, int):
                page += 1
            else:
                page = "Unknown"

            formatted.append(
                f"Source: {source}, Page: {page}\n"
                f"{doc.page_content}"
            )

        return "\n\n".join(formatted)

    chain = (
        {
            "context": itemgetter("question")
                       | retriever
                       | format_docs,
            "question": itemgetter("question")
        }
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return chain


def build_rag_chain(pdf_paths):

    """Called by Flask after the user uploads PDFs."""
    
    pages = load_pdf(pdf_paths)
    chunks = chunk_documents(pages)
    vector_store = create_vector_store(chunks)

    return setup_rag_chain(vector_store)
