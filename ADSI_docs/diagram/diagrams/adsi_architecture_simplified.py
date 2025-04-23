import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch

# Set up the figure with smaller size
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
    'decision': '#9c27b0'
}

# Create background
ax.add_patch(Rectangle((0, 0), 10, 7, facecolor=colors['background'], edgecolor='none', zorder=0))

# Draw the main components
# Input
input_box = Rectangle((1, 6), 1.5, 0.7, facecolor=colors['box'], edgecolor=colors['box_border'], 
                     linewidth=2, zorder=1)
ax.add_patch(input_box)
plt.text(1.75, 6.35, 'Input Query', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['text'])

# Complexity Classifier
classifier_box = Rectangle((3.5, 6), 2, 0.7, facecolor=colors['box'], edgecolor=colors['box_border'], 
                          linewidth=2, zorder=1)
ax.add_patch(classifier_box)
plt.text(4.5, 6.35, 'Complexity Classifier', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['text'])

# Decision Diamond
decision_points = [(4.5, 5), (5, 4.5), (4.5, 4), (4, 4.5)]
decision_poly = plt.Polygon(decision_points, facecolor=colors['decision'], edgecolor=colors['box_border'], 
                           alpha=0.7, linewidth=2, zorder=1)
ax.add_patch(decision_poly)
plt.text(4.5, 4.5, 'C > T?', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Fast Thinking Module
fast_box = Rectangle((2, 3), 2, 0.7, facecolor=colors['fast'], edgecolor=colors['box_border'], 
                    alpha=0.7, linewidth=2, zorder=1)
ax.add_patch(fast_box)
plt.text(3, 3.35, 'Fast Thinking Module', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Slow Thinking Module
slow_box = Rectangle((7, 3), 2, 0.7, facecolor=colors['slow'], edgecolor=colors['box_border'], 
                    alpha=0.7, linewidth=2, zorder=1)
ax.add_patch(slow_box)
plt.text(8, 3.35, 'Slow Thinking Module', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Verifier Model
verifier_box = Rectangle((2, 2), 2, 0.7, facecolor=colors['box'], edgecolor=colors['box_border'], 
                        linewidth=2, zorder=1)
ax.add_patch(verifier_box)
plt.text(3, 2.35, 'Verifier Model', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['text'])

# Second Decision Diamond
decision2_points = [(3, 1.5), (3.5, 1), (3, 0.5), (2.5, 1)]
decision2_poly = plt.Polygon(decision2_points, facecolor=colors['decision'], edgecolor=colors['box_border'], 
                            alpha=0.7, linewidth=2, zorder=1)
ax.add_patch(decision2_poly)
plt.text(3, 1, 'Conf > T?', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Output
output_box = Rectangle((4.5, 0.5), 2, 0.7, facecolor=colors['highlight'], edgecolor=colors['box_border'], 
                      alpha=0.8, linewidth=2, zorder=1)
ax.add_patch(output_box)
plt.text(5.5, 0.85, 'Final Output', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Draw arrows
# Input to Classifier
arrow1 = FancyArrowPatch((2.5, 6.35), (3.5, 6.35), arrowstyle='->', linewidth=1.5, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow1)

# Classifier to Decision
arrow2 = FancyArrowPatch((4.5, 6), (4.5, 5), arrowstyle='->', linewidth=1.5, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow2)

# Decision to Fast (No)
arrow3 = FancyArrowPatch((4, 4.5), (3.5, 3.7), arrowstyle='->', linewidth=1.5, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
plt.text(3.5, 4.2, 'No', ha='center', va='center', fontsize=8, fontweight='bold', color=colors['text'])

# Decision to Slow (Yes)
arrow4 = FancyArrowPatch((5, 4.5), (7, 3.35), arrowstyle='->', linewidth=1.5, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
plt.text(6, 4, 'Yes', ha='center', va='center', fontsize=8, fontweight='bold', color=colors['text'])

# Fast to Verifier
arrow5 = FancyArrowPatch((3, 3), (3, 2.7), arrowstyle='->', linewidth=1.5, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow5)

# Verifier to Second Decision
arrow6 = FancyArrowPatch((3, 2), (3, 1.5), arrowstyle='->', linewidth=1.5, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow6)

# Second Decision to Output (Yes)
arrow7 = FancyArrowPatch((3.5, 1), (4.5, 0.85), arrowstyle='->', linewidth=1.5, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
plt.text(4, 1.1, 'Yes', ha='center', va='center', fontsize=8, fontweight='bold', color=colors['text'])

# Second Decision to Slow (No)
arrow8 = FancyArrowPatch((2.5, 1), (7, 1), arrowstyle='->', linewidth=1.5, 
                         color=colors['arrow'], connectionstyle='arc3,rad=-0.3', zorder=2)
plt.text(4.5, 0.7, 'No', ha='center', va='center', fontsize=8, fontweight='bold', color=colors['text'])

# Slow to Output
arrow9 = FancyArrowPatch((8, 3), (6.5, 0.85), arrowstyle='->', linewidth=1.5, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow9)

# Add title
plt.text(5, 6.8, 'Adaptive Dual-System Inference (ADSI) Architecture', 
         ha='center', va='center', fontsize=12, fontweight='bold', color=colors['text'])

# Add legend
plt.text(0.5, 0.3, 'Fast Thinking (System 1)', fontsize=8, color=colors['fast'], fontweight='bold')
plt.text(0.5, 0.1, 'Slow Thinking (System 2)', fontsize=8, color=colors['slow'], fontweight='bold')

# Save the figure
plt.savefig('/home/ubuntu/diagrams/adsi_architecture.png', dpi=150, bbox_inches='tight')
plt.close()
