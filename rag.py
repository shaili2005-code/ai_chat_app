import os
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# ✅ Use a working Gemini model for generate_content
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

# Load PDF content
def load_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

pdf_text = load_pdf_text("documents/intro to machine learning.pdf")

# Ask Gemini
def answer_question(query):
    prompt = f"""Use the following PDF content to answer the question:

{pdf_text}

Question: {query}
Answer:"""
    response = model.generate_content(prompt)
    return response.text

# Main loop
if __name__ == "__main__":
    while True:
        query = input("\n❓ Ask something from the PDF (or type 'exit' to quit): ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting the chat.")
            break
        try:
            answer = answer_question(query)
            print(f"🤖 Answer: {answer}")
        except Exception as e:
            print(f"⚠️ Error: {e}")
