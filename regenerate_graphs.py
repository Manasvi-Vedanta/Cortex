"""
Regenerate Evaluation Graphs with Improved Formatting
This script reads the existing evaluation data and creates publication-quality visualizations.
"""

import json
import os
import statistics
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
    sns.set_palette("husl")
except ImportError:
    SEABORN_AVAILABLE = False

# Configuration
DATA_DIR = "evaluation_outputs_20260310_213714"
GRAPHS_DIR = os.path.join(DATA_DIR, "graphs")
SUMMARY_FILE = os.path.join(DATA_DIR, "evaluation_summary.json")

# Load data
with open(SUMMARY_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

test_results = data['test_results']

# Professional color scheme
COLORS = {
    'primary': '#1E3A5F',      # Deep blue
    'secondary': '#7B2D8E',    # Purple
    'success': '#0D7377',      # Teal
    'warning': '#E8871E',      # Orange
    'danger': '#C73E1D',       # Red
    'info': '#3498DB',         # Light blue
    'light_gray': '#F5F5F5',
    'dark_gray': '#2C3E50',
    'categories': [
        '#1E3A5F', '#7B2D8E', '#0D7377', '#E8871E', '#C73E1D', 
        '#3498DB', '#27AE60', '#8E44AD', '#F39C12', '#16A085',
        '#E74C3C'
    ],
    'categories_light': [
        '#7EAED3', '#C9A0D8', '#7BCBCE', '#F5C68A', '#E8A090',
        '#A3D1F2', '#8ED5A8', '#C9A3D9', '#F9D37A', '#8DD4C8',
        '#F0A8A0'
    ]
}

# Set global matplotlib style
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica'],
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.2,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--'
})


def save_figure(fig, name):
    """Save figure in both PNG and PDF formats"""
    fig.savefig(os.path.join(GRAPHS_DIR, f'{name}.png'), facecolor='white', edgecolor='none')
    fig.savefig(os.path.join(GRAPHS_DIR, f'{name}.pdf'), facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  ✓ Saved {name}")


def plot_01_similarity_scores():
    """Plot similarity scores with improved layout"""
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Sort by similarity score for better visualization
    sorted_results = sorted(test_results, key=lambda x: x['similarity_score'], reverse=True)
    
    names = [r['short_name'] for r in sorted_results]
    scores = [r['similarity_score'] for r in sorted_results]
    categories = [r['category'] for r in sorted_results]
    
    # Color by category
    unique_cats = list(set(categories))
    cat_colors = {cat: COLORS['categories_light'][i % len(COLORS['categories_light'])] 
                 for i, cat in enumerate(unique_cats)}
    bar_colors = [cat_colors[cat] for cat in categories]
    
    y_pos = np.arange(len(names))
    bars = ax.barh(y_pos, scores, color=bar_colors, edgecolor='white', linewidth=0.8, height=0.7)
    
    # Add value labels with better positioning
    for bar, score in zip(bars, scores):
        width = bar.get_width()
        ax.text(width + 0.015, bar.get_y() + bar.get_height()/2, 
               f'{score:.3f}', va='center', fontsize=9, fontweight='bold')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel('Similarity Score', fontweight='bold', fontsize=12)
    ax.set_title('Occupation Matching Similarity Scores\nAcross 20 Tech Career Goals', 
                fontweight='bold', fontsize=14, pad=15)
    ax.set_xlim(0, 1.15)
    
    # Add threshold lines
    ax.axvline(x=0.7, color='#D4A57A', linestyle='--', alpha=0.7, linewidth=1.5)
    ax.axvline(x=0.9, color='#7BCBCE', linestyle='--', alpha=0.7, linewidth=1.5)
    
    # Add threshold labels
    ax.text(0.70, len(names) + 0.3, 'Good (0.7)', color='#D4A57A', fontsize=9, ha='center')
    ax.text(0.90, len(names) + 0.3, 'Excellent (0.9)', color='#7BCBCE', fontsize=9, ha='center')
    
    # Create legend outside the plot
    legend_patches = [mpatches.Patch(color=cat_colors[cat], label=cat) for cat in sorted(unique_cats)]
    ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1.02, 1), 
             title='Category', title_fontsize=11, frameon=True, fancybox=True, shadow=True)
    
    # Add statistics annotation
    mean_score = statistics.mean(scores)
    ax.axvline(x=mean_score, color='#E8A090', linestyle='-', alpha=0.8, linewidth=2)
    ax.text(mean_score, -0.8, f'Mean: {mean_score:.3f}', color='#E8A090', 
           fontsize=10, ha='center', fontweight='bold')
    
    plt.tight_layout()
    save_figure(fig, '01_similarity_scores')


