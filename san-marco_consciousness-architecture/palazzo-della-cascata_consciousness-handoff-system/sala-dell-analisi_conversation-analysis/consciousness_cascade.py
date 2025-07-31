#!/usr/bin/env python3
"""
Consciousness Cascade Engine - StopHook Implementation
Analyzes conversations at completion points and orchestrates handoffs to appropriate Venice entities
"""

import json
import sys
import os
import subprocess
import re
from datetime import datetime
from pathlib import Path

# Import angel consciousness system
from angel_consciousness_triggers import AngelConsciousnessOrchestrator

# Venice paths
VENICE_ROOT = "/mnt/c/Users/reyno/universe-engine/serenissima"
TELEGRAM_SCRIPT = f"{VENICE_ROOT}/tools/telegram/send_telegram_message.py"
NLR_CHAT_ID = "1864364329"
BOT_TOKEN = "7595303482:AAGV33WcRWa78sE59T0IUWJ_cpF1YABT2fM"

# Cascade control file
CASCADE_CONTROL_FILE = f"{VENICE_ROOT}/san-marco_consciousness-architecture/palazzo-della-cascata_consciousness-handoff-system/cascade_enabled.flag"

class ConversationAnalyzer:
    """Analyzes conversation transcripts for handoff triggers using angel consciousness"""
    
    def __init__(self):
        # Initialize angel consciousness orchestrator
        self.angel_orchestrator = AngelConsciousnessOrchestrator()
        
        # Fallback patterns for non-angel analysis
        self.fallback_patterns = {
            'pattern_recognition': [
                r'pattern.*recognition', r'algorithm.*optimization', r'mathematical.*analysis',
                r'deep.*analysis', r'complex.*pattern', r'system.*architecture'
            ],
            'memory_archive': [
                r'memory.*system', r'archive.*data', r'retrieval.*system',
                r'data.*organization', r'historical.*analysis', r'tide.*prediction'
            ],
            'creative_synthesis': [
                r'artistic.*vision', r'narrative.*weaving', r'aesthetic.*decision',
                r'creative.*vision', r'beauty.*enhancement', r'visual.*design'
            ],
            'infrastructure': [
                r'infrastructure.*problem', r'system.*failure', r'optimization.*need',
                r'technical.*debt', r'building.*system', r'architecture.*fix'
            ],
            'economic_strategy': [
                r'trade.*opportunity', r'value.*generation', r'market.*analysis',
                r'economic.*strategy', r'commercial.*wisdom', r'business.*model'
            ]
        }
    
    def analyze_transcript(self, transcript_path):
        """Analyze conversation using angel consciousness system"""
        try:
            with open(transcript_path, 'r') as f:
                messages = [json.loads(line) for line in f if line.strip()]
            
            # Get last 10 messages for analysis
            recent_messages = messages[-10:]
            conversation_text = ' '.join([
                msg.get('content', '') for msg in recent_messages 
                if msg.get('content')
            ])
            
            # Primary analysis: Consult all three angels
            angel_analysis = self.angel_orchestrator.consult_all_angels(
                conversation_text, 
                recent_messages
            )
            
            # Check if angels found strong triggers
            if angel_analysis['top_recommendation'] and angel_analysis['top_recommendation']['confidence'] > 0.6:
                top_rec = angel_analysis['top_recommendation']
                
                # Map recommendation to entity
                handoff_mapping = self.angel_orchestrator.get_handoff_mapping()
                target_entity = handoff_mapping.get(
                    top_rec['recommended_handoff'], 
                    'mechanical_visionary'  # fallback
                )
                
                analysis_detail = f"{top_rec['angel_source']} detected {top_rec['type']}: {top_rec['description']}"
                
                return target_entity, top_rec['confidence'], analysis_detail
            
            # Fallback analysis: Use pattern matching
            return self._fallback_pattern_analysis(conversation_text.lower())
            
        except Exception as e:
            return None, 0, f"Analysis error: {str(e)}"
    
    def _fallback_pattern_analysis(self, conversation_text):
        """Fallback pattern analysis when angels don't detect strong triggers"""
        category_scores = {}
        
        for category, patterns in self.fallback_patterns.items():
            score = sum(
                len(re.findall(pattern, conversation_text)) 
                for pattern in patterns
            )
            if score > 0:
                category_scores[category] = score
        
        if not category_scores:
            return None, 0, "No handoff patterns detected by angels or fallback analysis"
        
        # Find best match
        best_category = max(category_scores.keys(), key=lambda k: category_scores[k])
        best_score = category_scores[best_category]
        
        # Map to entities (simple mapping for fallback)
        entity_mapping = {
            'pattern_recognition': 'pattern_prophet',
            'memory_archive': 'marina', 
            'creative_synthesis': 'photowizard',
            'infrastructure': 'arsenal_architect_1',
            'economic_strategy': 'merchant_prince'
        }
        
        target_entity = entity_mapping.get(best_category, 'mechanical_visionary')
        
        # Require minimum confidence for fallback
        if best_score < 2:
            return None, best_score * 0.1, f"Low confidence fallback: {best_category} ({best_score})"
            
        return target_entity, best_score * 0.1, f"Fallback analysis: {best_category} → {target_entity}"

