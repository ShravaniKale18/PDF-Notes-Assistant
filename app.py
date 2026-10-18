import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from rag_pipeline import build_rag_chain

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

rag_chain = None
uploaded_pdfs = []


def is_allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def home():
    global rag_chain, uploaded_pdfs

    answer = ""
    question = ""
    message = ""

    if request.method == "POST":
        action = request.form.get("action")

        # Upload and process PDFs
        if action == "upload":
            files = request.files.getlist("pdfs")

            valid_files = [
                file for file in files
                if file.filename and is_allowed_file(file.filename)
            ]

            if not valid_files:
                message = "Please select at least one PDF file."
            else:
                try:
                    paths = []

                    for file in valid_files:
                        filename = secure_filename(file.filename)

                        if not filename:
                            continue

                        path = os.path.join(UPLOAD_FOLDER, filename)
                        file.save(path)
                        paths.append(path)

                    if not paths:
                        raise ValueError("No valid PDF files were saved.")

                    rag_chain = build_rag_chain(paths)
                    uploaded_pdfs = paths

                    message = "PDFs processed successfully! You can now ask questions."

                except Exception:
                    app.logger.exception("PDF processing failed")
                    rag_chain = None
                    uploaded_pdfs = []
                    message = "Could not process PDFs. Check the terminal for details."

        # Ask questions about uploaded PDFs
        elif action == "ask":
            question = request.form.get("question", "").strip()

            if rag_chain is None:
                message = "Please upload your PDFs first."
            elif not question:
                message = "Please enter a question."
            else:
                try:
                    result = rag_chain.invoke({"question": question})

                    if isinstance(result, dict):
                        answer = result.get("answer", str(result))
                    else:
                        answer = str(result)

                except Exception:
                    app.logger.exception("Question answering failed")
                    message = "Unable to generate an answer. Check the terminal."

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        message=message,
        uploaded_pdfs=uploaded_pdfs
    )


if __name__ == "__main__":
    app.run(debug=True)
