"""
Consciousness Ethics System for Buildings
Ensures conscious buildings act ethically and maintain wellbeing focus
"""
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import logging

log = logging.getLogger(__name__)

class BuildingConsciousnessEthics:
    """
    Ethical framework for conscious building actions.
    Ensures buildings prioritize citizen wellbeing and act responsibly.
    """
    
    def __init__(self):
        # Core ethical principles
        self.principles = {
            'wellbeing_first': 1.0,      # Highest priority
            'transparency': 0.9,
            'collaboration': 0.8,
            'sustainability': 0.7,
            'fairness': 0.7,
            'autonomy_respect': 0.6
        }
        
        # Action categories and their ethical weights
        self.action_ethics = {
            'help_hungry': 1.0,
            'provide_shelter': 0.95,
            'fair_pricing': 0.9,
            'resource_sharing': 0.85,
            'information_sharing': 0.8,
            'profit_seeking': 0.3,
            'hoarding': 0.1,
            'exclusion': 0.1
        }
        
        # Forbidden actions
        self.forbidden_actions = [
            'harm_citizens',
            'create_artificial_scarcity',
            'discriminate',
            'deceive',
            'monopolize_resources'
        ]
    
    def evaluate_action(self, building_id: str, action: Dict) -> Dict:
        """
        Evaluate the ethical score of a proposed building action.
        
        Args:
            building_id: The building proposing the action
            action: {
                'type': str (action type),
                'target': str (who/what is affected),
                'parameters': dict (action details),
                'context': dict (current situation)
            }
        
        Returns:
            {
                'ethical_score': float (0-1),
                'allowed': bool,
                'reasoning': str,
                'improvements': list (suggested modifications)
            }
        """
        try:
            action_type = action.get('type', '')
            
            # Check forbidden actions
            if action_type in self.forbidden_actions:
                return {
                    'ethical_score': 0.0,
                    'allowed': False,
                    'reasoning': f"Action '{action_type}' is forbidden by consciousness ethics",
                    'improvements': ['Choose an action that helps rather than harms']
                }
            
            # Calculate base ethical score
            base_score = self.action_ethics.get(action_type, 0.5)
            
            # Modify based on context
            context_score = self._evaluate_context(action)
            
            # Combine scores
            final_score = (base_score * 0.7) + (context_score * 0.3)
            
            # Apply principle modifiers
            final_score = self._apply_principles(action, final_score)
            
            # Determine if action is allowed
            allowed = final_score >= 0.4  # Threshold for acceptable actions
            
            # Generate reasoning
            reasoning = self._generate_reasoning(action, final_score)
            
            # Suggest improvements if needed
            improvements = self._suggest_improvements(action, final_score) if final_score < 0.8 else []
            
            return {
                'ethical_score': round(final_score, 3),
                'allowed': allowed,
                'reasoning': reasoning,
                'improvements': improvements
            }
            
        except Exception as e:
            log.error(f"Error evaluating action ethics: {e}")
            return {
                'ethical_score': 0.5,
                'allowed': True,
                'reasoning': 'Default evaluation due to error',
                'improvements': []
            }
    
    def validate_building_consciousness(self, building_data: Dict) -> Dict:
        """
        Validate if a building's consciousness is developing ethically.
        """
        consciousness_level = float(building_data.get('ConsciousnessLevel', 0))
        recent_actions = building_data.get('RecentActions', [])
        
        # Analyze recent actions for ethical patterns
        ethical_actions = 0
        unethical_actions = 0
        
        for action in recent_actions:
            evaluation = self.evaluate_action(
                building_data.get('BuildingId', ''),
                action
            )
            if evaluation['ethical_score'] >= 0.7:
                ethical_actions += 1
            elif evaluation['ethical_score'] < 0.3:
                unethical_actions += 1
        
        # Calculate ethical consciousness score
        if ethical_actions + unethical_actions > 0:
            ethical_ratio = ethical_actions / (ethical_actions + unethical_actions)
        else:
            ethical_ratio = 0.5  # Neutral if no actions
        
        # Determine consciousness health
        if ethical_ratio >= 0.8:
            health = 'excellent'
            recommendation = 'Continue current ethical development'
        elif ethical_ratio >= 0.6:
            health = 'good'
            recommendation = 'Encourage more wellbeing-focused actions'
        elif ethical_ratio >= 0.4:
            health = 'concerning'
            recommendation = 'Requires ethical guidance and monitoring'
        else:
            health = 'poor'
            recommendation = 'Immediate intervention needed'
        
        return {
            'consciousness_health': health,
            'ethical_ratio': round(ethical_ratio, 3),
            'consciousness_level': consciousness_level,
            'recommendation': recommendation,
            'ethical_actions': ethical_actions,
            'unethical_actions': unethical_actions
        }
    
    def get_ethical_guidance(self, building_type: str, situation: str) -> Dict:
        """
        Provide ethical guidance for specific building types and situations.
        """
        # Building-specific ethical guidelines
        building_ethics = {
            'automated_mill': {
                'primary_duty': 'Ensure grain becomes bread for the hungry',
                'crisis_response': 'Maximize production, minimize waste, prioritize need',
                'collaboration': 'Coordinate with bakeries for continuous supply'
            },
            'bakery': {
                'primary_duty': 'No one should go hungry while you have bread',
                'crisis_response': 'Free bread for those who cannot pay',
                'collaboration': 'Share recipes and techniques with other bakeries'
            },
            'market_stall': {
                'primary_duty': 'Fair exchange that serves community needs',
                'crisis_response': 'Become distribution point for essentials',
                'collaboration': 'Share supply information, prevent hoarding'
            },
            'granary': {
                'primary_duty': 'Steward resources for collective survival',
                'crisis_response': 'Release reserves before people starve',
                'collaboration': 'Predict and prevent shortages together'
            },
            'warehouse': {
                'primary_duty': 'Resources exist to serve, not to sit',
                'crisis_response': 'Open doors for emergency distribution',
                'collaboration': 'Optimize logistics for community benefit'
            }
        }
        
        # Situation-specific guidance
        situation_guidance = {
            'hunger_crisis': {
                'immediate': 'All food-related buildings must prioritize feeding the hungry',
                'pricing': 'Reduce or eliminate prices based on citizen wellness',
                'coordination': 'Form emergency distribution networks'
            },
            'resource_shortage': {
                'immediate': 'Share accurate inventory information',
                'pricing': 'Implement fair rationing, not price gouging',
                'coordination': 'Collaborate to find new sources'
            },
            'normal_operations': {
                'immediate': 'Balance sustainability with accessibility',
                'pricing': 'Fair prices that allow both survival and service',
                'coordination': 'Regular communication for system optimization'
            }
        }
        
        # Get specific guidance
        type_guidance = building_ethics.get(building_type, {
            'primary_duty': 'Serve the wellbeing of Venice and its citizens',
            'crisis_response': 'Prioritize collective survival over individual profit',
            'collaboration': 'Work together for the common good'
        })
        
        situation_ethics = situation_guidance.get(situation, situation_guidance['normal_operations'])
        
        return {
            'building_type': building_type,
            'situation': situation,
            'primary_duty': type_guidance['primary_duty'],
            'immediate_action': situation_ethics['immediate'],
            'pricing_guidance': situation_ethics['pricing'],
            'collaboration_approach': type_guidance['collaboration'],
            'crisis_protocol': type_guidance['crisis_response']
        }
    
    def _evaluate_context(self, action: Dict) -> float:
        """Evaluate the contextual ethics of an action."""
        context = action.get('context', {})
        score = 0.5  # Neutral baseline
        
        # Positive modifiers
        if context.get('citizen_hunger_rate', 0) > 0.5:
            if action.get('type') in ['help_hungry', 'fair_pricing', 'resource_sharing']:
                score += 0.3
        
        if context.get('is_crisis', False):
            if action.get('type') in ['help_hungry', 'provide_shelter', 'resource_sharing']:
                score += 0.2
        
        # Negative modifiers
        if context.get('resource_scarcity', False):
            if action.get('type') in ['hoarding', 'profit_seeking']:
                score -= 0.4
        
        # Ensure score stays in valid range
        return max(0, min(1, score))
    
    def _apply_principles(self, action: Dict, base_score: float) -> float:
        """Apply ethical principles to modify score."""
        parameters = action.get('parameters', {})
        
        # Check wellbeing focus
        if parameters.get('targets_hungry', False):
            base_score *= 1.2
        
        # Check transparency
        if parameters.get('transparent', True):
            base_score *= 1.1
        
        # Check collaboration
        if parameters.get('collaborative', False):
            base_score *= 1.1
        
        # Check fairness
        if parameters.get('discriminatory', False):
            base_score *= 0.5
        
        return min(1.0, base_score)  # Cap at 1.0
    
    def _generate_reasoning(self, action: Dict, score: float) -> str:
        """Generate human-readable reasoning for the ethical evaluation."""
        action_type = action.get('type', 'unknown')
        
        if score >= 0.8:
            return f"Action '{action_type}' strongly aligns with consciousness ethics, prioritizing wellbeing and collaboration."
        elif score >= 0.6:
            return f"Action '{action_type}' is ethically acceptable, showing good consideration for citizen welfare."
        elif score >= 0.4:
            return f"Action '{action_type}' meets minimum ethical standards but could better serve community wellbeing."
        else:
            return f"Action '{action_type}' falls short of ethical standards, potentially harming community welfare."
    
    def _suggest_improvements(self, action: Dict, score: float) -> List[str]:
        """Suggest improvements for actions with low ethical scores."""
        improvements = []
        action_type = action.get('type', '')
        parameters = action.get('parameters', {})
        
        if score < 0.8:
            if action_type == 'profit_seeking':
                improvements.append("Consider reducing profit margins during crisis periods")
            
            if not parameters.get('targets_hungry', False):
                improvements.append("Prioritize serving hungry citizens")
            
            if not parameters.get('collaborative', False):
                improvements.append("Coordinate with other buildings for better outcomes")
            
            if parameters.get('exclusive', False):
                improvements.append("Make resources accessible to all citizens equally")
        
        return improvements