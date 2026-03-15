"""
Learning Resource Coverage Analysis & Graph Generator
Compares resource coverage between Gemini and GPT-5.2 evaluation outputs.
Generates publication-quality graphs matching the existing evaluation graph style.
"""

import json
import os
import glob
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# Configuration
# ============================================================
GEMINI_DIR = 'evaluation_outputs_20260124_102936'
GPT_DIR = 'evaluation_outputs_20260302_120401'

TEST_LABELS = [
    'ML Engineer', 'DevOps Engineer', 'Frontend Dev', 'Backend Dev',
    'Data Scientist', 'Cloud Architect', 'Cybersecurity', 'Full Stack Dev',
    'Android Dev', 'iOS Dev', 'Data Engineer', 'Blockchain Dev',
    'Game Dev', 'AI Researcher', 'SRE', 'DBA',
    'Embedded Dev', 'CV Engineer', 'Tech Lead', 'QA Engineer'
]

CATEGORIES = {
    'ML Engineer': 'AI/ML', 'DevOps Engineer': 'Infrastructure', 'Frontend Dev': 'Web Dev',
    'Backend Dev': 'Web Dev', 'Data Scientist': 'AI/ML', 'Cloud Architect': 'Infrastructure',
    'Cybersecurity': 'Security', 'Full Stack Dev': 'Web Dev', 'Android Dev': 'Mobile',
    'iOS Dev': 'Mobile', 'Data Engineer': 'Data', 'Blockchain Dev': 'Emerging',
    'Game Dev': 'Creative', 'AI Researcher': 'AI/ML', 'SRE': 'Infrastructure',
    'DBA': 'Data', 'Embedded Dev': 'Systems', 'CV Engineer': 'AI/ML',
    'Tech Lead': 'Leadership', 'QA Engineer': 'Quality'
}

# Style matching existing evaluation graphs
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'ggplot')
plt.rcParams.update({
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 14,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False
})

COLORS = {
    'gemini': '#2E86AB',
    'gpt': '#A23B72',
    'success': '#2ECC71',
    'warning': '#F39C12',
    'danger': '#E74C3C',
    'info': '#3498DB',
    'categories': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3A506B', '#5BC0BE', '#6B2737', '#1B998B']
}


# ============================================================
# Data Extraction
# ============================================================
def analyze_resources(base_dir):
    """Extract resource coverage data from evaluation output folder."""
    results = []
    for test_folder in sorted(glob.glob(os.path.join(base_dir, 'test_*'))):
        lp_file = os.path.join(test_folder, '01_learning_path.json')
        if not os.path.exists(lp_file):
            continue
        with open(lp_file) as f:
            data = json.load(f)
        path = data.get('learning_path', [])
        test_name = os.path.basename(test_folder)

        total_unique_skills = set()
        skills_with_resources = set()
        resource_count_by_cat = {}
        total_resources = 0
        has_guides = False
        has_skill_details = False
        has_prerequisites = False

        for session in path:
            skills = session.get('skills', [])
            for s in skills:
                total_unique_skills.add(s)

            # Check learning_resources
            resources = session.get('learning_resources', {})
            nonempty = False
            for cat, items in resources.items():
                if items:
                    nonempty = True
                    resource_count_by_cat[cat] = resource_count_by_cat.get(cat, 0) + len(items)
                    total_resources += len(items)
            if nonempty:
                for s in skills:
                    skills_with_resources.add(s)

            if session.get('comprehensive_guides'):
                has_guides = True
            if session.get('skill_details'):
                has_skill_details = True
            if session.get('prerequisites') is not None:
                has_prerequisites = True

        total = len(total_unique_skills)
        covered = len(skills_with_resources)
        coverage_pct = (covered / total * 100) if total > 0 else 0

        results.append({
            'test_name': test_name,
            'unique_skills': total,
            'skills_with_resources': covered,
            'coverage_pct': coverage_pct,
            'total_resources': total_resources,
            'resources_by_category': resource_count_by_cat,
            'has_guides': has_guides,
            'has_skill_details': has_skill_details,
            'has_prerequisites': has_prerequisites,
            'sessions': len(path)
        })
    return results


