"""
Quick test to verify feedback integration is working.
"""
import requests

BASE_URL = "http://localhost:5000"

print("Testing community feedback integration...")
print("=" * 60)

# Test 1: Generate path
print("\n1. Generating learning path...")
response = requests.post(f"{BASE_URL}/api/path", json={
    "goal": "Data Scientist",
    "current_skills": []
})

if response.status_code == 200:
    data = response.json()
    path = data.get('learning_path', [])
    print(f"✅ Success! Generated {len(path)} sessions")
    
    if path:
        # Show first few skills
        print(f"\nFirst session skills:")
        first_session = path[0]
        skills = first_session.get('skills', [])[:5]
        for skill in skills:
            skill_name = skill if isinstance(skill, str) else skill.get('label', 'Unknown')
            print(f"  • {skill_name}")
else:
    print(f"❌ Error {response.status_code}: {response.text}")

print("\n" + "=" * 60)
print("\n⚠️  IMPORTANT: Restart the server to apply code changes!")
print("   1. Stop the current server (Ctrl+C in the terminal)")
print("   2. Run: python app.py")
print("   3. Then run: python demo_feedback_integration.py")