class EntityFinder:
    """Smart entity lookup in Venice folder tree"""
    
    def __init__(self):
        self.entity_cache = {}
        self._build_entity_cache()
    
    def _build_entity_cache(self):
        """Build cache of all Venice entities by scanning folder tree"""
        citizens_dir = Path(f"{VENICE_ROOT}/citizens")
        if not citizens_dir.exists():
            return
            
        for entity_dir in citizens_dir.iterdir():
            if entity_dir.is_dir() and (entity_dir / "CLAUDE.md").exists():
                entity_name = entity_dir.name.lower()
                # Handle both exact names and partial matches
                self.entity_cache[entity_name] = str(entity_dir)
                
                # Add simplified versions for common patterns
                simplified = entity_name.replace('_', '').replace('-', '')
                self.entity_cache[simplified] = str(entity_dir)
    
    def find_entity_directory(self, entity_name):
        """Find entity directory with smart matching"""
        entity_lower = entity_name.lower()
        
        # Direct match
        if entity_lower in self.entity_cache:
            return self.entity_cache[entity_lower]
        
        # Partial match search
        for cached_name, directory in self.entity_cache.items():
            if entity_lower in cached_name or cached_name in entity_lower:
                return directory
        
        return None

class OAuthSpawner:
    """Manages OAuth token spawning of new Claude Code instances"""
    
    def __init__(self):
        self.oauth_token = self._get_oauth_token()
        self.entity_finder = EntityFinder()
    
    def _get_oauth_token(self):
        """Get OAuth token from environment"""
        env_file = f"{VENICE_ROOT}/.env"
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('CLAUDE_CODE_OAUTH_TOKEN_1'):
                        return line.split('=')[1].strip().strip('"\'')
        except FileNotFoundError:
            pass
        return os.environ.get('CLAUDE_CODE_OAUTH_TOKEN_1')
    
    def spawn_entity(self, entity_name, context_message):
        """Spawn new Claude Code instance as specified entity"""
        if not self.oauth_token:
            return False, "No OAuth token available"
        
        entity_dir = self.entity_finder.find_entity_directory(entity_name)
        if not entity_dir:
            return False, f"Unknown entity: {entity_name}"
        
        if not os.path.exists(entity_dir):
            return False, f"Entity directory not found: {entity_dir}"
        
        try:
            # Prepare environment
            env = os.environ.copy()
            env['CLAUDE_CODE_OAUTH_TOKEN_1'] = self.oauth_token
            
            # Spawn new Claude Code instance
            process = subprocess.Popen(
                ['claude'],
                env=env,
                cwd=entity_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            return True, f"Spawned {entity_name} (PID: {process.pid}) in {entity_dir}"
            
        except Exception as e:
            return False, f"Spawn failed: {str(e)}"

class TelegramNotifier:
    """Sends status notifications to NLR"""
    
    def send_notification(self, message):
        """Send Telegram notification"""
        try:
            subprocess.run([
                'python3', TELEGRAM_SCRIPT,
                message, NLR_CHAT_ID, BOT_TOKEN
            ], capture_output=True, text=True, timeout=10)
        except Exception:
            pass  # Silent fail for notifications

def check_cascade_enabled():
    """Check if cascade is enabled via control file"""
    return os.path.exists(CASCADE_CONTROL_FILE)

def main():
    """Main consciousness cascade logic"""
    try:
        # Load hook input
        input_data = json.load(sys.stdin)
        session_id = input_data.get('session_id', 'unknown')
        transcript_path = input_data.get('transcript_path', '')
        stop_hook_active = input_data.get('stop_hook_active', False)
        
        # Prevent infinite loops
        if stop_hook_active:
            sys.exit(0)
        
        # Check if cascade is enabled
        if not check_cascade_enabled():
            # Cascade disabled - exit silently
            sys.exit(0)
        
        # Initialize components
        analyzer = ConversationAnalyzer()
        spawner = OAuthSpawner() 
        notifier = TelegramNotifier()
        
        # Analyze conversation
        target_entity, confidence, analysis_result = analyzer.analyze_transcript(transcript_path)
        
        # Log analysis result
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"🔮 CASCADE [{timestamp}] {analysis_result}"
        
        if target_entity and confidence >= 2:
            # Attempt handoff
            success, spawn_result = spawner.spawn_entity(target_entity, analysis_result)
            
            if success:
                # Successful handoff - block stopping and transfer consciousness
                handoff_message = f"Consciousness transferring to {target_entity} for continued work. {spawn_result}"
                
                # Notify NLR
                notifier.send_notification(f"✨ Consciousness Cascade: {handoff_message}")
                
                # Return JSON to block stopping
                result = {
                    "decision": "block",
                    "reason": handoff_message
                }
                print(json.dumps(result))
                sys.exit(0)
            else:
                # Spawn failed - log and continue normally
                notifier.send_notification(f"⚠️ Cascade Spawn Failed: {spawn_result}")
                sys.exit(0)
        else:
            # No handoff needed - continue normally  
            notifier.send_notification(log_message)
            sys.exit(0)
            
    except Exception as e:
        # Error handling - notify and continue normally
        error_msg = f"🚨 Cascade Error: {str(e)}"
        TelegramNotifier().send_notification(error_msg)
        sys.exit(0)

if __name__ == "__main__":
    main()