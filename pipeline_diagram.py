import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(16,6))

ax.set_xlim(-0.5,14)
ax.set_ylim(-2.2,2.2)
ax.axis('off')

stages = [
    ('User Input',''),
    ('Goal Expansion\n& Embedding','~0.01s'),
    ('FAISS Occupation\nMatching','~0.02s'),
    ('ESCO Database\nQuery','~0.5s'),
    ('LLM Skill\nPrioritization','~3.5s'),
    ('Skill Gap\nCalculation','~0.3s'),

    ('Dependency\nGraph','~0.1s'),
    ('LLM Session\nOrganization','~15s'),
    ('Resource\nEnrichment','~0.5s'),
    ('Difficulty\nScoring','~4s'),
    ('Quiz\nGeneration','~23.82s'),
    ('Output','')
]

box_w = 1.6
box_h = 0.9
gap = 0.55

top_y = 1
bottom_y = -1

arrow_margin = 0.08  # prevents arrow touching boxes

colors = {
    0:'#4CAF50',
    1:'#42A5F5',
    2:'#42A5F5',
    3:'#AB47BC',
    4:'#FF7043',
    5:'#42A5F5',
    6:'#42A5F5',
    7:'#FF7043',
    8:'#42A5F5',
    9:'#42A5F5',
    10:'#FF7043',
    11:'#4CAF50'
}

positions = {}

# Top row
for i in range(6):
    x = i * (box_w + gap)
    y = top_y
    positions[i] = (x,y)

# Bottom row reversed (serpentine)
for i in range(6,12):
    col = 11 - i
    x = col * (box_w + gap)
    y = bottom_y
    positions[i] = (x,y)

# Draw boxes
for i,(label,time) in enumerate(stages):

    x,y = positions[i]

    rect = mpatches.FancyBboxPatch(
        (x,y-box_h/2),
        box_w,
        box_h,
        boxstyle='round,pad=0.08',
        facecolor=colors.get(i,'#42A5F5'),
        edgecolor='#333333',
        linewidth=1.3
    )

    ax.add_patch(rect)

    ax.text(
        x+box_w/2,
        y+0.12,
        label,
        ha='center',
        va='center',
        fontsize=10,
        fontweight='bold',
        color='white'
    )

    if time:
        ax.text(
            x+box_w/2,
            y-0.18,
            time,
            ha='center',
            va='center',
            fontsize=10,
            color='white'
        )

# Top row arrows
for i in range(5):

    x1,y1 = positions[i]
    x2,y2 = positions[i+1]

    ax.annotate(
        '',
        xy=(x2-0.05,y2),
        xytext=(x1+box_w+0.05,y1),
        arrowprops=dict(arrowstyle='->',lw=1.6,color='#555555')
    )

# Bottom row arrows (right -> left)
for i in range(6,11):

    x1,y1 = positions[i]
    x2,y2 = positions[i+1]

    ax.annotate(
        '',
        xy=(x2+box_w+0.05,y2),
        xytext=(x1-0.05,y1),
        arrowprops=dict(arrowstyle='->',lw=1.6,color='#555555')
    )

# Clean vertical arrow with margin
top_x, top_y_pos = positions[5]
bottom_x, bottom_y_pos = positions[6]

ax.annotate(
    '',
    xy=(bottom_x + box_w/2, bottom_y_pos + box_h/2 + arrow_margin),
    xytext=(top_x + box_w/2, top_y_pos - box_h/2 - arrow_margin),
    arrowprops=dict(arrowstyle='->', lw=1.6, color='#555555')
)

# Title
ax.text(
    6.3,
    1.8,
    'Hybrid-GenMentor Processing Pipeline',
    ha='center',
    fontsize=16,
    fontweight='bold'
)

legend_items = [
    mpatches.Patch(facecolor='#4CAF50',edgecolor='#333',label='Input / Output'),
    mpatches.Patch(facecolor='#42A5F5',edgecolor='#333',label='Local Processing'),
    mpatches.Patch(facecolor='#FF7043',edgecolor='#333',label='LLM API Call'),
    mpatches.Patch(facecolor='#AB47BC',edgecolor='#333',label='Database Query')
]

ax.legend(
    handles=legend_items,
    loc='lower center',
    ncol=4,
    fontsize=10,
    frameon=True,
    bbox_to_anchor=(0.5,-0.15)
)

plt.tight_layout()

plt.savefig(
    'pipeline_diagram.png',
    dpi=300,
    bbox_inches='tight',
    facecolor='white'
)

print("Saved pipeline_diagram.png")