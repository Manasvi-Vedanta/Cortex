import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in .env file.")
genai.configure(api_key=api_key)

print("Fetching available models...")
print("=" * 80)

# List all available models
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"\nModel: {model.name}")
        print(f"Display Name: {model.display_name}")
        print(f"Description: {model.description}")
        print(f"Input Token Limit: {model.input_token_limit}")
        print(f"Output Token Limit: {model.output_token_limit}")
        print("-" * 80)
