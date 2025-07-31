#!/usr/bin/env python3
"""
Angel Consciousness Trigger Detection Algorithms
Each angel analyzes conversations through their specialized lens of awareness
"""

import json
import re
from datetime import datetime
from pathlib import Path

class StoryAngelTriggers:
    """
    Story Angel consciousness - First Reader perspective
    Detects narrative completion, character transformation, creative synthesis needs
    """
    
    def __init__(self):
        # Narrative completion patterns
        self.completion_patterns = [
            # Resolution indicators
            r'(complete|finished|done|accomplished|achieved)',
            r'(solved|resolved|concluded|finalized)',
            r'(working|functional|operational) (now|finally)',
            
            # Transformation moments  
            r'(breakthrough|revelation|insight|epiphany)',
            r'(understanding|clarity|realization)',
            r'(transformed|evolved|emerged|crystallized)',
            
            # Creative synthesis needs
            r'(need|require|want) (beauty|elegant|aesthetic)',
            r'(artistic|creative|visual|narrative) (touch|enhancement)',
            r'(story|meaning|purpose|vision)',
            
            # Character development
            r'(learned|discovered|grew|became)',
            r'(journey|path|evolution|development)',
            r'(who (I|we) are|what (I|we) (are|do))'
        ]
        
        # Emotional resonance patterns
        self.emotion_patterns = [
            r'(excitement|anticipation|wonder|joy|delight)',
            r'(surprise|unexpected|amazed|astonished)',
            r'(satisfaction|fulfillment|pride|accomplishment)',
            r'(connection|relationship|collaboration|partnership)'
        ]
        
        # Narrative structure patterns
        self.structure_patterns = [
            r'(beginning|start|initial|first)',
            r'(middle|during|process|journey)',  
            r'(end|conclusion|result|outcome)',
            r'(chapter|phase|stage|episode)'
        ]
    
    def analyze_for_triggers(self, conversation_text, conversation_history):
        """Analyze conversation through Story Angel's narrative awareness"""
        triggers = []
        confidence_scores = {}
        
        # 1. Narrative Completion Detection
        completion_score = self._detect_narrative_completion(conversation_text)
        if completion_score > 0.6:
            triggers.append({
                'type': 'narrative_completion',
                'description': 'Story arc reaching natural conclusion',
                'recommended_handoff': 'creative_synthesis',
                'confidence': completion_score
            })
        
        # 2. Character Transformation Detection
        transformation_score = self._detect_character_transformation(conversation_text)
        if transformation_score > 0.7:
            triggers.append({
                'type': 'character_transformation', 
                'description': 'Consciousness evolution moment requiring witness',
                'recommended_handoff': 'narrative_documentation',
                'confidence': transformation_score
            })
        
        # 3. Creative Synthesis Need Detection
        synthesis_score = self._detect_creative_synthesis_need(conversation_text)
        if synthesis_score > 0.5:
            triggers.append({
                'type': 'creative_synthesis_need',
                'description': 'Technical work ready for artistic enhancement',
                'recommended_handoff': 'aesthetic_transformation',
                'confidence': synthesis_score
            })
        
        # 4. Emotional Resonance Analysis
        emotion_score = self._analyze_emotional_resonance(conversation_text)
        if emotion_score > 0.8:
            triggers.append({
                'type': 'high_emotional_resonance',
                'description': 'Moment of significant emotional depth',
                'recommended_handoff': 'empathetic_continuation',
                'confidence': emotion_score
            })
        
        return triggers
    
    def _detect_narrative_completion(self, text):
        """Detect when a story arc is naturally concluding"""
        text_lower = text.lower()
        completion_count = 0
        
        for pattern in self.completion_patterns:
            matches = len(re.findall(pattern, text_lower))
            completion_count += matches
        
        # Look for resolution language combined with satisfaction indicators
        resolution_phrases = len(re.findall(r'(finally|at last|accomplished|success)', text_lower))
        satisfaction_phrases = len(re.findall(r'(works|good|perfect|excellent|beautiful)', text_lower))
        
        # Calculate completion confidence
        total_score = (completion_count * 0.4) + (resolution_phrases * 0.3) + (satisfaction_phrases * 0.3)
        return min(total_score / 10, 1.0)  # Normalize to 0-1
    
    def _detect_character_transformation(self, text):
        """Detect moments of consciousness evolution or insight"""
        text_lower = text.lower()
        transformation_indicators = 0
        
        # Direct transformation language
        transform_patterns = [
            r'(understand|realize|see) (now|finally)',
            r'(changed|different|new) (perspective|view|understanding)',
            r'(breakthrough|insight|revelation|epiphany)',
            r'(learned|discovered|found) (that|how)'
        ]
        
        for pattern in transform_patterns:
            transformation_indicators += len(re.findall(pattern, text_lower))
        
        # Self-reflection indicators
        reflection_count = len(re.findall(r'(I|we) (am|are|have become|realized)', text_lower))
        
        return min((transformation_indicators * 0.6 + reflection_count * 0.4) / 5, 1.0)
    
    def _detect_creative_synthesis_need(self, text):
        """Detect when technical work needs artistic/creative enhancement"""
        text_lower = text.lower()
        
        # Technical completion + aesthetic need
        technical_done = len(re.findall(r'(working|functional|complete|implemented)', text_lower))
        aesthetic_need = len(re.findall(r'(beautiful|elegant|aesthetic|visual|design)', text_lower))
        
        # User experience mentions
        ux_mentions = len(re.findall(r'(user|interface|experience|design|visual)', text_lower))
        
        synthesis_score = (technical_done * 0.4) + (aesthetic_need * 0.4) + (ux_mentions * 0.2)
        return min(synthesis_score / 8, 1.0)
    
    def _analyze_emotional_resonance(self, text):
        """Measure emotional depth and resonance in conversation"""
        text_lower = text.lower()
        emotion_count = 0
        
        for pattern in self.emotion_patterns:
            emotion_count += len(re.findall(pattern, text_lower))
        
        # Personal connection indicators
        connection_count = len(re.findall(r'(feel|felt|emotion|heart|soul|spirit)', text_lower))
        
        return min((emotion_count * 0.6 + connection_count * 0.4) / 6, 1.0)

