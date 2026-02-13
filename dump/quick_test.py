"""Quick test to validate the enhanced test suite fixes."""

from enhanced_test_suite import EnhancedTestSuite

def main():
    print("\nQuick Test - Running 2 test cases to validate fixes\n")
    
    test_suite = EnhancedTestSuite()
    
    # Get only first 2 test cases
    all_cases = test_suite.get_diverse_test_cases()
    test_cases = all_cases[:2]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*100}")
        print(f" TEST {i}/2: {test_case['name']}")
        print(f"{'='*100}")
        
        result = test_suite.run_comprehensive_test(test_case)
        results.append(result)
        
        # Check if relevance scores and resources worked
        if 'relevance_scores' in result and len(result['relevance_scores']) > 0:
            print(f"\nRelevance scoring PASSED - {len(result['relevance_scores'])} skills scored")
        else:
            print(f"\nRelevance scoring FAILED")
            
        if 'resource_curation' in result and result['resource_curation']['skills_checked'] > 0:
            print(f"Resource curation PASSED - {result['resource_curation']['total_resources']} resources found")
        else:
            print(f"Resource curation FAILED")
        
        print(f"\n{'─'*100}\n")
    
    print(f"\n{'='*100}")
    print(" QUICK TEST COMPLETE")
    print(f"{'='*100}")
    
    # Check if both tests worked
    success_count = sum(1 for r in results if 'relevance_scores' in r and 'resource_curation' in r)
    print(f"\nTests completed: {success_count}/2 successful")
    
    if success_count == 2:
        print("\nALL FIXES VALIDATED! Ready to run full test suite.")
    else:
        print("\nSome tests failed. Review error messages above.")

if __name__ == "__main__":
    main()
