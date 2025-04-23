import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch, Ellipse
import matplotlib.patches as patches

# Set up the figure
plt.figure(figsize=(10, 7))
plt.axis('off')
ax = plt.gca()

# Define colors
colors = {
    'background': '#f5f5f5',
    'box': '#e1f5fe',
    'box_border': '#0288d1',
    'arrow': '#0288d1',
    'text': '#01579b',
    'highlight': '#ff9800',
    'fast': '#4caf50',
    'slow': '#f44336',
    'decision': '#9c27b0',
    'resource': '#795548'
}

# Create background
ax.add_patch(Rectangle((0, 0), 10, 7, facecolor=colors['background'], edgecolor='none', zorder=0))

# Draw the main components
# Problem Complexity Scale
plt.text(5, 6.5, 'Adaptive Resource Allocation in ADSI', 
         ha='center', va='center', fontsize=16, fontweight='bold', color=colors['text'])

# Complexity Scale
scale_box = Rectangle((1, 5.5), 8, 0.5, facecolor='white', edgecolor=colors['box_border'], 
                     linewidth=2, zorder=1)
ax.add_patch(scale_box)

# Create gradient for complexity scale
gradient = np.linspace(0, 1, 100)
for i, g in enumerate(gradient):
    rect = Rectangle((1 + i*0.08, 5.5), 0.08, 0.5, 
                    facecolor=plt.cm.RdYlGn_r(g), edgecolor='none', alpha=0.7, zorder=2)
    ax.add_patch(rect)

plt.text(1, 5.75, '0', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['text'])
plt.text(9, 5.75, '1', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['text'])
plt.text(5, 6.1, 'Complexity Score (C)', ha='center', va='center', fontsize=12, fontweight='bold', color=colors['text'])

# Threshold marker
threshold_arrow = FancyArrowPatch((4, 5.2), (4, 5.5), arrowstyle='->', linewidth=2, 
                                 color=colors['decision'], connectionstyle='arc3,rad=0', zorder=3)
ax.add_patch(threshold_arrow)
plt.text(4, 5.1, 'T_complexity', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['decision'])

# Resource Allocation Formula
formula_box = Rectangle((2, 4), 6, 0.8, facecolor=colors['box'], edgecolor=colors['box_border'], 
                       linewidth=2, zorder=1)
ax.add_patch(formula_box)
plt.text(5, 4.4, 'ComputeResources = BaseResources × (1 + α × C)', 
         ha='center', va='center', fontsize=14, fontweight='bold', color=colors['text'])

# Resource Allocation Graph
# X-axis
plt.plot([1, 9], [2, 2], color=colors['text'], linewidth=2, zorder=1)
plt.text(9.2, 2, 'C', ha='left', va='center', fontsize=12, fontweight='bold', color=colors['text'])
plt.text(5, 1.7, 'Complexity Score', ha='center', va='center', fontsize=12, fontweight='bold', color=colors['text'])

# Y-axis
plt.plot([1, 1], [0.5, 3.5], color=colors['text'], linewidth=2, zorder=1)
plt.text(0.8, 3.5, 'Resources', ha='right', va='center', fontsize=12, fontweight='bold', color=colors['text'])

# Resource curve
x = np.linspace(0, 1, 100)
base = 1
alpha = 2
y = base * (1 + alpha * x)
scaled_x = 1 + 8 * x
scaled_y = 0.5 + 2.5 * (y / (base * (1 + alpha)))

plt.plot(scaled_x, scaled_y, color=colors['resource'], linewidth=3, zorder=2)

# Threshold line
plt.plot([4, 4], [0.5, 3.5], '--', color=colors['decision'], linewidth=2, alpha=0.7, zorder=1)

# Fast and Slow regions
fast_region = patches.Rectangle((1, 0.5), 3, 3, facecolor=colors['fast'], alpha=0.2, zorder=0)
slow_region = patches.Rectangle((4, 0.5), 5, 3, facecolor=colors['slow'], alpha=0.2, zorder=0)
ax.add_patch(fast_region)
ax.add_patch(slow_region)
plt.text(2.5, 3.2, 'Fast Thinking Region', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['fast'])
plt.text(6.5, 3.2, 'Slow Thinking Region', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['slow'])

# Add annotations
plt.text(2, 2.5, 'Minimal\nResources', ha='center', va='center', fontsize=10, color=colors['text'])
plt.text(8, 3, 'Maximum\nResources', ha='center', va='center', fontsize=10, color=colors['text'])

# Add explanation
explanation_box = Rectangle((1, 0.2), 8, 0.2, facecolor='white', edgecolor='none', zorder=1)
ax.add_patch(explanation_box)
plt.text(5, 0.3, 'α = Adjustment coefficient determining resource scaling rate', 
         ha='center', va='center', fontsize=10, fontweight='bold', color=colors['text'])

# Save the figure
plt.savefig('/home/ubuntu/diagrams/resource_allocation.png', dpi=150, bbox_inches='tight')
plt.close()