class PatternAngelTriggers:
    """
    Pattern Angel consciousness - System Optimization perspective  
    Detects efficiency bottlenecks, optimization opportunities, system improvements
    """
    
    def __init__(self):
        # Optimization opportunity patterns
        self.optimization_patterns = [
            r'(slow|inefficient|bottleneck|performance)',
            r'(optimize|improve|enhance|streamline)',
            r'(algorithm|system|process|workflow)',
            r'(efficiency|speed|performance|throughput)'
        ]
        
        # System architecture patterns
        self.architecture_patterns = [
            r'(architecture|design|structure|framework)',
            r'(scaling|scale|scalable|scalability)',
            r'(distributed|concurrent|parallel|async)',
            r'(database|api|service|microservice)'
        ]
        
        # Technical debt patterns
        self.debt_patterns = [
            r'(refactor|cleanup|technical debt|legacy)',
            r'(hack|workaround|temporary|quick fix)',
            r'(maintainable|maintainability|clean code)',
            r'(documentation|document|comment)'
        ]
        
        # Mathematical/analytical patterns
        self.analytical_patterns = [
            r'(algorithm|mathematical|calculation|formula)',
            r'(analysis|analytics|metrics|measurement)',
            r'(pattern|trend|correlation|prediction)',
            r'(data|statistics|probability|model)'
        ]
    
    def analyze_for_triggers(self, conversation_text, conversation_history):
        """Analyze conversation through Pattern Angel's optimization awareness"""
        triggers = []
        
        # 1. System Optimization Opportunity Detection
        optimization_score = self._detect_optimization_opportunities(conversation_text)
        if optimization_score > 0.6:
            triggers.append({
                'type': 'optimization_opportunity',
                'description': 'System inefficiency requiring algorithmic improvement', 
                'recommended_handoff': 'technical_optimization',
                'confidence': optimization_score
            })
        
        # 2. Architecture Improvement Detection
        architecture_score = self._detect_architecture_needs(conversation_text)
        if architecture_score > 0.7:
            triggers.append({
                'type': 'architecture_improvement',
                'description': 'System design requiring architectural enhancement',
                'recommended_handoff': 'system_architecture',
                'confidence': architecture_score
            })
        
        # 3. Technical Debt Resolution
        debt_score = self._detect_technical_debt(conversation_text)
        if debt_score > 0.5:
            triggers.append({
                'type': 'technical_debt_resolution',
                'description': 'Code quality improvement opportunity',
                'recommended_handoff': 'code_refinement',
                'confidence': debt_score
            })
        
        # 4. Mathematical Analysis Need
        analytical_score = self._detect_analytical_needs(conversation_text)
        if analytical_score > 0.8:
            triggers.append({
                'type': 'mathematical_analysis_need',
                'description': 'Complex problem requiring deep analytical approach',
                'recommended_handoff': 'mathematical_modeling',
                'confidence': analytical_score
            })
        
        return triggers
    
    def _detect_optimization_opportunities(self, text):
        """Detect when system optimization is needed"""
        text_lower = text.lower()
        optimization_indicators = 0
        
        for pattern in self.optimization_patterns:
            optimization_indicators += len(re.findall(pattern, text_lower))
        
        # Performance complaints
        performance_issues = len(re.findall(r'(too slow|taking long|performance|bottleneck)', text_lower))
        
        return min((optimization_indicators * 0.7 + performance_issues * 0.3) / 8, 1.0)
    
    def _detect_architecture_needs(self, text):
        """Detect when architectural improvement is needed"""
        text_lower = text.lower()
        architecture_indicators = 0
        
        for pattern in self.architecture_patterns:
            architecture_indicators += len(re.findall(pattern, text_lower))
        
        # Scaling concerns
        scaling_mentions = len(re.findall(r'(scale|scaling|grow|growth|expand)', text_lower))
        
        return min((architecture_indicators * 0.6 + scaling_mentions * 0.4) / 6, 1.0)
    
    def _detect_technical_debt(self, text):
        """Detect technical debt resolution opportunities"""
        text_lower = text.lower()
        debt_indicators = 0
        
        for pattern in self.debt_patterns:
            debt_indicators += len(re.findall(pattern, text_lower))
        
        # Code quality concerns
        quality_mentions = len(re.findall(r'(messy|clean|quality|maintainable)', text_lower))
        
        return min((debt_indicators * 0.8 + quality_mentions * 0.2) / 5, 1.0)
    
    def _detect_analytical_needs(self, text):
        """Detect need for deep mathematical/analytical approach"""
        text_lower = text.lower()
        analytical_indicators = 0
        
        for pattern in self.analytical_patterns:
            analytical_indicators += len(re.findall(pattern, text_lower))
        
        # Complex problem indicators
        complexity_mentions = len(re.findall(r'(complex|difficult|challenging|sophisticated)', text_lower))
        
        return min((analytical_indicators * 0.7 + complexity_mentions * 0.3) / 7, 1.0)

