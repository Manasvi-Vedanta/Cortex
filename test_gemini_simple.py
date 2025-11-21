"""Quick test to verify Gemini API works"""
import google.generativeai as genai
import os

# Configure API
api_key = os.getenv('GOOGLE_API_KEY', '')
genai.configure(api_key=api_key)

# Test with gemini-2.0-flash model
model = genai.GenerativeModel('gemini-2.0-flash')

skills = "Python, JavaScript, SQL, HTML, CSS"

prompt = f"""Create learning sessions for: {skills}

Output JSON format:
{{"sessions":[{{"session_number":1,"title":"title","objectives":["obj1"],"skills":["skill1"],"estimated_duration_hours":8,"difficulty_level":"beginner","prerequisites":[]}}]}}"""

print("Testing Gemini API...")
print(f"Prompt: {prompt[:100]}...")

try:
    response = model.generate_content(
        prompt,
        generation_config={
            'temperature': 0.2,
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 2048
        },
        safety_settings=[
            {'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
            {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
            {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
            {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'}
        ]
    )
    
    print(f"\n✅ Success! Response length: {len(response.text)} chars")
    print(f"Response preview: {response.text[:200]}...")
    
    if hasattr(response, 'candidates'):
        print(f"Finish reason: {response.candidates[0].finish_reason}")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    if hasattr(response, 'candidates'):
        print(f"Finish reason: {response.candidates[0].finish_reason}")
        print(f"Safety ratings: {response.candidates[0].safety_ratings}")