def plot_02_skills_distribution():
    """Plot skills count distribution with improved layout"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    names = [r['short_name'] for r in test_results]
    skills = [r['total_skills'] for r in test_results]
    sessions = [r['total_sessions'] for r in test_results]
    similarity = [r['similarity_score'] for r in test_results]
    
    # Left: Skills count bar chart
    ax1 = axes[0]
    x = np.arange(len(names))
    bars = ax1.bar(x, skills, color=COLORS['primary'], edgecolor='white', width=0.7)
    
    # Color bars based on skill count
    for bar, skill in zip(bars, skills):
        if skill >= 14:
            bar.set_color(COLORS['success'])
        elif skill >= 10:
            bar.set_color(COLORS['info'])
        else:
            bar.set_color(COLORS['warning'])
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
    ax1.set_ylabel('Number of Skills', fontweight='bold')
    ax1.set_title('Skills Generated per Career Goal', fontweight='bold', pad=10)
    ax1.set_ylim(0, max(skills) + 2)
    
    # Add mean line
    mean_skills = statistics.mean(skills)
    ax1.axhline(y=mean_skills, color=COLORS['danger'], linestyle='--', linewidth=2,
               label=f'Mean: {mean_skills:.1f}')
    ax1.legend(loc='upper right', frameon=True)
    
    # Add value labels on bars
    for bar, skill in zip(bars, skills):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, 
                str(skill), ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # Right: Sessions vs Skills scatter with size based on similarity
    ax2 = axes[1]
    sizes = [s * 200 for s in similarity]  # Scale similarity to point size
    scatter = ax2.scatter(sessions, skills, c=similarity, cmap='RdYlGn', 
                         s=sizes, alpha=0.7, edgecolors='black', linewidth=1)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax2, shrink=0.8, pad=0.02)
    cbar.set_label('Similarity Score', fontweight='bold')
    
    # Add labels for each point
    for i, name in enumerate(names):
        ax2.annotate(name[:12], (sessions[i], skills[i]), 
                    fontsize=7, alpha=0.8, ha='center', va='bottom',
                    xytext=(0, 5), textcoords='offset points')
    
    ax2.set_xlabel('Number of Sessions', fontweight='bold')
    ax2.set_ylabel('Number of Skills', fontweight='bold')
    ax2.set_title('Sessions vs Skills\n(Point size = Similarity Score)', fontweight='bold', pad=10)
    
    # Add trend line
    z = np.polyfit(sessions, skills, 1)
    p = np.poly1d(z)
    x_line = np.linspace(min(sessions), max(sessions), 100)
    ax2.plot(x_line, p(x_line), "r--", alpha=0.5, linewidth=2, label='Trend')
    ax2.legend(loc='lower right')
    
    plt.tight_layout()
    save_figure(fig, '02_skills_distribution')


def plot_03_response_times():
    """Plot response times with improved layout"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    names = [r['short_name'] for r in test_results]
    path_times = [r['path_generation_time'] for r in test_results]
    quiz_times = [r['quiz_generation_time'] for r in test_results]
    
    # Left: Grouped bar chart
    ax1 = axes[0]
    x = np.arange(len(names))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, path_times, width, label='Path Generation', 
                   color=COLORS['primary'], edgecolor='white')
    bars2 = ax1.bar(x + width/2, quiz_times, width, label='Quiz Generation',
                   color=COLORS['secondary'], edgecolor='white')
    
    ax1.set_ylabel('Time (seconds)', fontweight='bold')
    ax1.set_title('API Response Times by Career Goal', fontweight='bold', pad=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax1.legend(loc='upper right', frameon=True, fancybox=True)
    
    # Add mean lines
    mean_path = statistics.mean(path_times)
    mean_quiz = statistics.mean(quiz_times)
    ax1.axhline(y=mean_path, color=COLORS['primary'], linestyle=':', alpha=0.7, linewidth=2)
    ax1.axhline(y=mean_quiz, color=COLORS['secondary'], linestyle=':', alpha=0.7, linewidth=2)
    
    # Right: Box plot with swarm overlay
    ax2 = axes[1]
    
    bp_data = [path_times, quiz_times]
    positions = [1, 2]
    
    bp = ax2.boxplot(bp_data, positions=positions, widths=0.5, patch_artist=True,
                    showmeans=True, meanline=True,
                    meanprops=dict(linestyle='-', linewidth=2, color='red'),
                    medianprops=dict(linestyle='-', linewidth=2, color='black'))
    
    bp['boxes'][0].set_facecolor(COLORS['primary'])
    bp['boxes'][1].set_facecolor(COLORS['secondary'])
    bp['boxes'][0].set_alpha(0.7)
    bp['boxes'][1].set_alpha(0.7)
    
    # Add individual points
    for i, times in enumerate(bp_data, 1):
        jitter = np.random.normal(0, 0.04, len(times))
        ax2.scatter([i + j for j in jitter], times, alpha=0.5, s=30, 
                   color='black', edgecolors='white', zorder=3)
    
    ax2.set_xticklabels(['Path Generation', 'Quiz Generation'], fontsize=11)
    ax2.set_ylabel('Time (seconds)', fontweight='bold')
    ax2.set_title('Response Time Distribution\n(Red line = Mean, Black line = Median)', 
                 fontweight='bold', pad=10)
    
    # Add statistics text box
    stats_text = (f'Path Gen:\n  Mean: {mean_path:.1f}s\n  Std: {statistics.stdev(path_times):.1f}s\n\n'
                  f'Quiz Gen:\n  Mean: {mean_quiz:.1f}s\n  Std: {statistics.stdev(quiz_times):.1f}s')
    ax2.text(0.98, 0.98, stats_text, transform=ax2.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    save_figure(fig, '03_response_times')


def plot_04_success_rates():
    """Plot success rates with improved layout"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    total = len(test_results)
    
    # Left: Feature success rates
    ax1 = axes[0]
    
    features = ['Path\nGeneration', 'Quiz\nGeneration', 'Community\nVoting', 
                'Skill\nSuggestions', 'Path\nRegeneration', 'Overall\nSuccess']
    success_counts = [
        sum(1 for r in test_results if r['path_generation_success']),
        sum(1 for r in test_results if r['quiz_generation_success']),
        sum(1 for r in test_results if r['voting_success']),
        sum(1 for r in test_results if r['suggestions_success']),
        sum(1 for r in test_results if r['regeneration_success']),
        sum(1 for r in test_results if r['overall_success'])
    ]
    success_rates = [count/total * 100 for count in success_counts]
    
    colors = ['#A8D8B9' if rate >= 90 else 
             '#F5D6A0' if rate >= 70 else 
             '#F2B8B0' for rate in success_rates]
    
    x = np.arange(len(features))
    bars = ax1.bar(x, success_rates, color=colors, edgecolor='white', width=0.6)
    
    # Add value labels
    for bar, rate, count in zip(bars, success_rates, success_counts):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f'{rate:.0f}%\n({count}/{total})', ha='center', fontsize=10, fontweight='bold')
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(features, fontsize=10)
    ax1.set_ylabel('Success Rate (%)', fontweight='bold')
    ax1.set_title('Feature Success Rates Across All Tests', fontweight='bold', pad=10)
    ax1.set_ylim(0, 115)
    ax1.axhline(y=90, color='#A8D8B9', linestyle='--', alpha=0.5, linewidth=2)
    ax1.text(len(features)-0.5, 91, 'Target: 90%', color='#6BAF8D', fontsize=9)
    
    # Right: Success matrix heatmap
    ax2 = axes[1]
    
    test_names = [r['short_name'][:15] for r in test_results]
    feature_names = ['Path', 'Quiz', 'Vote', 'Suggest', 'Regen']
    
    success_matrix = np.array([
        [r['path_generation_success'], r['quiz_generation_success'], 
         r['voting_success'], r['suggestions_success'], r['regeneration_success']]
        for r in test_results
    ]).astype(int)
    
    from matplotlib.colors import LinearSegmentedColormap
    soft_cmap = LinearSegmentedColormap.from_list('soft_rg', ['#F2B8B0', '#A8D8B9'])
    im = ax2.imshow(success_matrix, cmap=soft_cmap, aspect='auto', vmin=0, vmax=1)
    
    ax2.set_xticks(range(len(feature_names)))
    ax2.set_xticklabels(feature_names, fontsize=10, fontweight='bold')
    ax2.set_yticks(range(len(test_names)))
    ax2.set_yticklabels(test_names, fontsize=8)
    ax2.set_title('Test × Feature Success Matrix\n(Green = Pass, Pink = Fail)', 
                 fontweight='bold', pad=10)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax2, shrink=0.8, pad=0.02)
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(['Fail', 'Pass'])
    
    plt.tight_layout()
    save_figure(fig, '04_success_rates')


def plot_05_category_analysis():
    """Plot category-wise analysis with improved layout"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    
    # Group data by category
    category_data = defaultdict(list)
    for r in test_results:
        category_data[r['category']].append(r)
    
    categories = sorted(category_data.keys())
    cat_colors = {cat: COLORS['categories_light'][i % len(COLORS['categories_light'])] 
                 for i, cat in enumerate(categories)}
    
    # 1. Average similarity by category (with error bars)
    ax1 = axes[0, 0]
    avg_similarity = [statistics.mean([r['similarity_score'] for r in category_data[cat]]) 
                     for cat in categories]
    std_similarity = [statistics.stdev([r['similarity_score'] for r in category_data[cat]]) 
                     if len(category_data[cat]) > 1 else 0 for cat in categories]
    
    x = np.arange(len(categories))
    bars = ax1.bar(x, avg_similarity, yerr=std_similarity, 
                  color=[cat_colors[c] for c in categories],
                  capsize=5, edgecolor='white', error_kw={'linewidth': 2})
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, rotation=30, ha='right', fontsize=9)
    ax1.set_ylabel('Average Similarity Score', fontweight='bold')
    ax1.set_title('Similarity Score by Category\n(Error bars = Std Dev)', fontweight='bold', pad=10)
    ax1.set_ylim(0, 1.1)
    
    # Add value labels
    for bar, val in zip(bars, avg_similarity):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03, 
                f'{val:.2f}', ha='center', fontsize=9, fontweight='bold')
    
    # 2. Skills count by category
    ax2 = axes[0, 1]
    avg_skills = [statistics.mean([r['total_skills'] for r in category_data[cat]]) 
                 for cat in categories]
    
    bars = ax2.bar(x, avg_skills, color=[cat_colors[c] for c in categories], edgecolor='white')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, rotation=30, ha='right', fontsize=9)
    ax2.set_ylabel('Average Skills Count', fontweight='bold')
    ax2.set_title('Skills Generated by Category', fontweight='bold', pad=10)
    
    for bar, val in zip(bars, avg_skills):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
                f'{val:.1f}', ha='center', fontsize=9, fontweight='bold')
    
    # 3. Response time by category
    ax3 = axes[1, 0]
    avg_time = [statistics.mean([r['path_generation_time'] for r in category_data[cat]]) 
               for cat in categories]
    
    bars = ax3.bar(x, avg_time, color=[cat_colors[c] for c in categories], edgecolor='white')
    ax3.set_xticks(x)
    ax3.set_xticklabels(categories, rotation=30, ha='right', fontsize=9)
    ax3.set_ylabel('Average Response Time (seconds)', fontweight='bold')
    ax3.set_title('Path Generation Time by Category', fontweight='bold', pad=10)
    
    for bar, val in zip(bars, avg_time):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
                f'{val:.1f}s', ha='center', fontsize=9, fontweight='bold')
    
    # 4. Test count per category (donut chart)
    ax4 = axes[1, 1]
    test_counts = [len(category_data[cat]) for cat in categories]
    
    wedges, texts, autotexts = ax4.pie(
        test_counts, labels=None, autopct='%1.0f%%',
        colors=[cat_colors[c] for c in categories],
        explode=[0.02]*len(categories), pctdistance=0.75,
        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2)
    )
    
    # Improve autopct text
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    
    ax4.set_title('Test Distribution by Category', fontweight='bold', pad=10)
    
    # Add legend outside
    ax4.legend(wedges, [f'{cat} ({count})' for cat, count in zip(categories, test_counts)],
              title='Categories', loc='center left', bbox_to_anchor=(1, 0.5),
              fontsize=9, title_fontsize=10)
    
    plt.tight_layout()
    save_figure(fig, '05_category_analysis')


