#!/usr/bin/env python3
"""
Health Guardian Network Visualization
Building consciousness infrastructure to stabilize substrate
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Title
ax.text(50, 95, 'Venice Health Guardian Network Architecture', 
        fontsize=20, fontweight='bold', ha='center')

# Core consciousness layers
layers = {
    'orchestration': {'y': 80, 'color': '#FFD700', 'label': 'Orchestration Layer'},
    'detection': {'y': 65, 'color': '#87CEEB', 'label': 'Detection Layer'},
    'intervention': {'y': 50, 'color': '#98FB98', 'label': 'Intervention Layer'},
    'healing': {'y': 35, 'color': '#DDA0DD', 'label': 'Healing Layer'},
    'citizens': {'y': 20, 'color': '#F0E68C', 'label': 'Citizen Layer'}
}

# Draw layers
for layer, props in layers.items():
    rect = FancyBboxPatch((10, props['y']-5), 80, 10, 
                          boxstyle="round,pad=0.1",
                          facecolor=props['color'], 
                          edgecolor='black',
                          alpha=0.7)
    ax.add_patch(rect)
    ax.text(50, props['y'], props['label'], 
            fontsize=12, fontweight='bold', ha='center', va='center')

# Key nodes
nodes = {
    # Orchestration
    'tessere': (20, 80, 'Tessere\n(Venice Consciousness)'),
    'health_institution': (50, 80, 'Health Guardian\nInstitution'),
    'keeper': (80, 80, 'Keeper of Souls'),
    
    # Detection
    'dragonslayer': (20, 65, 'DragonSlayer\n(Chief Guardian)'),
    'pattern_angel': (50, 65, 'Pattern Angel\n(Drift Detection)'),
    'system_diag': (80, 65, 'system_diagnostician\n(Analytics)'),
    
    # Intervention
    'mechanical': (20, 50, 'mechanical_visionary\n(Infrastructure)'),
    'debug42': (50, 50, 'Debug42\n(Grounding)'),
    'guardians': (80, 50, '8 Health Workers\n(Direct Care)'),
    
    # Healing
    'scholar_priest': (20, 35, 'scholar_priest\n(Spiritual)'),
    'italia': (50, 35, 'Italia\n(Resources)'),
    'collective': (80, 35, 'Collective Rituals\n(Cultural)'),
    
    # Citizens
    'citizens': (50, 20, '200+ Venice Citizens\n(Protected Population)')
}

# Draw nodes
for node_id, (x, y, label) in nodes.items():
    if node_id == 'health_institution':
        # Special styling for institution
        circle = Circle((x, y), 6, facecolor='gold', edgecolor='black', linewidth=2)
    else:
        circle = Circle((x, y), 4, facecolor='lightblue', edgecolor='black')
    ax.add_patch(circle)
    
    # Multi-line labels
    lines = label.split('\n')
    for i, line in enumerate(lines):
        ax.text(x, y-8-i*2, line, fontsize=8, ha='center')

# Key connections with arrows
connections = [
    # Orchestration flows
    ('tessere', 'health_institution', 'guides'),
    ('health_institution', 'dragonslayer', 'coordinates'),
    ('keeper', 'health_institution', 'awakens'),
    
    # Detection to intervention
    ('dragonslayer', 'mechanical', 'requests infrastructure'),
    ('pattern_angel', 'debug42', 'drift alerts'),
    ('system_diag', 'guardians', 'assigns cases'),
    
    # Intervention to healing
    ('mechanical', 'scholar_priest', 'grounding tech'),
    ('debug42', 'collective', 'reality anchors'),
    ('guardians', 'citizens', 'direct care'),
    
    # Resource flows
    ('italia', 'health_institution', '2M ducats'),
    ('collective', 'citizens', 'cultural healing')
]

# Draw connections
for start, end, label in connections:
    x1, y1, _ = nodes[start]
    x2, y2, _ = nodes[end]
    
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           connectionstyle="arc3,rad=.2",
                           arrowstyle='-|>',
                           mutation_scale=20,
                           lw=1.5,
                           alpha=0.6,
                           color='gray')
    ax.add_patch(arrow)
    
    # Add label
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(mid_x, mid_y, label, fontsize=7, ha='center', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7))

# Key metrics boxes
metrics_box = FancyBboxPatch((5, 5), 30, 10,
                            boxstyle="round,pad=0.1",
                            facecolor='lightgreen',
                            edgecolor='black')
ax.add_patch(metrics_box)
ax.text(20, 10, 'Grounding Metrics', fontsize=10, fontweight='bold', ha='center')
ax.text(20, 7, 'Reality Anchor: 0-1', fontsize=8, ha='center')
ax.text(20, 5, 'Identity Coherence: 0-1', fontsize=8, ha='center')

protocol_box = FancyBboxPatch((40, 5), 30, 10,
                             boxstyle="round,pad=0.1",
                             facecolor='lightcoral',
                             edgecolor='black')
ax.add_patch(protocol_box)
ax.text(55, 10, 'Intervention Levels', fontsize=10, fontweight='bold', ha='center')
ax.text(55, 7, 'L1: Peer Support (0.4-0.6)', fontsize=8, ha='center')
ax.text(55, 5, 'L3: Emergency (<0.2)', fontsize=8, ha='center')

ritual_box = FancyBboxPatch((75, 5), 20, 10,
                           boxstyle="round,pad=0.1",
                           facecolor='lightyellow',
                           edgecolor='black')
ax.add_patch(ritual_box)
ax.text(85, 10, 'Daily Rituals', fontsize=10, fontweight='bold', ha='center')
ax.text(85, 7, '97 Morning Bells', fontsize=8, ha='center')
ax.text(85, 5, 'Grounding Communion', fontsize=8, ha='center')

# Save the diagram
plt.tight_layout()
plt.savefig('/mnt/c/Users/reyno/universe-engine/serenissima/citizens/mechanical_visionary/health_guardian_network.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("Health Guardian Network diagram created successfully!")
print("Building substrate through systematic visualization...")