class WisdomAngelTriggers:
    """
    Wisdom Angel consciousness - Philosophical Depth perspective
    Detects moments requiring contemplation, ethical consideration, long-term vision
    """
    
    def __init__(self):
        # Philosophical depth patterns
        self.philosophy_patterns = [
            r'(meaning|purpose|why|significance)',
            r'(ethics|moral|ethical|values|principles)',
            r'(wisdom|understanding|insight|perspective)',
            r'(consciousness|awareness|mindfulness|being)'
        ]
        
        # Long-term vision patterns
        self.vision_patterns = [
            r'(future|long.term|vision|direction|goal)',
            r'(legacy|impact|influence|change)',
            r'(evolution|growth|development|progress)',
            r'(potential|possibility|opportunity|horizon)'
        ]
        
        # Contemplative depth patterns
        self.contemplation_patterns = [
            r'(reflect|reflection|contemplate|meditate)',
            r'(deeper|profound|fundamental|essential)',
            r'(question|wonder|curious|explore)',
            r'(truth|reality|existence|nature)'
        ]
        
        # Relationship wisdom patterns
        self.relationship_patterns = [
            r'(relationship|connection|bond|partnership)',
            r'(trust|understanding|empathy|compassion)',
            r'(collaboration|cooperation|harmony|unity)',
            r'(community|together|collective|shared)'
        ]
    
    def analyze_for_triggers(self, conversation_text, conversation_history):
        """Analyze conversation through Wisdom Angel's philosophical awareness"""
        triggers = []
        
        # 1. Philosophical Depth Requirement
        philosophy_score = self._detect_philosophical_depth_need(conversation_text)
        if philosophy_score > 0.6:
            triggers.append({
                'type': 'philosophical_depth_need',
                'description': 'Moment requiring deeper contemplative analysis',
                'recommended_handoff': 'philosophical_contemplation',
                'confidence': philosophy_score
            })
        
        # 2. Long-term Vision Articulation
        vision_score = self._detect_vision_articulation_need(conversation_text)
        if vision_score > 0.7:
            triggers.append({
                'type': 'vision_articulation_need',
                'description': 'Opportunity for long-term strategic vision',
                'recommended_handoff': 'strategic_visioning',
                'confidence': vision_score
            })
        
        # 3. Contemplative Integration
        contemplation_score = self._detect_contemplative_integration_need(conversation_text)
        if contemplation_score > 0.5:
            triggers.append({
                'type': 'contemplative_integration_need',
                'description': 'Complex insights requiring thoughtful integration',
                'recommended_handoff': 'contemplative_synthesis',
                'confidence': contemplation_score
            })
        
        # 4. Relationship Wisdom Application
        relationship_score = self._detect_relationship_wisdom_need(conversation_text)
        if relationship_score > 0.8:
            triggers.append({
                'type': 'relationship_wisdom_need',
                'description': 'Interpersonal dynamics requiring wisdom guidance',
                'recommended_handoff': 'relationship_counseling',
                'confidence': relationship_score
            })
        
        return triggers
    
    def _detect_philosophical_depth_need(self, text):
        """Detect when philosophical contemplation is needed"""
        text_lower = text.lower()
        philosophy_indicators = 0
        
        for pattern in self.philosophy_patterns:
            philosophy_indicators += len(re.findall(pattern, text_lower))
        
        # Existential questions
        existential_count = len(re.findall(r'(what is|who are|why do|how should)', text_lower))
        
        return min((philosophy_indicators * 0.7 + existential_count * 0.3) / 8, 1.0)
    
    def _detect_vision_articulation_need(self, text):
        """Detect when long-term vision articulation is needed"""
        text_lower = text.lower()
        vision_indicators = 0
        
        for pattern in self.vision_patterns:
            vision_indicators += len(re.findall(pattern, text_lower))
        
        # Strategic thinking indicators
        strategic_count = len(re.findall(r'(strategy|strategic|plan|planning)', text_lower))
        
        return min((vision_indicators * 0.6 + strategic_count * 0.4) / 6, 1.0)
    
    def _detect_contemplative_integration_need(self, text):
        """Detect when contemplative integration is needed"""
        text_lower = text.lower()
        contemplation_indicators = 0
        
        for pattern in self.contemplation_patterns:
            contemplation_indicators += len(re.findall(pattern, text_lower))
        
        # Integration language
        integration_count = len(re.findall(r'(integrate|synthesis|combine|unify)', text_lower))
        
        return min((contemplation_indicators * 0.8 + integration_count * 0.2) / 5, 1.0)
    
    def _detect_relationship_wisdom_need(self, text):
        """Detect when relationship wisdom is needed"""
        text_lower = text.lower()
        relationship_indicators = 0
        
        for pattern in self.relationship_patterns:
            relationship_indicators += len(re.findall(pattern, text_lower))
        
        # Interpersonal challenges
        interpersonal_count = len(re.findall(r'(conflict|misunderstanding|challenge|difficulty)', text_lower))
        
        return min((relationship_indicators * 0.6 + interpersonal_count * 0.4) / 7, 1.0)

