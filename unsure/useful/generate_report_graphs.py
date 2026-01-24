"""
Generate Visualizations for Final Report
Creates graphs and charts for inclusion in the project report
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Load data
with open('comprehensive_test_report.json', 'r') as f:
    report = json.load(f)

results = report['functional_results']
benchmarks = report['benchmark_results']

# Extract data
test_ids = [r['test_id'] for r in results]
similarities = [r['similarity_score'] * 100 for r in results]
times = [r['elapsed_time'] for r in results]
skills = [r['total_skills'] for r in results]
statuses = [r['status'] for r in results]

# Figure 1: Similarity Scores Bar Chart
fig1, ax1 = plt.subplots(figsize=(14, 6))
colors = ['#2ecc71' if s >= 80 else '#f39c12' if s >= 70 else '#e74c3c' for s in similarities]
bars = ax1.bar(test_ids, similarities, color=colors, edgecolor='black', linewidth=0.5)
ax1.axhline(y=80, color='#27ae60', linestyle='--', linewidth=2, label='Target (80%)')
ax1.axhline(y=np.mean(similarities), color='#3498db', linestyle='-', linewidth=2, label=f'Average ({np.mean(similarities):.1f}%)')
ax1.set_xlabel('Test Case ID')
ax1.set_ylabel('Similarity Score (%)')
ax1.set_title('Occupation Matching Similarity Scores by Test Case')
ax1.set_ylim(0, 110)
ax1.legend(loc='lower right')
ax1.set_xticklabels(test_ids, rotation=45, ha='right')

# Add value labels on bars
for bar, sim in zip(bars, similarities):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{sim:.0f}%', 
             ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig('report_graph1_similarity_scores.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: report_graph1_similarity_scores.png')

# Figure 2: Processing Time Bar Chart
fig2, ax2 = plt.subplots(figsize=(14, 6))
colors2 = ['#e74c3c' if t > 35 else '#f39c12' if t > 25 else '#2ecc71' for t in times]
bars2 = ax2.bar(test_ids, times, color=colors2, edgecolor='black', linewidth=0.5)
ax2.axhline(y=np.mean(times), color='#3498db', linestyle='-', linewidth=2, label=f'Average ({np.mean(times):.1f}s)')
ax2.set_xlabel('Test Case ID')
ax2.set_ylabel('Processing Time (seconds)')
ax2.set_title('System Processing Time by Test Case')
ax2.legend(loc='upper right')
ax2.set_xticklabels(test_ids, rotation=45, ha='right')

plt.tight_layout()
plt.savefig('report_graph2_processing_time.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: report_graph2_processing_time.png')

# Figure 3: Category Performance Comparison
categories = {}
for r in results:
    cat = r.get('category', 'unknown')
    if cat not in categories:
        categories[cat] = {'sims': [], 'times': [], 'passed': 0, 'total': 0}
    categories[cat]['sims'].append(r['similarity_score'] * 100)
    categories[cat]['times'].append(r['elapsed_time'])
    categories[cat]['total'] += 1
    if r['status'] == 'PASS':
        categories[cat]['passed'] += 1

cat_names = list(categories.keys())
cat_sims = [np.mean(categories[c]['sims']) for c in cat_names]
cat_pass_rates = [categories[c]['passed']/categories[c]['total']*100 for c in cat_names]

fig3, ax3 = plt.subplots(figsize=(12, 6))
x = np.arange(len(cat_names))
width = 0.35

bars1 = ax3.bar(x - width/2, cat_sims, width, label='Avg Similarity (%)', color='#3498db', edgecolor='black')
bars2 = ax3.bar(x + width/2, cat_pass_rates, width, label='Pass Rate (%)', color='#2ecc71', edgecolor='black')

ax3.set_ylabel('Percentage (%)')
ax3.set_title('Performance by Test Category')
ax3.set_xticks(x)
ax3.set_xticklabels([c.replace('_', ' ').title() for c in cat_names], rotation=15, ha='right')
ax3.legend(loc='lower right')
ax3.set_ylim(0, 110)

# Add value labels
for bar in bars1:
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{bar.get_height():.1f}', 
             ha='center', va='bottom', fontsize=9)
for bar in bars2:
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{bar.get_height():.0f}', 
             ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('report_graph3_category_performance.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: report_graph3_category_performance.png')

# Figure 4: Optimization Speedup Comparison
fig4, ax4 = plt.subplots(figsize=(10, 6))
components = ['FAISS\nOccupation Matching', 'Database\nConnection Pool']
speedups = [benchmarks['occupation_matching']['avg_speedup'], benchmarks['database_operations']['speedup']]
colors4 = ['#9b59b6', '#e67e22']

bars4 = ax4.bar(components, speedups, color=colors4, edgecolor='black', linewidth=1)
ax4.axhline(y=1, color='#7f8c8d', linestyle='--', linewidth=1, label='Baseline (1x)')
ax4.set_ylabel('Speedup Factor (x)')
ax4.set_title('Performance Optimization Improvements')
ax4.set_ylim(0, max(speedups) * 1.2)

for bar, spd in zip(bars4, speedups):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{spd:.2f}x', 
             ha='center', va='bottom', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('report_graph4_optimization_speedup.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: report_graph4_optimization_speedup.png')

# Figure 5: Similarity Score Distribution (Pie Chart)
fig5, ax5 = plt.subplots(figsize=(8, 8))
ranges = {
    '90-100% (Excellent)': sum(1 for s in similarities if s >= 90),
    '80-89% (Good)': sum(1 for s in similarities if 80 <= s < 90),
    '70-79% (Acceptable)': sum(1 for s in similarities if 70 <= s < 80),
    '<70% (Low)': sum(1 for s in similarities if s < 70)
}
labels = [f'{k}\n({v} tests)' for k, v in ranges.items() if v > 0]
sizes = [v for v in ranges.values() if v > 0]
colors5 = ['#27ae60', '#2ecc71', '#f39c12', '#e74c3c'][:len(sizes)]
explode = [0.02] * len(sizes)

wedges, texts, autotexts = ax5.pie(sizes, explode=explode, labels=labels, colors=colors5, autopct='%1.1f%%',
                                     shadow=True, startangle=90, textprops={'fontsize': 11})
ax5.set_title('Similarity Score Distribution')
plt.tight_layout()
plt.savefig('report_graph5_similarity_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: report_graph5_similarity_distribution.png')

# Figure 6: Skills vs Time Scatter Plot
fig6, ax6 = plt.subplots(figsize=(10, 6))
scatter_colors = ['#2ecc71' if s == 'PASS' else '#f39c12' for s in statuses]
scatter = ax6.scatter(skills, times, c=scatter_colors, s=100, edgecolors='black', linewidth=0.5, alpha=0.8)

# Add trend line
z = np.polyfit(skills, times, 1)
p = np.poly1d(z)
ax6.plot(sorted(skills), p(sorted(skills)), "r--", alpha=0.8, label=f'Trend (slope={z[0]:.2f})')

ax6.set_xlabel('Number of Skills Identified')
ax6.set_ylabel('Processing Time (seconds)')
ax6.set_title('Correlation: Skills Identified vs Processing Time')

# Create legend
green_patch = mpatches.Patch(color='#2ecc71', label='PASS')
orange_patch = mpatches.Patch(color='#f39c12', label='WARN')
ax6.legend(handles=[green_patch, orange_patch], loc='upper left')

plt.tight_layout()
plt.savefig('report_graph6_skills_vs_time.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: report_graph6_skills_vs_time.png')

# Figure 7: Module Accuracy Summary
fig7, ax7 = plt.subplots(figsize=(10, 6))
modules = ['Occupation\nMatching', 'Skill Gap\nIdentification', 'Semantic\nSimilarity', 'Learning Path\nGeneration', 'Overall\nSystem']
accuracies = [95.0, 100.0, 88.1, 100.0, 95.0]
colors7 = ['#3498db', '#2ecc71', '#9b59b6', '#1abc9c', '#e74c3c']

bars7 = ax7.barh(modules, accuracies, color=colors7, edgecolor='black', linewidth=0.5)
ax7.axvline(x=80, color='#27ae60', linestyle='--', linewidth=2, label='Target (80%)')
ax7.set_xlabel('Accuracy / Success Rate (%)')
ax7.set_title('Module-wise Accuracy Analysis')
ax7.set_xlim(0, 110)
ax7.legend(loc='lower right')

for bar, acc in zip(bars7, accuracies):
    ax7.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{acc:.1f}%', 
             ha='left', va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('report_graph7_module_accuracy.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: report_graph7_module_accuracy.png')

# Figure 8: System Architecture Performance Flow
fig8, ax8 = plt.subplots(figsize=(14, 4))
ax8.set_xlim(0, 100)
ax8.set_ylim(0, 10)
ax8.axis('off')

# Draw pipeline boxes
boxes = [
    (5, 4, 15, 3, 'User Input\n(Goal + Skills)', '#ecf0f1'),
    (22, 4, 15, 3, 'Embedding\n(0.1s)', '#3498db'),
    (39, 4, 15, 3, 'FAISS Match\n(0.01s)', '#9b59b6'),
    (56, 4, 15, 3, 'Skill Gap\n(25.2s)', '#e67e22'),
    (73, 4, 15, 3, 'LLM Session\n(6.6s)', '#1abc9c'),
    (90, 4, 10, 3, 'Output', '#27ae60'),
]

for x, y, w, h, text, color in boxes:
    rect = mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle='round,pad=0.1', 
                                     facecolor=color, edgecolor='black', linewidth=2)
    ax8.add_patch(rect)
    ax8.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold')

# Draw arrows
arrow_style = mpatches.ArrowStyle('->', head_length=0.5, head_width=0.3)
for i in range(len(boxes) - 1):
    x1 = boxes[i][0] + boxes[i][2]/2
    x2 = boxes[i+1][0] - boxes[i+1][2]/2
    ax8.annotate('', xy=(x2, 4), xytext=(x1, 4),
                 arrowprops=dict(arrowstyle='->', color='black', lw=2))

ax8.set_title('System Processing Pipeline with Timing', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('report_graph8_pipeline_timing.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: report_graph8_pipeline_timing.png')

print('\n' + '='*60)
print('All graphs saved successfully!')
print('='*60)
print('\nFiles created:')
print('  1. report_graph1_similarity_scores.png')
print('  2. report_graph2_processing_time.png')
print('  3. report_graph3_category_performance.png')
print('  4. report_graph4_optimization_speedup.png')
print('  5. report_graph5_similarity_distribution.png')
print('  6. report_graph6_skills_vs_time.png')
print('  7. report_graph7_module_accuracy.png')
print('  8. report_graph8_pipeline_timing.png')
