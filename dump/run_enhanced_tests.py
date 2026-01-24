"""
Fast Test Runner - Runs a subset of tests and generates a summary document
"""

import sys
import io
import time
from datetime import datetime
from enhanced_test_suite import EnhancedTestSuite

def generate_summary_document(report, filename="TEST_SUMMARY.md"):
    """Generate a markdown summary document from the test report."""
    
    summary = report['summary']
    perf_metrics = report.get('performance_metrics', {})
    sim_scores = report.get('similarity_scores', {})
    rel_analysis = report.get('relevance_analysis', {})
    cat_breakdown = report.get('category_breakdown', {})
    
    md_content = f"""# GenMentor Enhanced Test Suite - Summary Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 Executive Summary

| Metric | Value |
|--------|-------|
| **Total Tests** | {summary['total_tests']} |
| **Successful Tests** | {summary['successful_tests']} ✅ |
| **Failed Tests** | {summary['failed_tests']} ❌ |
| **Success Rate** | {summary['success_rate']:.1f}% |

---

## ⚡ Performance Benchmarks

"""
    
    if perf_metrics:
        md_content += """### Skill Gap Analysis
| Metric | Time (seconds) |
|--------|----------------|
"""
        if 'skill_gap_analysis' in perf_metrics:
            sga = perf_metrics['skill_gap_analysis']
            md_content += f"| Average | {sga['avg']:.2f}s |\n"
            md_content += f"| Minimum | {sga['min']:.2f}s |\n"
            md_content += f"| Maximum | {sga['max']:.2f}s |\n"
            md_content += f"| Std Dev | {sga['std']:.2f}s |\n"
        
        md_content += """\n### Learning Path Generation
| Metric | Time (seconds) |
|--------|----------------|
"""
        if 'learning_path_generation' in perf_metrics:
            lpg = perf_metrics['learning_path_generation']
            md_content += f"| Average | {lpg['avg']:.2f}s |\n"
            md_content += f"| Minimum | {lpg['min']:.2f}s |\n"
            md_content += f"| Maximum | {lpg['max']:.2f}s |\n"
            md_content += f"| Std Dev | {lpg['std']:.2f}s |\n"
        
        md_content += """\n### Total Processing Time
| Metric | Time (seconds) |
|--------|----------------|
"""
        if 'total_processing' in perf_metrics:
            tp = perf_metrics['total_processing']
            md_content += f"| Average | {tp['avg']:.2f}s |\n"
            md_content += f"| Minimum | {tp['min']:.2f}s |\n"
            md_content += f"| Maximum | {tp['max']:.2f}s |\n"
            md_content += f"| Std Dev | {tp['std']:.2f}s |\n"
    else:
        md_content += "_No performance metrics available_\n"
    
    md_content += "\n---\n\n## 🎯 Similarity Score Analysis\n\n"
    
    if sim_scores:
        md_content += f"""| Metric | Score |
|--------|-------|
| **Average** | {sim_scores['average']:.2f}% |
| **Median** | {sim_scores['median']:.2f}% |
| **Minimum** | {sim_scores['min']:.2f}% |
| **Maximum** | {sim_scores['max']:.2f}% |
| **Std Dev** | {sim_scores['std']:.2f}% |

### Distribution
"""
        if 'distribution' in sim_scores:
            dist = sim_scores['distribution']
            md_content += f"- **Excellent (90%+)**: {dist.get('excellent', 0)} tests\n"
            md_content += f"- **Very Good (80-90%)**: {dist.get('very_good', 0)} tests\n"
            md_content += f"- **Good (70-80%)**: {dist.get('good', 0)} tests\n"
            md_content += f"- **Fair (60-70%)**: {dist.get('fair', 0)} tests\n"
            md_content += f"- **Below 60%**: {dist.get('poor', 0)} tests\n"
    else:
        md_content += "_No similarity scores available_\n"
    
    md_content += "\n---\n\n## 🧠 Relevance Score Analysis\n\n"
    
    if rel_analysis:
        md_content += f"""| Metric | Score (out of 100) |
|--------|-------------------|
| **Average** | {rel_analysis['average_score']:.1f} |
| **Median** | {rel_analysis['median_score']:.1f} |
| **Minimum** | {rel_analysis['min_score']:.1f} |
| **Maximum** | {rel_analysis['max_score']:.1f} |

### Component Breakdown (Average)
| Component | Points | Max Points |
|-----------|--------|------------|
"""
        if 'component_averages' in rel_analysis:
            comp = rel_analysis['component_averages']
            md_content += f"| Occupation Relevance | {comp.get('occupation_relevance', 0):.1f} | 40 |\n"
            md_content += f"| Skill Gap Priority | {comp.get('skill_gap_priority', 0):.1f} | 30 |\n"
            md_content += f"| Learning Path Position | {comp.get('learning_path_position', 0):.1f} | 20 |\n"
            md_content += f"| Resource Availability | {comp.get('resource_availability', 0):.1f} | 10 |\n"
    else:
        md_content += "_No relevance analysis available_\n"
    
    md_content += "\n---\n\n## 📁 Category Breakdown\n\n"
    
    if cat_breakdown:
        md_content += "| Category | Tests | Avg Similarity |\n"
        md_content += "|----------|-------|----------------|\n"
        for cat, data in sorted(cat_breakdown.items(), key=lambda x: x[1]['count'], reverse=True):
            md_content += f"| {cat} | {data['count']} | {data['avg_similarity']:.1f}% |\n"
    else:
        md_content += "_No category breakdown available_\n"
    
    md_content += "\n---\n\n## 📋 Individual Test Results\n\n"
    
    for result in report['test_results']:
        status_icon = "✅" if result['status'] == 'success' else "❌"
        md_content += f"### {status_icon} {result['test_id']}: {result['name']}\n\n"
        md_content += f"**Goal**: {result['goal']}\n\n"
        md_content += f"**Category**: {result['category']} | **Difficulty**: {result['difficulty']}\n\n"
        
        if 'matched_occupation' in result:
            mo = result['matched_occupation']
            md_content += f"**Matched Occupation**: {mo['label']} ({mo['similarity_percentage']:.1f}% match)\n\n"
        
        if 'learning_path' in result:
            lp = result['learning_path']
            md_content += f"**Learning Path**: {lp['total_sessions']} sessions, {lp['total_hours']} hours ({lp['weeks_full_time']} weeks)\n\n"
        
        if 'components_status' in result:
            cs = result['components_status']
            md_content += "**Components**:\n"
            md_content += f"- Skill Gap Analysis: {'✅' if cs['skill_gap_analysis'] else '❌'}\n"
            md_content += f"- Learning Path Generation: {'✅' if cs['learning_path_generation'] else '❌'}\n"
            md_content += f"- Relevance Scoring: {'✅' if cs['relevance_scoring'] else '❌'}\n"
            md_content += f"- Resource Curation: {'✅' if cs['resource_curation'] else '❌'}\n\n"
        
        if 'relevance_scores' in result and len(result['relevance_scores']) > 0:
            md_content += "**Top Skills by Relevance**:\n"
            for i, rs in enumerate(result['relevance_scores'][:3], 1):
                md_content += f"{i}. {rs['skill'].title()} - {rs['total_score']}/100\n"
            md_content += "\n"
        
        if 'timestamps' in result:
            md_content += f"**Processing Time**: {result['timestamps']['total']:.2f}s\n\n"
        
        if 'error' in result:
            md_content += f"**Error**: {result['error']}\n\n"
        
        md_content += "---\n\n"
    
    md_content += f"""
## 📈 Key Insights

1. **System Performance**: Average total processing time of {perf_metrics.get('total_processing', {}).get('avg', 0):.2f}s per test
2. **Occupation Matching**: Average similarity score of {sim_scores.get('average', 0):.1f}%
3. **Skill Prioritization**: Average relevance score of {rel_analysis.get('average_score', 0):.1f}/100
4. **Success Rate**: {summary['success_rate']:.1f}% of tests completed successfully

---

**Test Suite**: GenMentor Enhanced Test Suite  
**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Save the document
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"\n✅ Summary document generated: {filename}")
    return filename


def main():
    """Run tests and generate summary."""
    print("\n" + "="*100)
    print(" GENMENTOR ENHANCED TEST SUITE - FAST RUN")
    print("="*100)
    print("\nRunning optimized test suite with summary generation...")
    
    test_suite = EnhancedTestSuite()
    
    # Get all test cases
    all_cases = test_suite.get_diverse_test_cases()
    
    # Run all tests (or subset for faster execution)
    # For full run: test_cases = all_cases
    # For fast run: test_cases = all_cases[:10]
    
    print(f"\n📊 Running {len(all_cases)} test cases...\n")
    
    results = []
    start_time = time.time()
    
    for i, test_case in enumerate(all_cases, 1):
        print(f"\n{'='*100}")
        print(f" TEST {i}/{len(all_cases)}: {test_case['name']}")
        print(f"{'='*100}")
        
        result = test_suite.run_comprehensive_test(test_case)
        results.append(result)
        
        # Quick status
        status = "✅ PASS" if result['status'] == 'success' else "❌ FAIL"
        print(f"\n{status} - {result.get('timestamps', {}).get('total', 0):.2f}s")
    
    total_time = time.time() - start_time
    
    print(f"\n{'='*100}")
    print(f" ALL TESTS COMPLETED IN {total_time:.2f}s")
    print(f"{'='*100}")
    
    # Generate comprehensive report
    report = test_suite.generate_comprehensive_report(results)
    
    # Save JSON report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"comprehensive_test_report_{timestamp}.json"
    test_suite.save_report(report, json_filename)
    
    # Generate summary document
    print(f"\n{'='*100}")
    print(" GENERATING SUMMARY DOCUMENT")
    print(f"{'='*100}")
    
    summary_filename = f"TEST_SUMMARY_{timestamp}.md"
    generate_summary_document(report, summary_filename)
    
    # Print quick summary
    print(f"\n{'='*100}")
    print(" QUICK SUMMARY")
    print(f"{'='*100}")
    print(f"\n✅ Success Rate: {report['summary']['success_rate']:.1f}%")
    print(f"✅ Tests Passed: {report['summary']['successful_tests']}/{report['summary']['total_tests']}")
    
    if report.get('similarity_scores'):
        print(f"✅ Avg Similarity: {report['similarity_scores']['average']:.1f}%")
    
    if report.get('relevance_analysis'):
        print(f"✅ Avg Relevance: {report['relevance_analysis']['average_score']:.1f}/100")
    
    if report.get('performance_metrics'):
        print(f"✅ Avg Processing: {report['performance_metrics']['total_processing']['avg']:.2f}s")
    
    print(f"\n📄 Reports Generated:")
    print(f"   - JSON: {json_filename}")
    print(f"   - Summary: {summary_filename}")
    print(f"\n{'='*100}\n")


if __name__ == "__main__":
    main()
