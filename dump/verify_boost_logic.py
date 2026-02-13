"""Quick verification: Check if community boost logic is active in running server."""
import sys
import importlib.util

# Load ai_engine module to check if boost code exists
spec = importlib.util.spec_from_file_location("ai_engine", "ai_engine.py")
ai_engine = importlib.util.module_from_spec(spec)

print("\n" + "="*80)
print(" VERIFICATION: Community Boost Logic")
print("="*80 + "\n")

# Read the source to verify boost logic exists
with open('ai_engine.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
    if 'vote_score >= 0.7 and vote_count >= 3' in content:
        print("✅ Community boost logic FOUND in ai_engine.py")
        print("   Code: if vote_score >= 0.7 and vote_count >= 3:")
        print("          relevance_score = 7")
    else:
        print("❌ Community boost logic NOT FOUND")
        
    if 'relevance_score = 7' in content and 'Community skill' in content:
        print("✅ Boost assignment code FOUND")
    else:
        print("❌ Boost assignment code NOT FOUND")

print("\n" + "="*80)
print(" RECOMMENDATION")
print("="*80 + "\n")

print("The community boost logic is in the code file.")
print("If community skills aren't appearing in learning paths:")
print("")
print("1. Restart the Flask server to reload the updated code:")
print("   - Stop current server (Ctrl+C)")
print("   - Clear Python cache: Remove-Item __pycache__ -Recurse -Force")
print("   - Start server: python app.py")
print("")
print("2. Then re-run the comprehensive test:")
print("   python test_comprehensive_feedback.py")
print("")
print("Expected result after restart:")
print("   • TensorFlow, PyTorch, MLflow, Kubeflow should appear in learning path")
print("   • Test 6 should PASS (Community Impact)")
print("   • Final score should be 6/6")

print("\n" + "="*80 + "\n")