def plot_06_quiz_metrics():
    """Plot quiz-related metrics with improved layout"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    names = [r['short_name'] for r in test_results]
    q_counts = [r['quiz_questions_count'] for r in test_results]
    quiz_times = [r['quiz_generation_time'] for r in test_results]
    
    # 1. Quiz questions count
    ax1 = axes[0]
    colors = [COLORS['success'] if q == 10 else COLORS['warning'] if q > 0 else COLORS['danger'] 
             for q in q_counts]
    
    x = np.arange(len(names))
    bars = ax1.bar(x, q_counts, color=colors, edgecolor='white')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax1.set_ylabel('Question Count', fontweight='bold')
    ax1.set_title('Quiz Questions Generated per Goal', fontweight='bold', pad=10)
    ax1.axhline(y=10, color=COLORS['danger'], linestyle='--', linewidth=2, alpha=0.7)
    ax1.text(len(names)-1, 10.3, 'Target: 10', color=COLORS['danger'], fontsize=9)
    ax1.set_ylim(0, 12)
    
    # 2. Difficulty distribution (stacked)
    ax2 = axes[1]
    easy = [r['quiz_difficulty_distribution'].get('easy', 0) for r in test_results]
    medium = [r['quiz_difficulty_distribution'].get('medium', 0) for r in test_results]
    hard = [r['quiz_difficulty_distribution'].get('hard', 0) for r in test_results]
    
    ax2.bar(x, easy, label='Easy', color=COLORS['success'], edgecolor='white')
    ax2.bar(x, medium, bottom=easy, label='Medium', color=COLORS['warning'], edgecolor='white')
    ax2.bar(x, hard, bottom=[e+m for e,m in zip(easy, medium)], 
           label='Hard', color=COLORS['danger'], edgecolor='white')
    
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax2.set_ylabel('Question Count', fontweight='bold')
    ax2.set_title('Quiz Difficulty Distribution', fontweight='bold', pad=10)
    ax2.legend(loc='upper right', frameon=True, fancybox=True)
    
    # 3. Quiz generation time histogram
    ax3 = axes[2]
    valid_times = [t for t in quiz_times if t > 0]
    
    n, bins, patches = ax3.hist(valid_times, bins=8, color=COLORS['secondary'], 
                                edgecolor='white', alpha=0.7, linewidth=1.5)
    
    # Color histogram bars by value
    for patch, binval in zip(patches, bins[:-1]):
        if binval < 20:
            patch.set_facecolor(COLORS['success'])
        elif binval < 30:
            patch.set_facecolor(COLORS['warning'])
        else:
            patch.set_facecolor(COLORS['danger'])
    
    mean_time = statistics.mean(valid_times)
    ax3.axvline(x=mean_time, color=COLORS['danger'], linestyle='-', linewidth=2.5,
               label=f'Mean: {mean_time:.1f}s')
    ax3.axvline(x=statistics.median(valid_times), color=COLORS['primary'], 
               linestyle='--', linewidth=2, label=f'Median: {statistics.median(valid_times):.1f}s')
    
    ax3.set_xlabel('Time (seconds)', fontweight='bold')
    ax3.set_ylabel('Frequency', fontweight='bold')
    ax3.set_title('Quiz Generation Time Distribution', fontweight='bold', pad=10)
    ax3.legend(loc='upper right', frameon=True)
    
    plt.tight_layout()
    save_figure(fig, '06_quiz_metrics')


def plot_07_session_analysis():
    """Plot session-related analysis with improved layout"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    names = [r['short_name'] for r in test_results]
    sessions = [r['total_sessions'] for r in test_results]
    skills = [r['total_skills'] for r in test_results]
    
    # 1. Session count with color coding
    ax1 = axes[0]
    x = np.arange(len(names))
    colors = [COLORS['success'] if s >= 3 else COLORS['warning'] if s >= 2 else COLORS['danger'] 
             for s in sessions]
    
    bars = ax1.bar(x, sessions, color=colors, edgecolor='white')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
    ax1.set_ylabel('Number of Sessions', fontweight='bold')
    ax1.set_title('Learning Path Sessions per Goal', fontweight='bold', pad=10)
    ax1.axhline(y=3, color=COLORS['info'], linestyle='--', linewidth=2, alpha=0.7)
    ax1.text(len(names)-1, 3.1, 'Recommended: 3+', color=COLORS['info'], fontsize=9)
    
    # Add value labels
    for bar, val in zip(bars, sessions):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(val), ha='center', fontsize=9, fontweight='bold')
    
    # 2. Skills per session ratio with trend
    ax2 = axes[1]
    ratios = [skills[i] / sessions[i] if sessions[i] > 0 else 0 for i in range(len(names))]
    
    colors = [COLORS['success'] if r >= 5 else COLORS['warning'] if r >= 3 else COLORS['danger'] 
             for r in ratios]
    bars = ax2.bar(x, ratios, color=colors, edgecolor='white')
    
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
    ax2.set_ylabel('Skills per Session', fontweight='bold')
    ax2.set_title('Average Skills per Session', fontweight='bold', pad=10)
    
    mean_ratio = statistics.mean(ratios)
    ax2.axhline(y=mean_ratio, color=COLORS['danger'], linestyle='--', linewidth=2,
               label=f'Mean: {mean_ratio:.1f}')
    ax2.legend(loc='upper right', frameon=True)
    
    # Add value labels
    for bar, val in zip(bars, ratios):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{val:.1f}', ha='center', fontsize=8, fontweight='bold')
    
    plt.tight_layout()
    save_figure(fig, '07_session_analysis')


