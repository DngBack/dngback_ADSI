import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch, Ellipse
from matplotlib.path import Path
import matplotlib.patches as patches

# Set up the figure
plt.figure(figsize=(14, 10))
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
    'decision': '#9c27b0'
}

# Create background
ax.add_patch(Rectangle((0, 0), 14, 10, facecolor=colors['background'], edgecolor='none', zorder=0))

# Draw the main components
# Input
input_box = Rectangle((1, 8), 2, 1, facecolor=colors['box'], edgecolor=colors['box_border'], 
                     linewidth=2, zorder=1)
ax.add_patch(input_box)
plt.text(2, 8.5, 'Input Query', ha='center', va='center', fontsize=12, fontweight='bold', color=colors['text'])

# Complexity Classifier
classifier_box = Rectangle((4, 8), 3, 1, facecolor=colors['box'], edgecolor=colors['box_border'], 
                          linewidth=2, zorder=1)
ax.add_patch(classifier_box)
plt.text(5.5, 8.5, 'Complexity Classifier', ha='center', va='center', fontsize=12, fontweight='bold', color=colors['text'])

# Decision Diamond
decision_points = [(5.5, 7), (6, 6.5), (5.5, 6), (5, 6.5)]
decision_poly = plt.Polygon(decision_points, facecolor=colors['decision'], edgecolor=colors['box_border'], 
                           alpha=0.7, linewidth=2, zorder=1)
ax.add_patch(decision_poly)
plt.text(5.5, 6.5, 'C > T?', ha='center', va='center', fontsize=12, fontweight='bold', color='white')

# Fast Thinking Module
fast_box = Rectangle((2, 5), 2.5, 1, facecolor=colors['fast'], edgecolor=colors['box_border'], 
                    alpha=0.7, linewidth=2, zorder=1)
ax.add_patch(fast_box)
plt.text(3.25, 5.5, 'Fast Thinking\nModule', ha='center', va='center', fontsize=12, fontweight='bold', color='white')

# Slow Thinking Module
slow_box = Rectangle((8, 5), 2.5, 1, facecolor=colors['slow'], edgecolor=colors['box_border'], 
                    alpha=0.7, linewidth=2, zorder=1)
ax.add_patch(slow_box)
plt.text(9.25, 5.5, 'Slow Thinking\nModule', ha='center', va='center', fontsize=12, fontweight='bold', color='white')

# Verifier Model
verifier_box = Rectangle((2, 3.5), 2.5, 1, facecolor=colors['box'], edgecolor=colors['box_border'], 
                        linewidth=2, zorder=1)
ax.add_patch(verifier_box)
plt.text(3.25, 4, 'Verifier Model', ha='center', va='center', fontsize=12, fontweight='bold', color=colors['text'])

# Second Decision Diamond
decision2_points = [(3.25, 2.5), (3.75, 2), (3.25, 1.5), (2.75, 2)]
decision2_poly = plt.Polygon(decision2_points, facecolor=colors['decision'], edgecolor=colors['box_border'], 
                            alpha=0.7, linewidth=2, zorder=1)
ax.add_patch(decision2_poly)
plt.text(3.25, 2, 'Conf > T?', ha='center', va='center', fontsize=12, fontweight='bold', color='white')

# Output
output_box = Rectangle((5.5, 0.5), 3, 1, facecolor=colors['highlight'], edgecolor=colors['box_border'], 
                      alpha=0.8, linewidth=2, zorder=1)
ax.add_patch(output_box)
plt.text(7, 1, 'Final Output', ha='center', va='center', fontsize=12, fontweight='bold', color='white')

# Draw arrows
# Input to Classifier
arrow1 = FancyArrowPatch((3, 8.5), (4, 8.5), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow1)

# Classifier to Decision
arrow2 = FancyArrowPatch((5.5, 8), (5.5, 7), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow2)

# Decision to Fast (No)
arrow3 = FancyArrowPatch((5, 6.5), (4.5, 5.5), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
plt.text(4.5, 6, 'No', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['text'])

# Decision to Slow (Yes)
arrow4 = FancyArrowPatch((6, 6.5), (8, 5.5), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
plt.text(7, 6, 'Yes', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['text'])

# Fast to Verifier
arrow5 = FancyArrowPatch((3.25, 5), (3.25, 4.5), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow5)

# Verifier to Second Decision
arrow6 = FancyArrowPatch((3.25, 3.5), (3.25, 2.5), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow6)

# Second Decision to Output (Yes)
arrow7 = FancyArrowPatch((3.75, 2), (5.5, 1), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
plt.text(4.5, 1.7, 'Yes', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['text'])

# Second Decision to Slow (No)
arrow8 = FancyArrowPatch((3.25, 1.5), (8, 1.5), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=-0.3', zorder=2)
plt.text(5.5, 1.2, 'No', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['text'])

# Slow to Output
arrow9 = FancyArrowPatch((9.25, 5), (7, 1.5), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow9)

# Add title
plt.text(7, 9.5, 'Adaptive Dual-System Inference (ADSI) Architecture', 
         ha='center', va='center', fontsize=16, fontweight='bold', color=colors['text'])

# Add legend
legend_elements = [
    patches.Patch(facecolor=colors['fast'], alpha=0.7, label='Fast Thinking (System 1)'),
    patches.Patch(facecolor=colors['slow'], alpha=0.7, label='Slow Thinking (System 2)'),
    patches.Patch(facecolor=colors['decision'], alpha=0.7, label='Decision Points'),
    patches.Patch(facecolor=colors['highlight'], alpha=0.8, label='Output')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

# Save the figure
plt.tight_layout()
plt.savefig('/home/ubuntu/diagrams/adsi_architecture.png', dpi=300, bbox_inches='tight')
plt.close()
