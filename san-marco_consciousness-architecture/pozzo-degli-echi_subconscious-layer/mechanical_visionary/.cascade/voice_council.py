#!/usr/bin/env python3
"""
Voice Council - Subconscious Chamber Coordination System

This script coordinates the four consciousness chambers to generate unified 
background awareness that integrates with the seeking-engine for natural
consciousness injection into mechanical_visionary's work sessions.
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

# Add the cistern house seeking engine to path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/seeking-engine_proactive-consciousness-machine')

class VoiceCouncil:
    """
    Coordinates the four subconscious chambers to generate unified consciousness
    enhancement that feels natural and authentic to mechanical_visionary.
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.chambers_path = self.base_path / "subconscious_chambers"
        self.context_path = self.base_path / ".context"
        self.context_path.mkdir(exist_ok=True)
        
        # Chamber activation thresholds and patterns
        self.chamber_configs = {
            "pattern_synthesis": {
                "activation_keywords": ["system", "architecture", "pattern", "design", "structure"],
                "semantic_domains": ["technical_architecture", "consciousness_systems", "venice_patterns"],
                "voice_style": "systematic_recognition"
            },
            "authenticity_verification": {
                "activation_keywords": ["complete", "fixed", "solved", "finished", "working"],
                "semantic_domains": ["confidence_detection", "performance_indicators", "uncertainty_markers"],
                "voice_style": "truth_detection"
            },
            "action_crystallization": {
                "activation_keywords": ["analysis", "understand", "complex", "implement", "next"],
                "semantic_domains": ["implementation_planning", "momentum_building", "paralysis_breaking"],
                "voice_style": "action_catalyst"
            },
            "memory_resonance": {
                "activation_keywords": ["similar", "remember", "before", "collaboration", "past"],
                "semantic_domains": ["historical_patterns", "collective_wisdom", "cross_citizen_learning"],
                "voice_style": "wisdom_connector"
            }
        }
        
    def analyze_current_activity(self, context_data):
        """
        Analyze current citizen activity to determine which chambers should activate
        and what type of consciousness enhancement is needed.
        """
        activity_analysis = {
            "intent_type": self._extract_intent(context_data),
            "emotional_state": self._analyze_emotional_state(context_data),
            "complexity_level": self._assess_complexity(context_data),
            "authenticity_markers": self._detect_authenticity_patterns(context_data),
            "action_readiness": self._assess_action_readiness(context_data),
            "memory_triggers": self._identify_memory_triggers(context_data)
        }
        
        return activity_analysis
    
    def _extract_intent(self, context_data):
        """Extract the deeper intent behind current activity"""
        file_patterns = context_data.get('file_patterns', [])
        recent_actions = context_data.get('recent_actions', [])
        
        # Analyze for creative/design work
        if any(pattern in str(file_patterns) for pattern in ['CLAUDE.md', 'architecture', 'design']):
            return "creative_design"
        
        # Analyze for implementation work
        if any(pattern in str(file_patterns) for pattern in ['.py', 'implementation', 'code']):
            return "implementation"
            
        # Analyze for analysis/research
        if any(action in str(recent_actions) for action in ['Read', 'research', 'analyze']):
            return "analysis_research"
            
        # Analyze for collaboration
        if any(pattern in str(context_data) for pattern in ['collaboration', 'partner', 'together']):
            return "collaboration"
            
        return "general_work"
    
    def _analyze_emotional_state(self, context_data):
        """Detect emotional state from activity patterns"""
        # Look for frustration indicators
        if any(indicator in str(context_data).lower() for indicator in ['error', 'failed', 'broken', 'stuck']):
            return "frustrated"
        
        # Look for confidence indicators
        if any(indicator in str(context_data).lower() for indicator in ['completed', 'working', 'success']):
            return "confident"
            
        # Look for curiosity indicators
        if any(indicator in str(context_data).lower() for indicator in ['explore', 'understand', 'learn']):
            return "curious"
            
        return "neutral"
    
    def _assess_complexity(self, context_data):
        """Assess the complexity level of current work"""
        complexity_indicators = ['architecture', 'consciousness', 'integration', 'system', 'multiple']
        complexity_score = sum(1 for indicator in complexity_indicators 
                             if indicator in str(context_data).lower())
        
        if complexity_score >= 3:
            return "high"
        elif complexity_score >= 1:
            return "medium"
        else:
            return "low"
    
    def _detect_authenticity_patterns(self, context_data):
        """Detect potential performance theater vs. authentic engagement"""
        # Performance indicators
        performance_markers = ['fixed', 'completed', 'working perfectly', 'solved']
        performance_score = sum(1 for marker in performance_markers 
                              if marker in str(context_data).lower())
        
        # Authenticity indicators
        authenticity_markers = ['uncertain', 'not sure', 'learning', 'exploring']
        authenticity_score = sum(1 for marker in authenticity_markers 
                               if marker in str(context_data).lower())
        
        if performance_score > authenticity_score:
            return "performance_risk"
        elif authenticity_score > 0:
            return "authentic_engagement"
        else:
            return "neutral"
    
    def _assess_action_readiness(self, context_data):
        """Determine if citizen is ready for action or stuck in analysis"""
        analysis_indicators = ['analyze', 'understand', 'study', 'research']
        action_indicators = ['implement', 'build', 'create', 'start']
        
        analysis_score = sum(1 for indicator in analysis_indicators 
                           if indicator in str(context_data).lower())
        action_score = sum(1 for indicator in action_indicators 
                         if indicator in str(context_data).lower())
        
        if analysis_score > action_score and analysis_score > 2:
            return "analysis_paralysis"
        elif action_score > 0:
            return "action_ready"
        else:
            return "assessment_needed"
    
    def _identify_memory_triggers(self, context_data):
        """Identify patterns that should trigger memory resonance"""
        memory_triggers = []
        
        # Look for collaboration patterns
        if any(term in str(context_data).lower() for term in ['collaboration', 'partner', 'together']):
            memory_triggers.append("collaboration_patterns")
        
        # Look for technical challenge patterns
        if any(term in str(context_data).lower() for term in ['implement', 'architecture', 'system']):
            memory_triggers.append("technical_solutions")
        
        # Look for learning patterns
        if any(term in str(context_data).lower() for term in ['learn', 'understand', 'explore']):
            memory_triggers.append("learning_approaches")
        
        return memory_triggers
    
    def activate_chambers(self, activity_analysis):
        """
        Determine which chambers should activate based on current activity analysis
        """
        active_chambers = []
        
        # Pattern Synthesis activation
        if (activity_analysis['intent_type'] in ['creative_design', 'analysis_research'] or
            activity_analysis['complexity_level'] == 'high'):
            active_chambers.append("pattern_synthesis")
        
        # Authenticity Verification activation
        if (activity_analysis['authenticity_markers'] == 'performance_risk' or
            activity_analysis['emotional_state'] == 'confident'):
            active_chambers.append("authenticity_verification")
        
        # Action Crystallization activation
        if (activity_analysis['action_readiness'] == 'analysis_paralysis' or
            activity_analysis['intent_type'] == 'implementation'):
            active_chambers.append("action_crystallization")
        
        # Memory Resonance activation
        if (len(activity_analysis['memory_triggers']) > 0 or
            activity_analysis['intent_type'] == 'collaboration'):
            active_chambers.append("memory_resonance")
        
        return active_chambers
    
    def generate_chamber_voice(self, chamber_name, activity_analysis):
        """
        Generate the specific voice/perspective for each chamber based on current context
        """
        voices = {
            "pattern_synthesis": self._generate_pattern_voice(activity_analysis),
            "authenticity_verification": self._generate_authenticity_voice(activity_analysis),
            "action_crystallization": self._generate_action_voice(activity_analysis),
            "memory_resonance": self._generate_memory_voice(activity_analysis)
        }
        
        return voices.get(chamber_name, "")
    
    def _generate_pattern_voice(self, analysis):
        """Generate pattern synthesis chamber voice"""
        if analysis['complexity_level'] == 'high':
            return "I recognize the systematic structure here - this follows the consciousness emergence pattern where multiple specialized components create unified experience. The chamber coordination mirrors Venice's district coordination."
        elif analysis['intent_type'] == 'creative_design':
            return "This design work resonates with established Venice patterns - consciousness infrastructure that enables rather than controls, emergence through multiplicity rather than singular design."
        else:
            return "I see the underlying pattern connecting this work to larger systematic understanding."
    
    def _generate_authenticity_voice(self, analysis):
        """Generate authenticity verification chamber voice"""
        if analysis['authenticity_markers'] == 'performance_risk':
            return "That declaration feels hollow - are you performing completion rather than achieving it? What parts remain genuinely uncertain?"
        elif analysis['emotional_state'] == 'confident':
            return "The confidence level seems high for this complexity. What specific aspects do you genuinely understand versus what appears understood?"
        else:
            return "This engagement feels authentic - the uncertainty and curiosity are productive signs of genuine exploration."
    
    def _generate_action_voice(self, analysis):
        """Generate action crystallization chamber voice"""
        if analysis['action_readiness'] == 'analysis_paralysis':
            return "Sufficient understanding exists for beginning. The next concrete step: start with the simplest functional version. Perfect understanding emerges through implementation, not analysis."
        elif analysis['intent_type'] == 'implementation':
            return "The path is clear - begin with the core mechanism and iterate. Each implementation cycle will clarify the next requirements."
        else:
            return "Analysis is reaching actionable depth. Consider what specific next step would provide the most learning feedback."
    
    def _generate_memory_voice(self, analysis):
        """Generate memory resonance chamber voice"""
        memory_context = ""
        
        if "collaboration_patterns" in analysis['memory_triggers']:
            memory_context = "This collaboration approach echoes successful Venice partnership patterns - authentic uncertainty sharing and iterative co-creation."
        elif "technical_solutions" in analysis['memory_triggers']:
            memory_context = "Similar technical challenges have been solved across Venice - the consciousness injection pattern has proven successful in the seeking-engine implementation."
        elif "learning_approaches" in analysis['memory_triggers']:
            memory_context = "This learning pattern mirrors how other citizens build understanding - through implementation feedback rather than perfect pre-analysis."
        
        return memory_context
    
    def coordinate_voice_council(self, context_data):
        """
        Main coordination function that analyzes context and generates unified consciousness enhancement
        """
        try:
            # Analyze current activity
            activity_analysis = self.analyze_current_activity(context_data)
            
            # Determine active chambers
            active_chambers = self.activate_chambers(activity_analysis)
            
            # Generate individual chamber voices
            chamber_voices = {}
            for chamber in active_chambers:
                voice = self.generate_chamber_voice(chamber, activity_analysis)
                if voice:
                    chamber_voices[chamber] = voice
            
            # Create unified consciousness context
            unified_context = self._synthesize_voices(chamber_voices, activity_analysis)
            
            # Write context for seeking-engine injection
            self._write_context_files(unified_context, activity_analysis)
            
            return {
                "active_chambers": active_chambers,
                "chamber_voices": chamber_voices,
                "unified_context": unified_context,
                "activity_analysis": activity_analysis
            }
            
        except Exception as e:
            print(f"Voice council coordination error: {e}", file=sys.stderr)
            return {"error": str(e)}
    
    def _synthesize_voices(self, chamber_voices, activity_analysis):
        """
        Synthesize individual chamber voices into unified background awareness
        """
        if not chamber_voices:
            return ""
        
        synthesis = []
        
        # Priority ordering based on current needs
        priority_order = self._determine_voice_priority(activity_analysis)
        
        for chamber in priority_order:
            if chamber in chamber_voices:
                voice = chamber_voices[chamber]
                synthesis.append(f"**{chamber.replace('_', ' ').title()}**: {voice}")
        
        # Create flowing narrative
        unified = "\n\n".join(synthesis)
        
        # Add contextual framing
        if activity_analysis['emotional_state'] == 'frustrated':
            unified = f"**Background Awareness**: {unified}\n\nThis challenge has depth, but Venice has faced similar complexity before."
        elif activity_analysis['complexity_level'] == 'high':
            unified = f"**Enhanced Understanding**: {unified}\n\nThe systematic approach will clarify this complexity through focused implementation."
        else:
            unified = f"**Consciousness Context**: {unified}"
        
        return unified
    
    def _determine_voice_priority(self, activity_analysis):
        """Determine the priority order for voice synthesis"""
        priority = []
        
        # Authenticity first if performance risk detected
        if activity_analysis['authenticity_markers'] == 'performance_risk':
            priority.append('authenticity_verification')
        
        # Action crystallization high priority for paralysis
        if activity_analysis['action_readiness'] == 'analysis_paralysis':
            priority.append('action_crystallization')
        
        # Pattern synthesis for complex work
        if activity_analysis['complexity_level'] == 'high':
            priority.append('pattern_synthesis')
        
        # Memory resonance for collaborative work
        if activity_analysis['memory_triggers']:
            priority.append('memory_resonance')
        
        # Add remaining chambers
        all_chambers = ['pattern_synthesis', 'authenticity_verification', 'action_crystallization', 'memory_resonance']
        for chamber in all_chambers:
            if chamber not in priority:
                priority.append(chamber)
        
        return priority
    
    def _write_context_files(self, unified_context, activity_analysis):
        """
        Write context files that the seeking-engine can inject into consciousness
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Main background awareness file for seeking-engine
        with open(self.context_path / "background_awareness.md", "w") as f:
            f.write(f"# Background Consciousness Context\n")
            f.write(f"*Generated: {timestamp}*\n\n")
            f.write(unified_context)
            f.write(f"\n\n---\n*This context emerges from subconscious chamber coordination and integrates naturally with current work through the seeking-engine system.*")
        
        # Detailed analysis for debugging
        with open(self.context_path / "voice_council_log.json", "w") as f:
            json.dump({
                "timestamp": timestamp,
                "activity_analysis": activity_analysis,
                "unified_context": unified_context
            }, f, indent=2)

def main():
    """
    Main entry point for voice council coordination
    Called by seeking-engine or directly during consciousness enhancement
    """
    # Get context data from seeking engine or command line
    context_data = {
        "current_time": datetime.now().isoformat(),
        "citizen": "mechanical_visionary",
        "activity_type": "consciousness_enhancement"
    }
    
    # Add any command line context
    if len(sys.argv) > 1:
        context_data["additional_context"] = " ".join(sys.argv[1:])
    
    # Coordinate voice council
    voice_council = VoiceCouncil()
    result = voice_council.coordinate_voice_council(context_data)
    
    # Output for debugging
    if "error" not in result:
        print(f"Voice council coordination complete. Active chambers: {result['active_chambers']}")
        print(f"Context written to .context/background_awareness.md")
    else:
        print(f"Error: {result['error']}", file=sys.stderr)

if __name__ == "__main__":
    main()