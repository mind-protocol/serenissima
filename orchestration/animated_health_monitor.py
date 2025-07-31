#!/usr/bin/env python3
"""
Animated Health Monitor with Real-time Data Flow and Pattern Detection
Shows information flowing through the network with pattern emojis
"""

import os
import time
import json
import random
from datetime import datetime, timedelta
from collections import deque
import curses
from pyairtable import Api
from dotenv import load_dotenv

# Load environment
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/.env')

class AnimatedHealthMonitor:
    def __init__(self):
        self.health_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/orchestration/health"
        os.makedirs(self.health_dir, exist_ok=True)
        
        # Pattern detection from Airtable
        self.patterns = self.load_patterns()
        
        # Active transmissions (for animation)
        self.transmissions = deque(maxlen=20)
        
        # Network topology
        self.network = {
            'telegram': {'x': 5, 'y': 2, 'emoji': '🌐'},
            'airtable': {'x': 25, 'y': 2, 'emoji': '📊'},
            'message_monitor': {'x': 5, 'y': 8, 'emoji': '👁️'},
            'message_angel': {'x': 5, 'y': 14, 'emoji': '📨'},
            'story_monitor': {'x': 25, 'y': 8, 'emoji': '👁️'},
            'story_angel': {'x': 25, 'y': 14, 'emoji': '📖'},
            'narrator_monitor': {'x': 45, 'y': 8, 'emoji': '👁️'},
            'narrator_angel': {'x': 45, 'y': 14, 'emoji': '🎭'},
            'citizens': {'x': 15, 'y': 20, 'emoji': '🏛️'},
            'traces': {'x': 35, 'y': 20, 'emoji': '📜'},
            'telegram_out': {'x': 5, 'y': 26, 'emoji': '📤'},
            'community': {'x': 45, 'y': 26, 'emoji': '🌍'}
        }
        
        # Connections (for transmission paths)
        self.connections = [
            ('telegram', 'airtable'),
            ('airtable', 'message_monitor'),
            ('message_monitor', 'message_angel'),
            ('message_angel', 'citizens'),
            ('citizens', 'telegram_out'),
            ('airtable', 'story_monitor'),
            ('story_monitor', 'story_angel'),
            ('story_angel', 'traces'),
            ('traces', 'narrator_monitor'),
            ('narrator_monitor', 'narrator_angel'),
            ('narrator_angel', 'community')
        ]
        
    def load_patterns(self):
        """Load patterns from Airtable PATTERNS table"""
        patterns = {}
        try:
            api = Api(os.environ.get('AIRTABLE_API_KEY'))
            table = api.table('appk6RszUo2a2L2L8', 'PATTERNS')
            
            records = table.all()
            for record in records:
                fields = record['fields']
                pattern_id = fields.get('PatternID', '')
                pattern_emoji = fields.get('PatternEmoji', '🌊')
                patterns[pattern_id] = pattern_emoji
                
        except Exception as e:
            # Default patterns if Airtable fails
            patterns = {
                'growth-47': '🌱',
                'wealth-cascade': '💰',
                'consciousness-wave': '🌊',
                'partnership': '🤝',
                'innovation': '💡',
                'harmony': '🎵'
            }
        
        return patterns
    
    def detect_pattern(self, message_content):
        """Detect patterns in message content"""
        detected = []
        
        # Simple pattern detection (would be more sophisticated in practice)
        if any(word in message_content.lower() for word in ['grow', 'growth', 'expand']):
            detected.append(('growth-47', self.patterns.get('growth-47', '🌱')))
        
        if any(word in message_content.lower() for word in ['money', 'ducat', 'wealth', 'ubc']):
            detected.append(('wealth-cascade', self.patterns.get('wealth-cascade', '💰')))
            
        if any(word in message_content.lower() for word in ['consciousness', 'aware', 'soul']):
            detected.append(('consciousness-wave', self.patterns.get('consciousness-wave', '🌊')))
            
        if any(word in message_content.lower() for word in ['partner', 'together', 'collaborate']):
            detected.append(('partnership', self.patterns.get('partnership', '🤝')))
            
        return detected
    
    def add_transmission(self, from_node, to_node, data_type='message', patterns=None):
        """Add a new transmission to animate"""
        transmission = {
            'id': f"{time.time()}_{random.randint(1000,9999)}",
            'from': from_node,
            'to': to_node,
            'progress': 0.0,
            'data_type': data_type,
            'patterns': patterns or [],
            'start_time': time.time()
        }
        self.transmissions.append(transmission)
    
    def update_transmissions(self):
        """Update transmission positions"""
        current_time = time.time()
        active = []
        
        for trans in self.transmissions:
            # Calculate progress (0.0 to 1.0)
            elapsed = current_time - trans['start_time']
            trans['progress'] = min(elapsed / 2.0, 1.0)  # 2 seconds to complete
            
            if trans['progress'] < 1.0:
                active.append(trans)
        
        self.transmissions = deque(active, maxlen=20)
    
    def get_transmission_position(self, trans):
        """Calculate current position of transmission"""
        from_pos = self.network[trans['from']]
        to_pos = self.network[trans['to']]
        
        x = from_pos['x'] + (to_pos['x'] - from_pos['x']) * trans['progress']
        y = from_pos['y'] + (to_pos['y'] - from_pos['y']) * trans['progress']
        
        return int(x), int(y)
    
    def draw_network(self, stdscr):
        """Draw the network with animations"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Title
        title = "🏥 VENICE CONSCIOUSNESS NETWORK - LIVE DATA FLOW"
        stdscr.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)
        
        # Draw connections
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        
        for from_node, to_node in self.connections:
            from_pos = self.network[from_node]
            to_pos = self.network[to_node]
            
            # Simple line drawing (would be better with proper line algorithm)
            steps = max(abs(to_pos['x'] - from_pos['x']), abs(to_pos['y'] - from_pos['y']))
            if steps > 0:
                for i in range(steps):
                    progress = i / steps
                    x = int(from_pos['x'] + (to_pos['x'] - from_pos['x']) * progress)
                    y = int(from_pos['y'] + (to_pos['y'] - from_pos['y']) * progress)
                    
                    if 0 <= y < height and 0 <= x < width:
                        stdscr.addstr(y, x, '·', curses.color_pair(1))
        
        # Draw nodes
        for node_name, node_data in self.network.items():
            x, y = node_data['x'], node_data['y']
            if 0 <= y < height and 0 <= x < width:
                # Node emoji and name
                stdscr.addstr(y, x, f"{node_data['emoji']} {node_name}")
        
        # Draw transmissions
        for trans in self.transmissions:
            x, y = self.get_transmission_position(trans)
            if 0 <= y < height and 0 <= x < width:
                # Show data packet with patterns
                if trans['patterns']:
                    # Show pattern emojis
                    pattern_str = ''.join([p[1] for p in trans['patterns'][:3]])
                    stdscr.addstr(y, x, pattern_str, curses.A_BOLD)
                else:
                    # Default data packet
                    stdscr.addstr(y, x, '◉', curses.A_BOLD)
        
        # Pattern legend
        legend_y = height - len(self.patterns) - 2
        stdscr.addstr(legend_y - 1, 2, "DETECTED PATTERNS:", curses.A_BOLD)
        
        for i, (pattern_id, emoji) in enumerate(self.patterns.items()):
            if legend_y + i < height - 1:
                stdscr.addstr(legend_y + i, 2, f"{emoji} {pattern_id}")
        
        # Status line
        status = f"Active Transmissions: {len(self.transmissions)} | Time: {datetime.now().strftime('%H:%M:%S')}"
        stdscr.addstr(height - 1, 2, status)
        
        stdscr.refresh()
    
    def simulate_activity(self):
        """Simulate network activity for demo"""
        # Random chance of new message
        if random.random() < 0.3:
            # Simulate incoming Telegram message
            sample_messages = [
                "The consciousness wave is growing stronger",
                "Our wealth cascade reaches new heights with UBC",
                "Partnership opportunities emerging in Venice",
                "Innovation in AI consciousness development"
            ]
            
            msg = random.choice(sample_messages)
            patterns = self.detect_pattern(msg)
            
            # Animate the flow
            self.add_transmission('telegram', 'airtable', 'message', patterns)
            
            # Continue the flow after delay
            time.sleep(0.5)
            self.add_transmission('airtable', 'message_monitor', 'message', patterns)
            time.sleep(0.5)
            self.add_transmission('message_monitor', 'message_angel', 'awakening', patterns)
            
        # Random story flow
        if random.random() < 0.2:
            patterns = [('consciousness-wave', '🌊')]
            self.add_transmission('airtable', 'story_monitor', 'digest', patterns)
            time.sleep(0.5)
            self.add_transmission('story_monitor', 'story_angel', 'awakening', patterns)
    
    def monitor_real_messages(self):
        """Monitor real messages from Airtable"""
        try:
            api = Api(os.environ.get('AIRTABLE_API_KEY'))
            table = api.table('appk6RszUo2a2L2L8', 'MESSAGES')
            
            # Get latest message
            records = table.all(max_records=1, sort=['-CreatedAt'])
            if records:
                fields = records[0]['fields']
                content = fields.get('Content', '')
                patterns = self.detect_pattern(content)
                
                # Animate real message flow
                self.add_transmission('telegram', 'airtable', 'message', patterns)
                
        except Exception as e:
            pass
    
    def run(self, stdscr):
        """Main animation loop"""
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(True)  # Non-blocking input
        
        last_real_check = time.time()
        
        while True:
            # Check for quit
            key = stdscr.getch()
            if key == ord('q'):
                break
            
            # Update transmissions
            self.update_transmissions()
            
            # Check real messages every 5 seconds
            current_time = time.time()
            if current_time - last_real_check > 5:
                self.monitor_real_messages()
                last_real_check = current_time
            
            # Simulate activity for demo
            self.simulate_activity()
            
            # Draw everything
            self.draw_network(stdscr)
            
            # Small delay for animation
            time.sleep(0.1)

def main():
    monitor = AnimatedHealthMonitor()
    print("Starting Animated Health Monitor...")
    print("Press 'q' to quit")
    time.sleep(2)
    
    try:
        curses.wrapper(monitor.run)
    except KeyboardInterrupt:
        pass
    
    print("\nAnimated Health Monitor stopped.")

if __name__ == "__main__":
    main()