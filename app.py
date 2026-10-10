
from flask import Flask, render_template, request
import pdfplumber
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    details = None
    error = None

    if request.method == "POST":
        file = request.files.get("resume")

        if not file or not file.filename.lower().endswith(".pdf"):
            error = "Please upload a PDF resume."
        else:
            try:
                with pdfplumber.open(file) as pdf:
                    text = "\n".join(
                        page.extract_text() or ""
                        for page in pdf.pages
                    )

                email = re.search(
                    r"[\w.+-]+@[\w.-]+\.\w+", text
                )

                details = {
                    "email": email.group(0) if email else "Not found",
                    "text": text
                }

            except Exception:
                error = "Could not read this PDF. Please try another."

    return render_template(
        "index.html", details=details, error=error
    )

if __name__ == "__main__":
    app.run(debug=True)