# ============================================================
# Graph Generation
# ============================================================
def generate_graphs(gemini_data, gpt_data, output_dirs):
    """Generate all resource coverage graphs and save to both output directories."""

    gemini_cov = [d['coverage_pct'] for d in gemini_data]
    gpt_cov = [d['coverage_pct'] for d in gpt_data]
    gemini_res = [d['total_resources'] for d in gemini_data]
    gpt_res = [d['total_resources'] for d in gpt_data]

    # ---- GRAPH 1: Resource Coverage Comparison Bar Chart ----
    fig, ax = plt.subplots(figsize=(14, 7))
    x = np.arange(len(TEST_LABELS))
    width = 0.35

    bars1 = ax.bar(x - width/2, gemini_cov, width, label='Gemini 2.5 Flash',
                   color=COLORS['gemini'], alpha=0.85, edgecolor='white', linewidth=0.5)
    bars2 = ax.bar(x + width/2, gpt_cov, width, label='GPT-5.2',
                   color=COLORS['gpt'], alpha=0.85, edgecolor='white', linewidth=0.5)

    # Value labels on Gemini bars
    for bar, val in zip(bars1, gemini_cov):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                    f'{val:.0f}%', ha='center', va='bottom', fontsize=7, fontweight='bold',
                    color=COLORS['gemini'])

    # Value labels on GPT bars
    for bar, val in zip(bars2, gpt_cov):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                    f'{val:.0f}%', ha='center', va='bottom', fontsize=7, fontweight='bold',
                    color=COLORS['gpt'])

    # Mean lines
    gemini_mean = statistics.mean(gemini_cov)
    gpt_mean = statistics.mean(gpt_cov)
    ax.axhline(y=gemini_mean, color=COLORS['gemini'], linestyle='--', alpha=0.6, linewidth=1)
    ax.text(len(TEST_LABELS) - 0.5, gemini_mean + 1.5, f'Gemini Mean: {gemini_mean:.1f}%',
            fontsize=8, color=COLORS['gemini'], ha='right')
    ax.axhline(y=gpt_mean, color=COLORS['gpt'], linestyle='--', alpha=0.6, linewidth=1)
    ax.text(len(TEST_LABELS) - 0.5, gpt_mean + 1.5, f'GPT Mean: {gpt_mean:.1f}%',
            fontsize=8, color=COLORS['gpt'], ha='right')

    ax.set_xlabel('Test Cases')
    ax.set_ylabel('Resource Coverage (%)')
    ax.set_title('Learning Resource Coverage: Gemini vs GPT-5.2', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(TEST_LABELS, rotation=45, ha='right', fontsize=8)
    ax.set_ylim(0, 115)
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    for out_dir in output_dirs:
        plt.savefig(os.path.join(out_dir, '13_resource_coverage_comparison.png'))
        plt.savefig(os.path.join(out_dir, '13_resource_coverage_comparison.pdf'))
    plt.close()
    print("  ✅ Graph 1: Resource Coverage Comparison")

    # ---- GRAPH 2: Total Resources Per Test Case ----
    fig, ax = plt.subplots(figsize=(14, 7))

    bars1 = ax.bar(x - width/2, gemini_res, width, label='Gemini 2.5 Flash',
                   color=COLORS['gemini'], alpha=0.85, edgecolor='white', linewidth=0.5)
    bars2 = ax.bar(x + width/2, gpt_res, width, label='GPT-5.2',
                   color=COLORS['gpt'], alpha=0.85, edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars1, gemini_res):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(val), ha='center', va='bottom', fontsize=7, fontweight='bold',
                    color=COLORS['gemini'])

    for bar, val in zip(bars2, gpt_res):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(val), ha='center', va='bottom', fontsize=7, fontweight='bold',
                    color=COLORS['gpt'])

    ax.set_xlabel('Test Cases')
    ax.set_ylabel('Total Learning Resources')
    ax.set_title('Total Learning Resources Generated: Gemini vs GPT-5.2', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(TEST_LABELS, rotation=45, ha='right', fontsize=8)
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    for out_dir in output_dirs:
        plt.savefig(os.path.join(out_dir, '14_total_resources_comparison.png'))
        plt.savefig(os.path.join(out_dir, '14_total_resources_comparison.pdf'))
    plt.close()
    print("  ✅ Graph 2: Total Resources Comparison")

    # ---- GRAPH 3: Content Richness Dashboard (2x2) ----
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 3a: Coverage distribution (pie charts)
    gemini_covered = sum(1 for c in gemini_cov if c > 0)
    gemini_partial = sum(1 for c in gemini_cov if 0 < c < 100)
    gemini_full = sum(1 for c in gemini_cov if c == 100)
    gemini_none = sum(1 for c in gemini_cov if c == 0)

    sizes_gemini = [gemini_full, gemini_partial, gemini_none]
    labels_pie = ['Full (100%)', 'Partial (1-99%)', 'None (0%)']
    colors_pie = [COLORS['success'], COLORS['warning'], COLORS['danger']]

    axes[0, 0].pie(sizes_gemini, labels=labels_pie, colors=colors_pie, autopct='%1.0f%%',
                   startangle=90, textprops={'fontsize': 9})
    axes[0, 0].set_title('Gemini: Resource Coverage Distribution', fontweight='bold')

    # GPT coverage distribution (computed dynamically)
    gpt_full = sum(1 for c in gpt_cov if c == 100)
    gpt_partial = sum(1 for c in gpt_cov if 0 < c < 100)
    gpt_none = sum(1 for c in gpt_cov if c == 0)
    sizes_gpt = [gpt_full, gpt_partial, gpt_none]

    # Only show slices that are > 0 to avoid crowding
    gpt_labels = [l for l, s in zip(labels_pie, sizes_gpt) if s > 0]
    gpt_sizes = [s for s in sizes_gpt if s > 0]
    gpt_colors = [c for c, s in zip(colors_pie, sizes_gpt) if s > 0]

    axes[0, 1].pie(gpt_sizes, labels=gpt_labels, colors=gpt_colors, autopct='%1.0f%%',
                   startangle=90, textprops={'fontsize': 9})
    axes[0, 1].set_title('GPT-5.2: Resource Coverage Distribution', fontweight='bold')

    # 3b: Content features comparison
    features = ['Learning\nResources', 'Comprehensive\nGuides', 'Skill\nDetails', 'Prerequisites']
    gemini_has = [
        sum(1 for d in gemini_data if d['total_resources'] > 0),
        sum(1 for d in gemini_data if d['has_guides']),
        sum(1 for d in gemini_data if d['has_skill_details']),
        sum(1 for d in gemini_data if d['has_prerequisites'])
    ]
    gpt_has = [
        sum(1 for d in gpt_data if d['total_resources'] > 0),
        sum(1 for d in gpt_data if d['has_guides']),
        sum(1 for d in gpt_data if d['has_skill_details']),
        sum(1 for d in gpt_data if d['has_prerequisites'])
    ]

    x_feat = np.arange(len(features))
    axes[1, 0].bar(x_feat - 0.2, gemini_has, 0.4, label='Gemini', color=COLORS['gemini'], alpha=0.85)
    axes[1, 0].bar(x_feat + 0.2, gpt_has, 0.4, label='GPT-5.2', color=COLORS['gpt'], alpha=0.85)
    axes[1, 0].set_xticks(x_feat)
    axes[1, 0].set_xticklabels(features, fontsize=9)
    axes[1, 0].set_ylabel('Number of Test Cases (out of 20)')
    axes[1, 0].set_ylim(0, 22)
    axes[1, 0].set_title('Content Feature Availability', fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(axis='y', alpha=0.3)

    # Add value labels
    for bar_group, vals in [(axes[1, 0].patches[:4], gemini_has), (axes[1, 0].patches[4:], gpt_has)]:
        for bar, val in zip(bar_group, vals):
            axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                            str(val), ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 3c: Resource category breakdown (both Gemini and GPT)
    gemini_cats = {}
    for d in gemini_data:
        for cat, count in d['resources_by_category'].items():
            gemini_cats[cat] = gemini_cats.get(cat, 0) + count

    gpt_cats = {}
    for d in gpt_data:
        for cat, count in d['resources_by_category'].items():
            gpt_cats[cat] = gpt_cats.get(cat, 0) + count

    # Merge all category keys
    all_cat_keys = sorted(set(list(gemini_cats.keys()) + list(gpt_cats.keys())),
                          key=lambda k: gemini_cats.get(k, 0) + gpt_cats.get(k, 0), reverse=True)

    if all_cat_keys:
        cat_labels = [c.replace('_', ' ').title() for c in all_cat_keys]
        gemini_vals = [gemini_cats.get(k, 0) for k in all_cat_keys]
        gpt_vals = [gpt_cats.get(k, 0) for k in all_cat_keys]
        y_pos = np.arange(len(cat_labels))
        bar_h = 0.35

        axes[1, 1].barh(y_pos - bar_h/2, gemini_vals, bar_h, label='Gemini',
                        color=COLORS['gemini'], alpha=0.85, edgecolor='white')
        axes[1, 1].barh(y_pos + bar_h/2, gpt_vals, bar_h, label='GPT-5.2',
                        color=COLORS['gpt'], alpha=0.85, edgecolor='white')
        for i, v in enumerate(gemini_vals):
            if v > 0:
                axes[1, 1].text(v + 1, i - bar_h/2, str(v), va='center', fontsize=8, fontweight='bold', color=COLORS['gemini'])
        for i, v in enumerate(gpt_vals):
            if v > 0:
                axes[1, 1].text(v + 1, i + bar_h/2, str(v), va='center', fontsize=8, fontweight='bold', color=COLORS['gpt'])
        axes[1, 1].set_yticks(y_pos)
        axes[1, 1].set_yticklabels(cat_labels)
        axes[1, 1].set_xlabel('Total Resources Across All Tests')
        axes[1, 1].set_title('Resources by Category: Gemini vs GPT-5.2', fontweight='bold')
        axes[1, 1].legend(fontsize=8)
        axes[1, 1].grid(axis='x', alpha=0.3)
    else:
        axes[1, 1].text(0.5, 0.5, 'No resource categories', ha='center', va='center', transform=axes[1, 1].transAxes)

    fig.suptitle('Learning Resource Coverage Dashboard: Gemini vs GPT-5.2',
                 fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    for out_dir in output_dirs:
        plt.savefig(os.path.join(out_dir, '15_resource_coverage_dashboard.png'))
        plt.savefig(os.path.join(out_dir, '15_resource_coverage_dashboard.pdf'))
    plt.close()
    print("  ✅ Graph 3: Resource Coverage Dashboard")

    # ---- GRAPH 4: Category-wise Resource Coverage (Gemini vs GPT) ----
    fig, ax = plt.subplots(figsize=(14, 7))

    gemini_cat_coverage = {}
    gpt_cat_coverage = {}
    for i in range(len(gemini_data)):
        cat = CATEGORIES[TEST_LABELS[i]]
        if cat not in gemini_cat_coverage:
            gemini_cat_coverage[cat] = []
            gpt_cat_coverage[cat] = []
        gemini_cat_coverage[cat].append(gemini_data[i]['coverage_pct'])
        gpt_cat_coverage[cat].append(gpt_data[i]['coverage_pct'])

    # Sort by average of both providers combined
    all_cats_sorted = sorted(gemini_cat_coverage.keys(),
                             key=lambda c: (statistics.mean(gemini_cat_coverage[c]) + statistics.mean(gpt_cat_coverage[c])) / 2,
                             reverse=True)
    cat_names = all_cats_sorted
    gemini_cat_means = [statistics.mean(gemini_cat_coverage[c]) for c in cat_names]
    gpt_cat_means = [statistics.mean(gpt_cat_coverage[c]) for c in cat_names]

    x_cat = np.arange(len(cat_names))
    width_cat = 0.35

    bars_g = ax.bar(x_cat - width_cat/2, gemini_cat_means, width_cat, label='Gemini 2.5 Flash',
                    color=COLORS['gemini'], alpha=0.85, edgecolor='white', linewidth=0.5)
    bars_p = ax.bar(x_cat + width_cat/2, gpt_cat_means, width_cat, label='GPT-5.2',
                    color=COLORS['gpt'], alpha=0.85, edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars_g, gemini_cat_means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f'{val:.0f}%', ha='center', va='bottom', fontsize=9, fontweight='bold', color=COLORS['gemini'])
    for bar, val in zip(bars_p, gpt_cat_means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f'{val:.0f}%', ha='center', va='bottom', fontsize=9, fontweight='bold', color=COLORS['gpt'])

    ax.set_xticks(x_cat)
    ax.set_xticklabels(cat_names, rotation=30, ha='right')
    ax.set_ylabel('Average Resource Coverage (%)')
    ax.set_title('Average Resource Coverage by Career Category: Gemini vs GPT-5.2', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 120)
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    # Mean lines
    overall_gemini = statistics.mean(gemini_cov)
    overall_gpt = statistics.mean(gpt_cov)
    ax.axhline(y=overall_gemini, color=COLORS['gemini'], linestyle='--', alpha=0.5, linewidth=1)
    ax.axhline(y=overall_gpt, color=COLORS['gpt'], linestyle='--', alpha=0.5, linewidth=1)
    ax.text(len(cat_names) - 0.5, overall_gemini + 2, f'Gemini Mean: {overall_gemini:.1f}%',
            fontsize=8, color=COLORS['gemini'], ha='right')
    ax.text(len(cat_names) - 0.5, overall_gpt + 2, f'GPT Mean: {overall_gpt:.1f}%',
            fontsize=8, color=COLORS['gpt'], ha='right')

    plt.tight_layout()
    for out_dir in output_dirs:
        plt.savefig(os.path.join(out_dir, '16_category_resource_coverage.png'))
        plt.savefig(os.path.join(out_dir, '16_category_resource_coverage.pdf'))
    plt.close()
    print("  ✅ Graph 4: Category-wise Resource Coverage")


# ============================================================
# Summary Report
# ============================================================
def print_summary(gemini_data, gpt_data):
    """Print a summary comparison table."""
    gemini_cov = [d['coverage_pct'] for d in gemini_data]
    gpt_cov = [d['coverage_pct'] for d in gpt_data]
    gemini_res = [d['total_resources'] for d in gemini_data]
    gpt_res = [d['total_resources'] for d in gpt_data]

    print("\n" + "=" * 80)
    print("  LEARNING RESOURCE COVERAGE ANALYSIS REPORT")
    print("=" * 80)

    print(f"\n{'Metric':<40} {'Gemini':>15} {'GPT-5.2':>15}")
    print("-" * 70)
    print(f"{'Mean Coverage (%)':<40} {statistics.mean(gemini_cov):>14.1f}% {statistics.mean(gpt_cov):>14.1f}%")
    print(f"{'Std Dev Coverage':<40} {statistics.stdev(gemini_cov):>14.1f}% {statistics.stdev(gpt_cov):>14.1f}%")
    print(f"{'Min Coverage':<40} {min(gemini_cov):>14.1f}% {min(gpt_cov):>14.1f}%")
    print(f"{'Max Coverage':<40} {max(gemini_cov):>14.1f}% {max(gpt_cov):>14.1f}%")
    print(f"{'Tests with Full Coverage (100%)':<40} {sum(1 for c in gemini_cov if c == 100):>15} {sum(1 for c in gpt_cov if c == 100):>15}")
    print(f"{'Tests with Partial Coverage':<40} {sum(1 for c in gemini_cov if 0 < c < 100):>15} {sum(1 for c in gpt_cov if 0 < c < 100):>15}")
    print(f"{'Tests with No Coverage (0%)':<40} {sum(1 for c in gemini_cov if c == 0):>15} {sum(1 for c in gpt_cov if c == 0):>15}")
    print(f"{'Total Resources Generated':<40} {sum(gemini_res):>15} {sum(gpt_res):>15}")
    print(f"{'Mean Resources Per Test':<40} {statistics.mean(gemini_res):>14.1f} {statistics.mean(gpt_res):>14.1f}")
    print(f"{'Tests with Guides':<40} {sum(1 for d in gemini_data if d['has_guides']):>15} {sum(1 for d in gpt_data if d['has_guides']):>15}")
    print(f"{'Tests with Skill Details':<40} {sum(1 for d in gemini_data if d['has_skill_details']):>15} {sum(1 for d in gpt_data if d['has_skill_details']):>15}")
    print(f"{'Tests with Prerequisites':<40} {sum(1 for d in gemini_data if d['has_prerequisites']):>15} {sum(1 for d in gpt_data if d['has_prerequisites']):>15}")

    print(f"\n{'Per-Test Breakdown':}")
    print(f"{'#':<3} {'Test Case':<22} {'Gemini Cov':>12} {'GPT Cov':>12} {'Gemini Res':>12} {'GPT Res':>12}")
    print("-" * 75)
    for i in range(20):
        print(f"{i+1:<3} {TEST_LABELS[i]:<22} {gemini_cov[i]:>11.0f}% {gpt_cov[i]:>11.0f}% {gemini_res[i]:>12} {gpt_res[i]:>12}")

    print("\n" + "=" * 80)


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("📊 Learning Resource Coverage Analysis")
    print("=" * 50)

    print(f"\n📁 Analyzing Gemini outputs: {GEMINI_DIR}")
    gemini_data = analyze_resources(GEMINI_DIR)
    print(f"   Found {len(gemini_data)} test cases")

    print(f"📁 Analyzing GPT-5.2 outputs: {GPT_DIR}")
    gpt_data = analyze_resources(GPT_DIR)
    print(f"   Found {len(gpt_data)} test cases")

    # Print summary
    print_summary(gemini_data, gpt_data)

    # Generate graphs into both folders
    output_dirs = []
    for d in [GEMINI_DIR, GPT_DIR]:
        graphs_dir = os.path.join(d, 'graphs')
        os.makedirs(graphs_dir, exist_ok=True)
        output_dirs.append(graphs_dir)

    print("\n📈 Generating graphs...")
    generate_graphs(gemini_data, gpt_data, output_dirs)

    print(f"\n✅ Graphs saved to:")
    for d in output_dirs:
        print(f"   {d}/")
    print("\nDone!")