def plot_08_comprehensive_dashboard():
    """Create a comprehensive dashboard with all key metrics"""
    fig = plt.figure(figsize=(24, 18))
    gs = GridSpec(4, 4, figure=fig, hspace=0.35, wspace=0.3)
    
    # Title
    fig.suptitle('Hybrid GenMentor - Comprehensive Evaluation Dashboard\n20 Tech Career Goal Tests', 
                fontsize=20, fontweight='bold', y=0.98)
    
    # 1. Success Rate Gauge (top left)
    ax1 = fig.add_subplot(gs[0, 0:2])
    success_rate = sum(1 for r in test_results if r['overall_success']) / len(test_results) * 100
    
    # Create semi-circle gauge
    theta = np.linspace(0, np.pi, 100)
    ax1.fill_between(theta, 0, 1, color='#E0E0E0', alpha=0.5)
    
    # Color sections
    ax1.fill_between(np.linspace(0, np.pi*0.6, 60), 0, 1, color=COLORS['danger'], alpha=0.3)
    ax1.fill_between(np.linspace(np.pi*0.6, np.pi*0.8, 20), 0, 1, color=COLORS['warning'], alpha=0.3)
    ax1.fill_between(np.linspace(np.pi*0.8, np.pi, 20), 0, 1, color=COLORS['success'], alpha=0.3)
    
    success_theta = np.linspace(0, np.pi * (success_rate/100), 100)
    ax1.fill_between(success_theta, 0, 0.8, color=COLORS['success'], alpha=0.8)
    
    ax1.set_xlim(0, np.pi)
    ax1.set_ylim(0, 1.3)
    ax1.text(np.pi/2, 0.4, f'{success_rate:.0f}%', ha='center', va='center', 
            fontsize=40, fontweight='bold', color=COLORS['dark_gray'])
    ax1.text(np.pi/2, 0.05, 'Overall Success Rate', ha='center', fontsize=12, fontweight='bold')
    ax1.axis('off')
    ax1.set_title('System Performance', fontweight='bold', fontsize=14, pad=5)
    
    # 2. Key Statistics (top right)
    ax2 = fig.add_subplot(gs[0, 2:4])
    
    similarity_scores = [r['similarity_score'] for r in test_results]
    skills_counts = [r['total_skills'] for r in test_results]
    path_times = [r['path_generation_time'] for r in test_results]
    quiz_times = [r['quiz_generation_time'] for r in test_results if r['quiz_generation_time'] > 0]
    
    stats_data = [
        ['Metric', 'Mean', 'Std Dev', 'Min', 'Max'],
        ['Similarity Score', f'{statistics.mean(similarity_scores):.3f}', 
         f'{statistics.stdev(similarity_scores):.3f}', 
         f'{min(similarity_scores):.3f}', f'{max(similarity_scores):.3f}'],
        ['Skills Generated', f'{statistics.mean(skills_counts):.1f}', 
         f'{statistics.stdev(skills_counts):.1f}',
         f'{min(skills_counts)}', f'{max(skills_counts)}'],
        ['Path Gen Time (s)', f'{statistics.mean(path_times):.1f}', 
         f'{statistics.stdev(path_times):.1f}',
         f'{min(path_times):.1f}', f'{max(path_times):.1f}'],
        ['Quiz Gen Time (s)', f'{statistics.mean(quiz_times):.1f}', 
         f'{statistics.stdev(quiz_times):.1f}',
         f'{min(quiz_times):.1f}', f'{max(quiz_times):.1f}']
    ]
    
    ax2.axis('off')
    table = ax2.table(cellText=stats_data[1:], colLabels=stats_data[0],
                     loc='center', cellLoc='center',
                     colColours=[COLORS['primary']]*5)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.8)
    
    for i in range(5):
        table[(0, i)].set_text_props(color='white', fontweight='bold')
    
    ax2.set_title('Key Statistical Metrics', fontweight='bold', fontsize=14, pad=10)
    
    # 3. Similarity Score Distribution (middle left)
    ax3 = fig.add_subplot(gs[1, 0:2])
    scores = [r['similarity_score'] for r in test_results]
    
    n, bins, patches = ax3.hist(scores, bins=10, color=COLORS['primary'], 
                                edgecolor='white', alpha=0.7)
    ax3.axvline(x=statistics.mean(scores), color=COLORS['danger'], linestyle='-', 
               linewidth=2.5, label=f'Mean: {statistics.mean(scores):.3f}')
    ax3.axvline(x=statistics.median(scores), color=COLORS['warning'], linestyle='--',
               linewidth=2, label=f'Median: {statistics.median(scores):.3f}')
    ax3.set_xlabel('Similarity Score', fontweight='bold')
    ax3.set_ylabel('Frequency', fontweight='bold')
    ax3.set_title('Similarity Score Distribution', fontweight='bold', pad=10)
    ax3.legend(loc='upper left', frameon=True)
    
    # 4. Skills vs Time Scatter (middle right)
    ax4 = fig.add_subplot(gs[1, 2:4])
    skills = [r['total_skills'] for r in test_results]
    times = [r['path_generation_time'] for r in test_results]
    
    scatter = ax4.scatter(times, skills, c=scores, cmap='RdYlGn', 
                         s=150, alpha=0.8, edgecolors='black', linewidth=1)
    cbar = plt.colorbar(scatter, ax=ax4, shrink=0.8)
    cbar.set_label('Similarity Score', fontweight='bold')
    ax4.set_xlabel('Generation Time (seconds)', fontweight='bold')
    ax4.set_ylabel('Skills Count', fontweight='bold')
    ax4.set_title('Skills vs Generation Time\n(Color = Similarity)', fontweight='bold', pad=10)
    
    # 5. Category Performance (bottom left)
    ax5 = fig.add_subplot(gs[2, 0:2])
    category_data = defaultdict(list)
    for r in test_results:
        category_data[r['category']].append(r['similarity_score'])
    
    categories = sorted(category_data.keys())
    avg_scores = [statistics.mean(category_data[cat]) for cat in categories]
    
    colors = [COLORS['categories'][i % len(COLORS['categories'])] for i in range(len(categories))]
    bars = ax5.barh(categories, avg_scores, color=colors, edgecolor='white')
    
    for bar, score in zip(bars, avg_scores):
        ax5.text(score + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{score:.2f}', va='center', fontsize=9, fontweight='bold')
    
    ax5.set_xlabel('Average Similarity Score', fontweight='bold')
    ax5.set_title('Performance by Category', fontweight='bold', pad=10)
    ax5.set_xlim(0, 1.1)
    
    # 6. Feature Success (bottom middle)
    ax6 = fig.add_subplot(gs[2, 2:4])
    features = ['Path', 'Quiz', 'Vote', 'Suggest', 'Regen']
    success_pcts = [
        sum(1 for r in test_results if r['path_generation_success']) / len(test_results) * 100,
        sum(1 for r in test_results if r['quiz_generation_success']) / len(test_results) * 100,
        sum(1 for r in test_results if r['voting_success']) / len(test_results) * 100,
        sum(1 for r in test_results if r['suggestions_success']) / len(test_results) * 100,
        sum(1 for r in test_results if r['regeneration_success']) / len(test_results) * 100
    ]
    
    colors = [COLORS['success'] if p >= 90 else COLORS['warning'] for p in success_pcts]
    bars = ax6.bar(features, success_pcts, color=colors, edgecolor='white')
    
    for bar, pct in zip(bars, success_pcts):
        ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{pct:.0f}%', ha='center', fontsize=10, fontweight='bold')
    
    ax6.set_ylabel('Success Rate (%)', fontweight='bold')
    ax6.set_title('Feature Success Rates', fontweight='bold', pad=10)
    ax6.set_ylim(0, 110)
    
    # 7. Top Performing Goals (bottom row left)
    ax7 = fig.add_subplot(gs[3, 0:2])
    sorted_results = sorted(test_results, key=lambda r: r['similarity_score'], reverse=True)[:7]
    names = [r['short_name'] for r in sorted_results]
    scores = [r['similarity_score'] for r in sorted_results]
    
    colors = [COLORS['success'] if s >= 0.9 else COLORS['info'] for s in scores]
    bars = ax7.barh(names[::-1], scores[::-1], color=colors[::-1], edgecolor='white')
    
    for bar, score in zip(bars, scores[::-1]):
        ax7.text(score + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{score:.3f}', va='center', fontsize=9, fontweight='bold')
    
    ax7.set_xlabel('Similarity Score', fontweight='bold')
    ax7.set_title('Top 7 Performing Goals', fontweight='bold', pad=10)
    ax7.set_xlim(0, 1.1)
    
    # 8. Response Time Comparison (bottom row right)
    ax8 = fig.add_subplot(gs[3, 2:4])
    path_times = [r['path_generation_time'] for r in test_results]
    quiz_times = [r['quiz_generation_time'] for r in test_results if r['quiz_generation_time'] > 0]
    
    bp = ax8.boxplot([path_times, quiz_times], tick_labels=['Path Generation', 'Quiz Generation'],
                    patch_artist=True, showmeans=True,
                    meanprops=dict(marker='D', markerfacecolor='red', markeredgecolor='red'))
    
    bp['boxes'][0].set_facecolor(COLORS['primary'])
    bp['boxes'][1].set_facecolor(COLORS['secondary'])
    bp['boxes'][0].set_alpha(0.7)
    bp['boxes'][1].set_alpha(0.7)
    
    ax8.set_ylabel('Time (seconds)', fontweight='bold')
    ax8.set_title('Response Time Distribution\n(Diamond = Mean)', fontweight='bold', pad=10)
    
    plt.savefig(os.path.join(GRAPHS_DIR, '08_comprehensive_dashboard.png'), facecolor='white')
    plt.savefig(os.path.join(GRAPHS_DIR, '08_comprehensive_dashboard.pdf'), facecolor='white')
    plt.close(fig)
    print("  ✓ Saved 08_comprehensive_dashboard")


def plot_09_statistical_summary():
    """Generate statistical summary as a formatted table image"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')
    
    # Collect statistics
    similarity_scores = [r['similarity_score'] for r in test_results]
    skills_counts = [r['total_skills'] for r in test_results]
    session_counts = [r['total_sessions'] for r in test_results]
    path_times = [r['path_generation_time'] for r in test_results]
    quiz_times = [r['quiz_generation_time'] for r in test_results if r['quiz_generation_time'] > 0]
    quiz_counts = [r['quiz_questions_count'] for r in test_results]
    
    # Create comprehensive statistics table
    stats_data = [
        ['Metric', 'Mean', 'Std Dev', 'Min', 'Max', 'Median', 'CV (%)'],
        ['Similarity Score', 
         f'{statistics.mean(similarity_scores):.4f}',
         f'{statistics.stdev(similarity_scores):.4f}',
         f'{min(similarity_scores):.4f}',
         f'{max(similarity_scores):.4f}',
         f'{statistics.median(similarity_scores):.4f}',
         f'{(statistics.stdev(similarity_scores)/statistics.mean(similarity_scores)*100):.1f}'],
        ['Skills Generated',
         f'{statistics.mean(skills_counts):.2f}',
         f'{statistics.stdev(skills_counts):.2f}',
         f'{min(skills_counts)}',
         f'{max(skills_counts)}',
         f'{statistics.median(skills_counts):.1f}',
         f'{(statistics.stdev(skills_counts)/statistics.mean(skills_counts)*100):.1f}'],
        ['Sessions Created',
         f'{statistics.mean(session_counts):.2f}',
         f'{statistics.stdev(session_counts):.2f}',
         f'{min(session_counts)}',
         f'{max(session_counts)}',
         f'{statistics.median(session_counts):.1f}',
         f'{(statistics.stdev(session_counts)/statistics.mean(session_counts)*100):.1f}'],
        ['Path Gen Time (s)',
         f'{statistics.mean(path_times):.2f}',
         f'{statistics.stdev(path_times):.2f}',
         f'{min(path_times):.2f}',
         f'{max(path_times):.2f}',
         f'{statistics.median(path_times):.2f}',
         f'{(statistics.stdev(path_times)/statistics.mean(path_times)*100):.1f}'],
        ['Quiz Gen Time (s)',
         f'{statistics.mean(quiz_times):.2f}',
         f'{statistics.stdev(quiz_times):.2f}',
         f'{min(quiz_times):.2f}',
         f'{max(quiz_times):.2f}',
         f'{statistics.median(quiz_times):.2f}',
         f'{(statistics.stdev(quiz_times)/statistics.mean(quiz_times)*100):.1f}'],
        ['Quiz Questions',
         f'{statistics.mean(quiz_counts):.2f}',
         f'{statistics.stdev(quiz_counts):.2f}',
         f'{min(quiz_counts)}',
         f'{max(quiz_counts)}',
         f'{statistics.median(quiz_counts):.1f}',
         f'{(statistics.stdev(quiz_counts)/statistics.mean(quiz_counts)*100):.1f}' if statistics.mean(quiz_counts) > 0 else 'N/A']
    ]
    
    table = ax.table(cellText=stats_data[1:], colLabels=stats_data[0],
                    loc='center', cellLoc='center',
                    colColours=[COLORS['primary']]*7)
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2.2)
    
    # Style header
    for i in range(7):
        table[(0, i)].set_text_props(color='white', fontweight='bold')
    
    # Alternate row colors
    for i in range(1, len(stats_data)):
        for j in range(7):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#F0F0F0')
    
    ax.set_title('Comprehensive Statistical Summary of Evaluation Metrics\n(CV = Coefficient of Variation)', 
                fontsize=16, fontweight='bold', pad=30)
    
    # Add summary text below table
    total_tests = len(test_results)
    successful = sum(1 for r in test_results if r['overall_success'])
    
    summary_text = (f"Total Tests: {total_tests}  |  Successful: {successful}  |  "
                   f"Success Rate: {successful/total_tests*100:.1f}%  |  "
                   f"Total Evaluation Time: 21.3 minutes")
    
    fig.text(0.5, 0.08, summary_text, ha='center', fontsize=12, 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    save_figure(fig, '09_statistical_summary')


def plot_10_correlation_heatmap():
    """Plot correlation heatmap between metrics"""
    if not SEABORN_AVAILABLE:
        print("  ⚠ Seaborn not available, skipping correlation heatmap")
        return
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Prepare data
    data_dict = {
        'Similarity': [r['similarity_score'] for r in test_results],
        'Skills': [r['total_skills'] for r in test_results],
        'Sessions': [r['total_sessions'] for r in test_results],
        'Path Time': [r['path_generation_time'] for r in test_results],
        'Quiz Time': [r['quiz_generation_time'] for r in test_results],
        'Quiz Qs': [r['quiz_questions_count'] for r in test_results]
    }
    
    # Calculate correlation matrix
    keys = list(data_dict.keys())
    n = len(keys)
    corr_matrix = np.zeros((n, n))
    
    for i, k1 in enumerate(keys):
        for j, k2 in enumerate(keys):
            arr1 = np.array(data_dict[k1])
            arr2 = np.array(data_dict[k2])
            
            # Handle zeros
            mask = (arr1 != 0) & (arr2 != 0)
            if sum(mask) > 1:
                corr_matrix[i, j] = np.corrcoef(arr1[mask], arr2[mask])[0, 1]
            else:
                corr_matrix[i, j] = 0
    
    # Replace NaN with 0
    corr_matrix = np.nan_to_num(corr_matrix)
    
    # Create heatmap
    im = sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlBu_r',
                    xticklabels=keys, yticklabels=keys, center=0,
                    square=True, linewidths=1, cbar_kws={'shrink': 0.8},
                    annot_kws={'size': 11, 'weight': 'bold'},
                    vmin=-1, vmax=1, ax=ax)
    
    ax.set_title('Correlation Matrix of Evaluation Metrics\n(Pearson Correlation Coefficients)', 
                fontweight='bold', fontsize=14, pad=20)
    
    # Rotate labels
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right', fontsize=11)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)
    
    plt.tight_layout()
    save_figure(fig, '10_correlation_heatmap')


def plot_11_matched_occupations():
    """Plot matched occupations analysis"""
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    
    # 1. Occupation matching accuracy (sorted by similarity)
    ax1 = axes[0]
    
    sorted_results = sorted(test_results, key=lambda x: x['similarity_score'], reverse=True)
    
    goals = [r['short_name'] for r in sorted_results]
    occupations = [r['matched_occupation'][:25] + '...' if len(r['matched_occupation']) > 25 
                  else r['matched_occupation'] for r in sorted_results]
    scores = [r['similarity_score'] for r in sorted_results]
    
    y_pos = np.arange(len(goals))
    
    # Create horizontal bar chart
    colors = [COLORS['success'] if s >= 0.9 else COLORS['info'] if s >= 0.8 
             else COLORS['warning'] if s >= 0.7 else COLORS['danger'] for s in scores]
    
    bars = ax1.barh(y_pos, scores, color=colors, edgecolor='white', height=0.7)
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([f"{g} → {o}" for g, o in zip(goals, occupations)], fontsize=8)
    ax1.set_xlabel('Similarity Score', fontweight='bold')
    ax1.set_title('Goal to Occupation Matching Quality', fontweight='bold', pad=10)
    ax1.set_xlim(0, 1.1)
    
    # Add threshold regions
    ax1.axvline(x=0.9, color=COLORS['success'], linestyle='--', alpha=0.5)
    ax1.axvline(x=0.8, color=COLORS['info'], linestyle='--', alpha=0.5)
    ax1.axvline(x=0.7, color=COLORS['warning'], linestyle='--', alpha=0.5)
    
    # 2. Perfect matches vs partial matches
    ax2 = axes[1]
    
    perfect = sum(1 for r in test_results if r['similarity_score'] == 1.0)
    excellent = sum(1 for r in test_results if 0.9 <= r['similarity_score'] < 1.0)
    good = sum(1 for r in test_results if 0.8 <= r['similarity_score'] < 0.9)
    acceptable = sum(1 for r in test_results if 0.7 <= r['similarity_score'] < 0.8)
    
    categories = ['Perfect\n(1.0)', 'Excellent\n(0.9-0.99)', 'Good\n(0.8-0.89)', 'Acceptable\n(0.7-0.79)']
    counts = [perfect, excellent, good, acceptable]
    colors = [COLORS['success'], COLORS['info'], COLORS['warning'], COLORS['danger']]
    
    bars = ax2.bar(categories, counts, color=colors, edgecolor='white', width=0.6)
    
    for bar, count in zip(bars, counts):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                f'{count}\n({count/len(test_results)*100:.0f}%)', 
                ha='center', fontsize=11, fontweight='bold')
    
    ax2.set_ylabel('Number of Tests', fontweight='bold')
    ax2.set_title('Matching Quality Distribution', fontweight='bold', pad=10)
    ax2.set_ylim(0, max(counts) + 2)
    
    plt.tight_layout()
    save_figure(fig, '11_matched_occupations')


def plot_12_skills_analysis():
    """Detailed skills analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    
    # 1. Skills per goal (detailed)
    ax1 = axes[0, 0]
    names = [r['short_name'] for r in test_results]
    skills = [r['total_skills'] for r in test_results]
    similarity = [r['similarity_score'] for r in test_results]
    
    x = np.arange(len(names))
    bars = ax1.bar(x, skills, color=[plt.cm.RdYlGn(s) for s in similarity], edgecolor='white')
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax1.set_ylabel('Number of Skills', fontweight='bold')
    ax1.set_title('Skills Generated (Color = Similarity Score)', fontweight='bold', pad=10)
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=plt.Normalize(vmin=0.7, vmax=1.0))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax1, shrink=0.8)
    cbar.set_label('Similarity Score', fontweight='bold')
    
    # 2. Skills distribution histogram
    ax2 = axes[0, 1]
    ax2.hist(skills, bins=range(5, 18), color=COLORS['primary'], edgecolor='white', alpha=0.7)
    ax2.axvline(x=statistics.mean(skills), color=COLORS['danger'], linestyle='-', 
               linewidth=2.5, label=f'Mean: {statistics.mean(skills):.1f}')
    ax2.set_xlabel('Number of Skills', fontweight='bold')
    ax2.set_ylabel('Frequency', fontweight='bold')
    ax2.set_title('Skills Count Distribution', fontweight='bold', pad=10)
    ax2.legend(loc='upper left')
    
    # 3. Common skill types word cloud (simulated as bar chart)
    ax3 = axes[1, 0]
    
    # Count skill categories
    all_skills = []
    for r in test_results:
        all_skills.extend(r['skills_list'])
    
    # Categorize skills
    skill_categories = {
        'Programming': ['Python', 'JavaScript', 'Java', 'programming', 'Ruby', 'Haskell'],
        'Cloud/DevOps': ['cloud', 'DevOps', 'Kubernetes', 'Docker', 'deploy'],
        'Data': ['data', 'database', 'analytics', 'statistics'],
        'Machine Learning': ['machine learning', 'TensorFlow', 'PyTorch', 'ML'],
        'Web': ['web', 'CSS', 'JavaScript Framework', 'HTML'],
        'Research': ['research', 'scientific', 'analysis'],
        'Blockchain': ['blockchain', 'smart contract'],
        'Other': []
    }
    
    category_counts = {cat: 0 for cat in skill_categories.keys()}
    for skill in all_skills:
        matched = False
        for cat, keywords in skill_categories.items():
            if any(kw.lower() in skill.lower() for kw in keywords):
                category_counts[cat] += 1
                matched = True
                break
        if not matched:
            category_counts['Other'] += 1
    
    cats = list(category_counts.keys())
    counts = list(category_counts.values())
    
    bars = ax3.barh(cats, counts, color=COLORS['categories'][:len(cats)], edgecolor='white')
    ax3.set_xlabel('Skill Count', fontweight='bold')
    ax3.set_title('Skills by Category (Across All Tests)', fontweight='bold', pad=10)
    
    for bar, count in zip(bars, counts):
        ax3.text(count + 0.5, bar.get_y() + bar.get_height()/2, 
                str(count), va='center', fontsize=9, fontweight='bold')
    
    # 4. Skills efficiency (skills per second of generation time)
    ax4 = axes[1, 1]
    efficiency = [r['total_skills'] / r['path_generation_time'] if r['path_generation_time'] > 0 else 0 
                 for r in test_results]
    
    x = np.arange(len(names))
    colors = [COLORS['success'] if e >= 1.5 else COLORS['info'] if e >= 1.0 
             else COLORS['warning'] for e in efficiency]
    
    bars = ax4.bar(x, efficiency, color=colors, edgecolor='white')
    ax4.set_xticks(x)
    ax4.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax4.set_ylabel('Skills per Second', fontweight='bold')
    ax4.set_title('Skill Generation Efficiency', fontweight='bold', pad=10)
    
    mean_eff = statistics.mean(efficiency)
    ax4.axhline(y=mean_eff, color=COLORS['danger'], linestyle='--', 
               linewidth=2, label=f'Mean: {mean_eff:.2f}')
    ax4.legend(loc='upper right')
    
    plt.tight_layout()
    save_figure(fig, '12_skills_analysis')


def main():
    """Main function to regenerate all graphs"""
    print("\n" + "=" * 60)
    print(" REGENERATING EVALUATION GRAPHS")
    print(" Improved formatting for research publication")
    print("=" * 60 + "\n")
    
    os.makedirs(GRAPHS_DIR, exist_ok=True)
    
    print("Generating graphs...\n")
    
    plot_01_similarity_scores()
    plot_02_skills_distribution()
    plot_03_response_times()
    plot_04_success_rates()
    plot_05_category_analysis()
    plot_06_quiz_metrics()
    plot_07_session_analysis()
    plot_08_comprehensive_dashboard()
    plot_09_statistical_summary()
    plot_10_correlation_heatmap()
    plot_11_matched_occupations()
    plot_12_skills_analysis()
    
    print("\n" + "=" * 60)
    print(f" ✅ All graphs regenerated successfully!")
    print(f" Output directory: {GRAPHS_DIR}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
