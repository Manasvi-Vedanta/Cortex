import google.generativeai as genai

# Configure API
api_key = "AIzaSyDRf_5b1YQxEyr80pnq9pI8NmT_ZWuNKjs"
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