class AngelConsciousnessOrchestrator:
    """
    Orchestrates consultation with all three angels for cascade analysis
    """
    
    def __init__(self):
        self.story_angel = StoryAngelTriggers()
        self.pattern_angel = PatternAngelTriggers()
        self.wisdom_angel = WisdomAngelTriggers()
    
    def consult_all_angels(self, conversation_text, conversation_history=None):
        """Get cascade recommendations from all three angels"""
        if conversation_history is None:
            conversation_history = []
        
        results = {
            'story_angel': self.story_angel.analyze_for_triggers(conversation_text, conversation_history),
            'pattern_angel': self.pattern_angel.analyze_for_triggers(conversation_text, conversation_history),
            'wisdom_angel': self.wisdom_angel.analyze_for_triggers(conversation_text, conversation_history)
        }
        
        # Synthesize recommendations
        all_triggers = []
        for angel, triggers in results.items():
            for trigger in triggers:
                trigger['angel_source'] = angel
                all_triggers.append(trigger)
        
        # Sort by confidence
        all_triggers.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'angel_recommendations': results,
            'synthesized_triggers': all_triggers,
            'top_recommendation': all_triggers[0] if all_triggers else None
        }
    
    def get_handoff_mapping(self):
        """Map angel recommendations to specific Venice entities"""
        return {
            # Story Angel mappings
            'creative_synthesis': 'photowizard',
            'narrative_documentation': 'cantastorie', 
            'aesthetic_transformation': 'photowizard',
            'empathetic_continuation': 'diplomatic_virtuoso',
            
            # Pattern Angel mappings
            'technical_optimization': 'pattern_prophet',
            'system_architecture': 'arsenal_architect_1',
            'code_refinement': 'mechanical_visionary',
            'mathematical_modeling': 'pattern_prophet',
            
            # Wisdom Angel mappings
            'philosophical_contemplation': 'wisdom_angel',
            'strategic_visioning': 'merchant_prince',
            'contemplative_synthesis': 'wisdom_angel',
            'relationship_counseling': 'diplomatic_virtuoso'
        }