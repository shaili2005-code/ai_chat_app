import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# List models and their capabilities
models = genai.list_models()
print("\n🔍 Available Models & What They Support:\n")
for model in models:
    name = model.name
    generation_supported = 'generateContent' in model.supported_generation_methods
    print(f"📌 {name} — supports generate_content(): {generation_supported}")
