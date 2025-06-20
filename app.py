from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # << Add this line

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

def load_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

pdf_text = load_pdf_text("documents/intro to machine learning.pdf")

@app.route("/")
def index():
    return render_template("index.html")

def answer_question(query):
    prompt = f"""Use the following PDF content to answer the question:

{pdf_text}

Question: {query}
Answer:"""
    try:
        response = model.generate_content(prompt)
        print("Gemini response:", response)  # Debug print
        return response.text
    except Exception as e:
        print("Error calling Gemini API:", e)
        raise


@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()
    print("Received data:", data)  # Debug print
    question = data.get("question") if data else None
    if not question:
        print("No question provided!")
        return jsonify({"error": "Question is required"}), 400
    try:
        answer = answer_question(question)
        print("Answer generated:", answer)  # Debug print
        return jsonify({"answer": answer})
    except Exception as e:
        print("Error during answer generation:", e)  # Debug print
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
