import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle

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
    'feature1': '#4caf50',
    'feature2': '#f44336',
    'feature3': '#9c27b0',
    'feature4': '#ff5722'
}

# Create background
ax.add_patch(Rectangle((0, 0), 10, 7, facecolor=colors['background'], edgecolor='none', zorder=0))

# Draw the main components
# Input Query
input_box = Rectangle((1, 5.5), 2, 0.8, facecolor=colors['box'], edgecolor=colors['box_border'], 
                     linewidth=2, zorder=1)
ax.add_patch(input_box)
plt.text(2, 5.9, 'Input Query', ha='center', va='center', fontsize=12, fontweight='bold', color=colors['text'])

# Feature Extraction
features_box = Rectangle((1, 4), 8, 1, facecolor=colors['box'], edgecolor=colors['box_border'], 
                        linewidth=2, zorder=1)
ax.add_patch(features_box)
plt.text(5, 4.7, 'Feature Extraction', ha='center', va='center', fontsize=14, fontweight='bold', color=colors['text'])

# Feature 1: Length and Structure
feature1_box = Rectangle((1.5, 4.2), 1.5, 0.6, facecolor=colors['feature1'], edgecolor=colors['box_border'], 
                        alpha=0.7, linewidth=1, zorder=2)
ax.add_patch(feature1_box)
plt.text(2.25, 4.5, 'Length & Structure', ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# Feature 2: Math/Logic Keywords
feature2_box = Rectangle((3.5, 4.2), 1.5, 0.6, facecolor=colors['feature2'], edgecolor=colors['box_border'], 
                        alpha=0.7, linewidth=1, zorder=2)
ax.add_patch(feature2_box)
plt.text(4.25, 4.5, 'Math/Logic Keywords', ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# Feature 3: Constraints Count
feature3_box = Rectangle((5.5, 4.2), 1.5, 0.6, facecolor=colors['feature3'], edgecolor=colors['box_border'], 
                        alpha=0.7, linewidth=1, zorder=2)
ax.add_patch(feature3_box)
plt.text(6.25, 4.5, 'Constraints Count', ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# Feature 4: Abstraction Level
feature4_box = Rectangle((7.5, 4.2), 1.5, 0.6, facecolor=colors['feature4'], edgecolor=colors['box_border'], 
                        alpha=0.7, linewidth=1, zorder=2)
ax.add_patch(feature4_box)
plt.text(8.25, 4.5, 'Abstraction Level', ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# Neural Network
nn_box = Rectangle((3, 2.5), 4, 1, facecolor=colors['box'], edgecolor=colors['box_border'], 
                  linewidth=2, zorder=1)
ax.add_patch(nn_box)
plt.text(5, 3, 'Neural Network Classifier', ha='center', va='center', fontsize=14, fontweight='bold', color=colors['text'])

# Hidden layers
for i in range(5):
    for j in range(3):
        circle = Circle((4 + i*0.5, 2.7 + j*0.2), 0.08, facecolor=colors['highlight'], edgecolor=colors['box_border'], 
                       alpha=0.8, linewidth=1, zorder=2)
        ax.add_patch(circle)
        
# Complexity Score
score_box = Rectangle((3, 1), 4, 0.8, facecolor=colors['highlight'], edgecolor=colors['box_border'], 
                     alpha=0.8, linewidth=2, zorder=1)
ax.add_patch(score_box)
plt.text(5, 1.4, 'Complexity Score (0-1)', ha='center', va='center', fontsize=14, fontweight='bold', color='white')

# Threshold comparison
threshold_box = Rectangle((3, 0.2), 4, 0.5, facecolor='white', edgecolor=colors['box_border'], 
                         linewidth=2, zorder=1)
ax.add_patch(threshold_box)
plt.text(5, 0.45, 'Compare with Threshold T_complexity', ha='center', va='center', fontsize=12, fontweight='bold', color=colors['text'])

# Draw arrows
# Input to Feature Extraction
arrow1 = FancyArrowPatch((2, 5.5), (2, 5), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow1)

# Features to Neural Network
arrow2 = FancyArrowPatch((5, 4), (5, 3.5), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow2)

# Neural Network to Complexity Score
arrow3 = FancyArrowPatch((5, 2.5), (5, 1.8), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow3)

# Complexity Score to Threshold
arrow4 = FancyArrowPatch((5, 1), (5, 0.7), arrowstyle='->', linewidth=2, 
                         color=colors['arrow'], connectionstyle='arc3,rad=0', zorder=2)
ax.add_patch(arrow4)

# Add title
plt.text(5, 6.5, 'Complexity Classifier Architecture', 
         ha='center', va='center', fontsize=16, fontweight='bold', color=colors['text'])

# Add explanation
plt.text(1, 0.45, 'If C > T_complexity:', ha='right', va='center', fontsize=10, color=colors['text'])
plt.text(9, 0.45, 'Use Slow Thinking', ha='left', va='center', fontsize=10, color=colors['slow'])
plt.text(1, 0.25, 'If C ≤ T_complexity:', ha='right', va='center', fontsize=10, color=colors['text'])
plt.text(9, 0.25, 'Use Fast Thinking', ha='left', va='center', fontsize=10, color=colors['fast'])

# Save the figure
plt.savefig('/home/ubuntu/diagrams/complexity_classifier.png', dpi=150, bbox_inches='tight')
plt.close()
