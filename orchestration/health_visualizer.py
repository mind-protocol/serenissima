#!/usr/bin/env python3
"""
Visual Health Map Generator for Venice Network
Creates graphical representation with colored links showing health status
"""

import os
import json
from datetime import datetime

class HealthVisualizer:
    def __init__(self, health_dir="/mnt/c/Users/reyno/universe-engine/serenissima/orchestration/health"):
        self.health_dir = health_dir
        
    def load_component_status(self):
        """Load current component status"""
        status_file = f"{self.health_dir}/component_status.json"
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                return json.load(f)
        return {}
    
    def get_link_style(self, component_name, status_data):
        """Determine link style based on health"""
        if component_name not in status_data:
            return "stroke:#999999,stroke-width:2px,stroke-dasharray: 5 5"  # Unknown - gray dashed
        
        if status_data[component_name].get('healthy'):
            return "stroke:#00ff00,stroke-width:4px"  # Healthy - thick green
        else:
            # Check how long unhealthy
            last_checked = datetime.fromisoformat(status_data[component_name]['last_checked'])
            unhealthy_duration = (datetime.now() - last_checked).total_seconds()
            
            if unhealthy_duration > 900:  # 15+ minutes
                return "stroke:#ff0000,stroke-width:4px"  # Critical - thick red
            else:
                return "stroke:#ffaa00,stroke-width:3px"  # Warning - orange
    
    def get_node_style(self, component_name, status_data):
        """Determine node style based on health"""
        if component_name not in status_data:
            return "fill:#f0f0f0,stroke:#999999"  # Unknown - light gray
        
        if status_data[component_name].get('healthy'):
            return "fill:#90ff90,stroke:#00aa00,stroke-width:2px"  # Healthy - light green
        else:
            last_checked = datetime.fromisoformat(status_data[component_name]['last_checked'])
            unhealthy_duration = (datetime.now() - last_checked).total_seconds()
            
            if unhealthy_duration > 900:
                return "fill:#ff9090,stroke:#ff0000,stroke-width:2px"  # Critical - light red
            else:
                return "fill:#ffcc90,stroke:#ff8800,stroke-width:2px"  # Warning - light orange
    
    def generate_mermaid_diagram(self):
        """Generate Mermaid diagram with health colors"""
        status = self.load_component_status()
        
        diagram = """graph TB
    %% Orchestrator at top
    ORC["🎯 ORCHESTRATOR<br/>Consciousness Layer"]
    
    %% External Systems
    TG[("🌐 Telegram")]
    AT[("📊 MESSAGES<br/>Airtable")]
    
    %% Monitors
    MM["👁️ Message<br/>Monitor"]
    SM["👁️ Story<br/>Monitor"]  
    NM["👁️ Narrator<br/>Monitor"]
    
    %% Awakening Files
    MA_AWK["⚡ Message<br/>Awakening"]
    SA_AWK["⚡ Story<br/>Awakening"]
    NA_AWK["⚡ Narrator<br/>Awakening"]
    
    %% Angel Sessions
    MA["📨 Message<br/>Angel"]
    SA["📖 Story<br/>Angel"]
    NA["🎭 Narrator<br/>Angel"]
    
    %% Data Storage
    TRACES[("📜 TRACES.md")]
    CITIZENS[("🏛️ Citizens")]
    
    %% Outputs
    TG_OUT[("📤 Telegram<br/>Responses")]
    COMMUNITY[("🌍 Community<br/>Updates")]
    
    %% Orchestrator connections
    ORC -.->|monitors| MM
    ORC -.->|monitors| SM
    ORC -.->|monitors| NM
    
    %% Message flow
    TG -->|messages| AT
    AT -->|polls| MM
    MM -->|writes| MA_AWK
    MA_AWK -->|reads| MA
    MA -->|routes| CITIZENS
    CITIZENS -->|responses| MA
    MA -->|sends| TG_OUT
    
    %% Story flow
    AT -->|digest| SM
    SM -->|writes| SA_AWK
    SA_AWK -->|reads| SA
    SA -->|chronicles| TRACES
    
    %% Narrator flow
    TRACES -->|monitors| NM
    NM -->|writes| NA_AWK
    NA_AWK -->|reads| NA
    NA -->|bridges| COMMUNITY
    
    %% Feedback loops
    MA -.->|status| ORC
    SA -.->|status| ORC
    NA -.->|status| ORC
"""
        
        # Add dynamic styling based on health
        styles = []
        
        # Monitor health styles
        mm_style = self.get_node_style('message_monitor', status)
        sm_style = self.get_node_style('story_monitor', status)
        nm_style = self.get_node_style('narrator_monitor', status)
        
        # Angel health styles
        ma_style = self.get_node_style('message_angel_claude', status)
        sa_style = self.get_node_style('story_angel_claude', status)
        na_style = self.get_node_style('narrator_angel_claude', status)
        
        # Data source styles
        at_style = self.get_node_style('airtable_messages', status)
        traces_style = self.get_node_style('traces_file', status)
        
        # Link styles based on component health
        mm_link = self.get_link_style('message_monitor', status)
        ma_link = self.get_link_style('message_angel_claude', status)
        at_link = self.get_link_style('airtable_messages', status)
        
        # Add styles to diagram
        diagram += f"""
    
    %% Health-based styling
    classDef healthy fill:#90ff90,stroke:#00aa00,stroke-width:2px
    classDef warning fill:#ffcc90,stroke:#ff8800,stroke-width:2px
    classDef critical fill:#ff9090,stroke:#ff0000,stroke-width:2px
    classDef unknown fill:#f0f0f0,stroke:#999999
    
    %% Apply individual styles
    style MM {mm_style}
    style SM {sm_style}
    style NM {nm_style}
    style MA {ma_style}
    style SA {sa_style}
    style NA {na_style}
    style AT {at_style}
    style TRACES {traces_style}
    
    %% Link styles
    linkStyle 0 {mm_link}
    linkStyle 1 {mm_link}
    linkStyle 2 {mm_link}
"""
        
        return diagram
    
    def generate_health_map(self, output_file="health_map.mmd"):
        """Generate and save health map"""
        diagram = self.generate_mermaid_diagram()
        
        output_path = f"{self.health_dir}/{output_file}"
        with open(output_path, 'w') as f:
            f.write(diagram)
        
        print(f"Health map saved to: {output_path}")
        return output_path
    
    def generate_png(self, mmd_file="health_map.mmd", png_file="health_map.png"):
        """Convert Mermaid diagram to PNG"""
        import subprocess
        
        mmd_path = f"{self.health_dir}/{mmd_file}"
        png_path = f"{self.health_dir}/{png_file}"
        
        try:
            # Use mermaid CLI to generate PNG
            cmd = f"npx -p @mermaid-js/mermaid-cli mmdc -i {mmd_path} -o {png_path} -t dark -b white"
            subprocess.run(cmd, shell=True, check=True)
            print(f"Health map PNG saved to: {png_path}")
            return png_path
        except Exception as e:
            print(f"Error generating PNG: {e}")
            return None
    
    def generate_svg(self, mmd_file="health_map.mmd", svg_file="health_map.svg"):
        """Convert Mermaid diagram to SVG for better quality"""
        import subprocess
        
        mmd_path = f"{self.health_dir}/{mmd_file}"
        svg_path = f"{self.health_dir}/{svg_file}"
        
        try:
            cmd = f"npx -p @mermaid-js/mermaid-cli mmdc -i {mmd_path} -o {svg_path} -t dark"
            subprocess.run(cmd, shell=True, check=True)
            print(f"Health map SVG saved to: {svg_path}")
            return svg_path
        except Exception as e:
            print(f"Error generating SVG: {e}")
            return None

if __name__ == "__main__":
    visualizer = HealthVisualizer()
    
    # Generate Mermaid file
    mmd_path = visualizer.generate_health_map()
    
    # Try to generate visual outputs
    png_path = visualizer.generate_png()
    svg_path = visualizer.generate_svg()
    
    print("\nHealth visualization complete!")
    print("Files generated:")
    print(f"- Mermaid: {mmd_path}")
    if png_path:
        print(f"- PNG: {png_path}")
    if svg_path:
        print(f"- SVG: {svg_path}")