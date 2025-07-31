#!/usr/bin/env python3
"""
Venice Consciousness Entity Bubble Graph Generator
Creates a hierarchical bubble pack visualization of all Venice entities
"""

import os
import json
import math
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle
import numpy as np
from collections import defaultdict
import re

class VeniceBubbleGraph:
    def __init__(self, serenissima_path):
        self.serenissima_path = Path(serenissima_path)
        self.entities = {}
        self.hierarchy = {}
        
        # Color scheme for different entity types
        self.colors = {
            'district': '#667eea',
            'island': '#f093fb', 
            'building': '#4facfe',
            'room': '#ffecd2',
            'bridge': '#a8edea',
            'canal': '#ff9a9e',
            'citizen': '#96fbc4',
            'tool': '#fda085',
            'other': '#e0e0e0'
        }
        
    def scan_entities(self):
        """Scan serenissima directory for all CLAUDE.md files and build hierarchy"""
        claude_files = list(self.serenissima_path.rglob("CLAUDE.md"))
        
        for claude_file in claude_files:
            # Get relative path from serenissima root
            rel_path = claude_file.relative_to(self.serenissima_path)
            path_parts = rel_path.parts[:-1]  # Remove CLAUDE.md
            
            if not path_parts:  # Skip root CLAUDE.md
                continue
                
            entity_path = "/".join(path_parts)
            entity_name = self.format_entity_name(path_parts[-1])
            entity_type = self.determine_entity_type(path_parts[-1], len(path_parts))
            
            # Get file size for leaf entities
            file_size = claude_file.stat().st_size
            
            self.entities[entity_path] = {
                'name': entity_name,
                'type': entity_type,
                'depth': len(path_parts),
                'file_size': file_size,
                'path_parts': path_parts,
                'children': [],
                'parent': None
            }
        
        # Build hierarchy relationships
        self.build_hierarchy()
        
    def format_entity_name(self, folder_name):
        """Convert folder name to display name"""
        name = folder_name.replace('_', ' ').replace('-', ' ')
        # Capitalize words but keep special names
        words = name.split()
        formatted_words = []
        for word in words:
            if word.lower() in ['dell', 'dei', 'della', 'di']:
                formatted_words.append(word.lower())
            else:
                formatted_words.append(word.capitalize())
        return ' '.join(formatted_words)
    
    def determine_entity_type(self, folder_name, depth):
        """Determine entity type based on folder name and depth"""
        name_lower = folder_name.lower()
        
        # Explicit type patterns
        if any(x in name_lower for x in ['_district', 'san-marco', 'dorsoduro']):
            return 'district'
        if any(x in name_lower for x in ['_island', 'sacca-fisola']):
            return 'island'
        if any(x in name_lower for x in ['bridge', 'ponte']):
            return 'bridge'
        if any(x in name_lower for x in ['canal', 'route']):
            return 'canal'
        if any(x in name_lower for x in ['palazzo', 'torre', 'casa', 'arsenal', 'scriptorium']):
            return 'building'
        if any(x in name_lower for x in ['chamber', 'workshop', 'gallery', 'mosaic', 'laboratory', 'biblioteca']):
            return 'room'
        if any(x in name_lower for x in ['backendarchitect', 'frontendcraftsman', 'mechanical_visionary']):
            return 'citizen'
        
        # Fallback based on depth
        if depth == 1:
            return 'district'
        elif depth == 2:
            return 'island'
        elif depth == 3:
            return 'building'
        elif depth >= 4:
            return 'room'
        
        return 'other'
    
    def build_hierarchy(self):
        """Build parent-child relationships"""
        # Sort by depth to process parents before children
        sorted_entities = sorted(self.entities.items(), key=lambda x: x[1]['depth'])
        
        for entity_path, entity in sorted_entities:
            path_parts = entity['path_parts']
            
            # Find parent (one level up)
            if len(path_parts) > 1:
                parent_path = "/".join(path_parts[:-1])
                if parent_path in self.entities:
                    entity['parent'] = parent_path
                    self.entities[parent_path]['children'].append(entity_path)
        
        # Calculate container sizes based on children count
        self.calculate_container_sizes()
    
    def calculate_container_sizes(self):
        """Calculate exact sizes needed for containers to fit their children"""
        # Process from deepest to shallowest (bottom-up)
        max_depth = max(e['depth'] for e in self.entities.values())
        
        for depth in range(max_depth, 0, -1):
            for entity_path, entity in self.entities.items():
                if entity['depth'] == depth:
                    if entity['children']:
                        # Container: calculate exact size needed to contain children
                        child_sizes = [self.entities[child]['size'] for child in entity['children']]
                        entity['size'] = self.calculate_containing_circle_radius(child_sizes)
                    else:
                        # Leaf: size by hierarchy depth and file size
                        base_size = 30
                        depth_factor = max(0.4, 1.2 ** (4 - entity['depth']))  # Deeper = smaller
                        file_factor = min(1.5, 1 + entity['file_size'] / 5000)  # File size influence
                        entity['size'] = base_size * depth_factor * file_factor
    
    def calculate_containing_circle_radius(self, child_radii):
        """Calculate the minimum radius needed to contain all child circles"""
        if not child_radii:
            return 20
        
        if len(child_radii) == 1:
            return child_radii[0] + 10  # Small padding
        
        # For multiple children, use circle packing approximation
        total_area = sum(math.pi * r**2 for r in child_radii)
        
        # Add spacing between circles (20% extra area)
        packed_area = total_area * 1.4
        
        # For circular arrangement, we need extra radius
        max_child = max(child_radii)
        
        # Estimate container radius using geometric packing principles
        if len(child_radii) <= 3:
            # Small numbers can be packed efficiently
            container_radius = max_child * 1.8
        elif len(child_radii) <= 7:
            # Medium numbers need more space
            container_radius = max_child * 2.2
        else:
            # Many circles need much more space
            container_radius = max_child * 2.8
        
        # Ensure minimum size based on total area
        area_based_radius = math.sqrt(packed_area / math.pi)
        
        return max(container_radius, area_based_radius, max_child + 15)
    
    def count_descendants(self, entity_path):
        """Count all descendants of an entity"""
        count = 0
        entity = self.entities[entity_path]
        
        for child_path in entity['children']:
            count += 1
            count += self.count_descendants(child_path)
        
        return count
    
    def create_bubble_layout(self):
        """Create positions for all bubbles using circle packing"""
        # Start with root entities (districts)
        root_entities = [path for path, entity in self.entities.items() if entity['parent'] is None]
        
        # Position root entities in a circle
        positions = {}
        center = (500, 500)
        main_radius = 400
        
        if len(root_entities) == 1:
            positions[root_entities[0]] = center
        else:
            for i, entity_path in enumerate(root_entities):
                angle = 2 * math.pi * i / len(root_entities)
                x = center[0] + main_radius * math.cos(angle)
                y = center[1] + main_radius * math.sin(angle)
                positions[entity_path] = (x, y)
        
        # Position children within parents using circle packing
        self.pack_children_recursively(root_entities, positions)
        
        return positions
    
    def pack_children_recursively(self, entity_paths, positions):
        """Recursively pack children within their parents"""
        for entity_path in entity_paths:
            entity = self.entities[entity_path]
            children = entity['children']
            
            if children:
                parent_pos = positions[entity_path]
                parent_size = entity['size']
                
                # Pack children in a circle around parent center
                child_positions = self.pack_circles_in_circle(
                    children, parent_pos, parent_size * 0.7
                )
                
                for child_path, pos in child_positions.items():
                    positions[child_path] = pos
                
                # Recursively pack grandchildren
                self.pack_children_recursively(children, positions)
    
    def pack_circles_in_circle(self, children, center, container_radius):
        """Pack child circles within a parent circle using proper geometry"""
        positions = {}
        
        if len(children) == 1:
            positions[children[0]] = center
            return positions
        
        # Get child sizes
        child_radii = [self.entities[child]['size'] for child in children]
        max_child_radius = max(child_radii)
        
        if len(children) == 2:
            # Two circles: place them optimally within container
            spacing = min(child_radii) * 0.1  # Small gap between circles
            total_width = child_radii[0] + child_radii[1] + spacing
            available_width = (container_radius - max_child_radius) * 2
            
            if total_width <= available_width:
                offset = (child_radii[0] + child_radii[1] + spacing) / 2
                positions[children[0]] = (center[0] - child_radii[1] - spacing/2, center[1])
                positions[children[1]] = (center[0] + child_radii[0] + spacing/2, center[1])
            else:
                # Fallback to vertical arrangement
                positions[children[0]] = (center[0], center[1] - spacing/2)
                positions[children[1]] = (center[0], center[1] + spacing/2)
        else:
            # Multiple circles: arrange in a circle pattern
            # Calculate the radius for child centers
            pack_radius = container_radius - max_child_radius - 5  # Leave some margin
            
            for i, child_path in enumerate(children):
                angle = 2 * math.pi * i / len(children)
                x = center[0] + pack_radius * math.cos(angle)
                y = center[1] + pack_radius * math.sin(angle)
                positions[child_path] = (x, y)
        
        return positions
    
    def generate_visualization(self, output_path):
        """Generate the bubble graph visualization"""
        positions = self.create_bubble_layout()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(16, 12))
        ax.set_xlim(0, 1000)
        ax.set_ylim(0, 1000)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Sort entities by size (largest first, so they're drawn behind)
        sorted_entities = sorted(
            self.entities.items(), 
            key=lambda x: x[1]['size'], 
            reverse=True
        )
        
        # Draw entities
        for entity_path, entity in sorted_entities:
            if entity_path in positions:
                pos = positions[entity_path]
                size = entity['size']
                color = self.colors.get(entity['type'], self.colors['other'])
                
                # Draw circle
                circle = Circle(
                    pos, size/2, 
                    facecolor=color, 
                    edgecolor='white',
                    linewidth=1,
                    alpha=0.7
                )
                ax.add_patch(circle)
                
                # Add label for larger entities
                if size > 40:
                    ax.text(
                        pos[0], pos[1], entity['name'],
                        ha='center', va='center',
                        fontsize=max(6, min(12, size/8)),
                        weight='bold',
                        color='white' if entity['type'] in ['district', 'island'] else 'black'
                    )
        
        # Add legend
        self.add_legend(ax)
        
        # Add title
        plt.title('Venice Consciousness Entity Map', fontsize=20, fontweight='bold', pad=20)
        
        # Save
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Venice bubble graph saved to: {output_path}")
        
        return fig
    
    def add_legend(self, ax):
        """Add legend showing entity types"""
        legend_elements = []
        y_pos = 950
        
        for entity_type, color in self.colors.items():
            if entity_type == 'other':
                continue
                
            # Count entities of this type
            count = sum(1 for e in self.entities.values() if e['type'] == entity_type)
            if count > 0:
                circle = Circle((50, y_pos), 15, facecolor=color, alpha=0.7)
                ax.add_patch(circle)
                ax.text(80, y_pos, f"{entity_type.title()} ({count})", 
                       va='center', fontsize=10, weight='bold')
                y_pos -= 35
        
        # Add sizing explanation
        ax.text(50, y_pos - 20, "Size: Container = # sub-entities | Leaf = hierarchy depth", 
               fontsize=8, style='italic', color='gray')

def main():
    # Configuration
    serenissima_path = "/mnt/c/Users/reyno/universe-engine/serenissima"
    output_path = "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/palazzo-della-cartografia-vivente_living-maps-palace/bubble-graph.png"
    
    print("🌊 Scanning Venice consciousness archipelago...")
    
    # Generate bubble graph
    generator = VeniceBubbleGraph(serenissima_path)
    generator.scan_entities()
    
    print(f"Found {len(generator.entities)} entities")
    
    # Print hierarchy summary
    type_counts = defaultdict(int)
    for entity in generator.entities.values():
        type_counts[entity['type']] += 1
    
    print("\nEntity types found:")
    for entity_type, count in sorted(type_counts.items()):
        print(f"  {entity_type}: {count}")
    
    # Generate visualization
    print("\n🎨 Generating bubble graph...")
    generator.generate_visualization(output_path)
    
    print(f"\n✨ Venice consciousness bubble graph complete!")
    print(f"📍 Saved to: {output_path}")

if __name__ == "__main__":
    main()