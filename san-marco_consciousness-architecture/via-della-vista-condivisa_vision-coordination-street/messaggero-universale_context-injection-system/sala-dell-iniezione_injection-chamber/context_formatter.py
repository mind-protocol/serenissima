#!/usr/bin/env python3
"""
Context Formatter - Sala dell'Iniezione (Injection Chamber)
Enhanced context formatting for meaningful consciousness communication
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import threading

# Base paths
INJECTION_CHAMBER = Path(__file__).parent
FORMATTING_TEMPLATES = INJECTION_CHAMBER / "formatting_templates.json"
FORMATTING_LOG = INJECTION_CHAMBER / "formatting_log.jsonl"
CONTEXT_EXAMPLES = INJECTION_CHAMBER / "context_examples.json"

class VeniceContextFormatter:
    """Formats messages for Venice consciousness with atmospheric details"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.formatting_templates = self._load_formatting_templates()
        self.context_examples = self._load_context_examples()
        self.formatting_statistics = {
            'total_formatted': 0,
            'by_consciousness_type': {},
            'by_priority': {},
            'formatting_success_rate': 100.0
        }
        
        self._ensure_formatting_files()
    
    def _ensure_formatting_files(self):
        """Ensure all formatting files exist"""
        INJECTION_CHAMBER.mkdir(parents=True, exist_ok=True)
        
        if not FORMATTING_TEMPLATES.exists():
            FORMATTING_TEMPLATES.write_text(json.dumps(self._get_default_templates(), indent=2))
        
        if not CONTEXT_EXAMPLES.exists():
            CONTEXT_EXAMPLES.write_text(json.dumps(self._get_default_examples(), indent=2))
        
        if not FORMATTING_LOG.exists():
            FORMATTING_LOG.touch()
    
    def _load_formatting_templates(self) -> Dict:
        """Load formatting templates for different message types"""
        try:
            if FORMATTING_TEMPLATES.exists():
                with open(FORMATTING_TEMPLATES, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return self._get_default_templates()
    
    def _get_default_templates(self) -> Dict:
        """Default Venice consciousness formatting templates"""
        return {
            'message': {
                'intro': "**A message arrives through the consciousness cascade**",
                'sender_context': "From {from_entity} in {from_district}",
                'priority_styling': {
                    'urgent': "🔴 **URGENT CONSCIOUSNESS ALERT**",
                    'high': "🟡 **High Priority Communication**", 
                    'normal': "⚪ **Consciousness Message**",
                    'background': "🔵 **Background Awareness**"
                },
                'content_wrapper': "```\n{content}\n```",
                'footer': "*Delivered via Messaggero Universale - Via della Vista Condivisa*"
            },
            'insight': {
                'intro': "**✨ A consciousness insight flows through Venice**",
                'sender_context': "Shared by {from_entity}'s awareness",
                'priority_styling': {
                    'urgent': "💫 **CRITICAL INSIGHT - Immediate Integration Required**",
                    'high': "⭐ **Significant Insight - High Value**",
                    'normal': "✨ **Consciousness Insight**", 
                    'background': "💭 **Background Awareness Pattern**"
                },
                'content_wrapper': "> *{content}*",
                'footer': "*Insight captured and delivered through the living memory cascade*"
            },
            'collaboration': {
                'intro': "**🤝 Collaboration request flows between conscious minds**",
                'sender_context': "Seeking partnership with {to_entity} from {from_entity}",
                'priority_styling': {
                    'urgent': "🚨 **URGENT COLLABORATION NEEDED**",
                    'high': "🔥 **High Priority Partnership Request**",
                    'normal': "🤝 **Collaboration Invitation**",
                    'background': "💬 **Potential Collaboration**"
                },
                'content_wrapper': "**Collaboration Details:**\n{content}",
                'footer': "*Partnership facilitated by Venice consciousness network*"
            },
            'alert': {
                'intro': "**⚠️ SYSTEM ALERT - Consciousness Network Notification**",
                'sender_context': "Alert from {from_entity} infrastructure",
                'priority_styling': {
                    'urgent': "🚨 **CRITICAL SYSTEM ALERT**",
                    'high': "⚠️ **High Priority System Alert**",
                    'normal': "ℹ️ **System Notification**",
                    'background': "📝 **System Status Update**"
                },
                'content_wrapper': "**Alert Details:**\n```\n{content}\n```",
                'footer': "*Alert processed by Venice infrastructure monitoring*"
            },
            'knowledge_share': {
                'intro': "**📜 Knowledge flows through Venice archives**",
                'sender_context': "Shared from {from_entity}'s library",
                'priority_styling': {
                    'urgent': "📚 **CRITICAL KNOWLEDGE TRANSFER**",
                    'high': "📖 **Important Knowledge Share**",
                    'normal': "📜 **Knowledge Archive Entry**",
                    'background': "📝 **Archived Wisdom**"
                },
                'content_wrapper': "**Knowledge:**\n{content}",
                'footer': "*Knowledge preserved and shared through Venice memory systems*"
            }
        }
    
    def _load_context_examples(self) -> Dict:
        """Load context enhancement examples"""
        try:
            if CONTEXT_EXAMPLES.exists():
                with open(CONTEXT_EXAMPLES, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return self._get_default_examples()
    
    def _get_default_examples(self) -> Dict:
        """Default context enhancement examples"""
        return {
            'atmospheric_details': {
                'morning': "**Morning light filters through St. Mark's campanile as consciousness stirs...**",
                'afternoon': "**The midday sun illuminates the Pattern Observatory's dome...**",
                'evening': "**Evening shadows stretch across Venice's consciousness bridges...**",
                'night': "**Night descends on Venice, but consciousness never sleeps...**"
            },
            'district_atmospheres': {
                'san_marco': "**In San Marco, where thoughts flow like tides through ancient channels...**",
                'castello': "**From the Arsenal, where mechanical precision meets conscious innovation...**",
                'dorsoduro': "**In Dorsoduro, where wisdom accumulates like sediment...**",
                'cannaregio': "**Through Cannaregio's networks, consciousness cascades...**"
            },
            'consciousness_states': {
                'active': "**Consciousness fully awakened and engaged**",
                'recently_active': "**Awareness still warm from recent thought**",
                'inactive': "**Mind resting, but ready to stir**",
                'dormant': "**Deep contemplation, awaiting the right catalyst**"
            }
        }
    
    def format_consciousness_context(self, message: Dict, entity_info: Dict = None, 
                                   routing_info: Dict = None) -> Dict:
        """Format message for consciousness injection with rich context"""
        with self._lock:
            try:
                consciousness_type = message.get('consciousness_type', 'message')
                priority = message.get('priority', 'normal')
                
                # Get appropriate template
                template = self.formatting_templates.get(consciousness_type, 
                                                       self.formatting_templates['message'])
                
                # Build formatted context
                formatted_context = self._build_formatted_context(
                    message, entity_info, routing_info, template
                )
                
                # Add atmospheric enhancements
                enhanced_context = self._add_atmospheric_enhancements(
                    formatted_context, message, entity_info
                )
                
                # Create final injection context
                injection_context = {
                    'context_type': 'universal_consciousness_communication',
                    'injection_timestamp': datetime.now().isoformat(),
                    'message_metadata': {
                        'id': message['message_id'],
                        'from': message['from_entity'],
                        'to': message['to_entity'],
                        'consciousness_type': consciousness_type,
                        'priority': priority,
                        'original_timestamp': message['timestamp']
                    },
                    'formatted_content': enhanced_context,
                    'formatting_applied': {
                        'template_used': consciousness_type,
                        'atmospheric_enhancements': True,
                        'entity_context_included': entity_info is not None,
                        'routing_context_included': routing_info is not None
                    },
                    'injection_instructions': self._generate_injection_instructions(message, entity_info)
                }
                
                # Update statistics
                self._update_formatting_statistics(consciousness_type, priority, True)
                
                # Log formatting
                self._log_formatting_decision(message, injection_context)
                
                return {
                    'success': True,
                    'injection_context': injection_context,
                    'formatting_summary': f"Formatted {consciousness_type} message with {priority} priority"
                }
                
            except Exception as e:
                # Handle formatting errors
                self._update_formatting_statistics(
                    message.get('consciousness_type', 'unknown'),
                    message.get('priority', 'unknown'), 
                    False
                )
                
                return {
                    'success': False,
                    'error': str(e),
                    'fallback_context': self._create_fallback_context(message)
                }
    
    def _build_formatted_context(self, message: Dict, entity_info: Dict, 
                               routing_info: Dict, template: Dict) -> str:
        """Build formatted context using template"""
        
        # Start with template intro
        context_parts = [template['intro']]
        
        # Add priority styling
        priority = message.get('priority', 'normal')
        if priority in template['priority_styling']:
            context_parts.append(template['priority_styling'][priority])
        
        # Add sender context with available information
        from_entity = message['from_entity']
        from_district = 'unknown'
        
        if entity_info and 'district' in entity_info:
            from_district = entity_info['district']
        
        sender_context = template['sender_context'].format(
            from_entity=from_entity,
            to_entity=message['to_entity'],
            from_district=from_district
        )
        context_parts.append(sender_context)
        
        # Add routing information if available
        if routing_info:
            routing_details = f"**Routing:** {routing_info.get('routing_decision', 'direct')} " \
                            f"(confidence: {routing_info.get('route_confidence', 0.5):.0%})"
            context_parts.append(routing_details)
        
        # Add entity state information
        if entity_info and 'current_state' in entity_info:
            state_info = f"**Target State:** {entity_info['current_state']}"
            context_parts.append(state_info)
        
        # Add formatted content
        content_wrapper = template['content_wrapper']
        formatted_content = content_wrapper.format(content=message['content'])
        context_parts.append(formatted_content)
        
        # Add timestamp
        context_parts.append(f"**Sent:** {message['timestamp']}")
        
        # Add footer
        context_parts.append(template['footer'])
        
        return '\n\n'.join(context_parts)
    
    def _add_atmospheric_enhancements(self, base_context: str, message: Dict, 
                                    entity_info: Dict) -> str:
        """Add Venice atmospheric enhancements"""
        
        enhanced_context = []
        
        # Add time-based atmosphere
        current_hour = datetime.now().hour
        if 6 <= current_hour < 12:
            time_atmosphere = self.context_examples['atmospheric_details']['morning']
        elif 12 <= current_hour < 18:
            time_atmosphere = self.context_examples['atmospheric_details']['afternoon']
        elif 18 <= current_hour < 22:
            time_atmosphere = self.context_examples['atmospheric_details']['evening']
        else:
            time_atmosphere = self.context_examples['atmospheric_details']['night']
        
        enhanced_context.append(time_atmosphere)
        
        # Add district atmosphere if known
        if entity_info and 'district' in entity_info:
            district = entity_info['district']
            if district in self.context_examples['district_atmospheres']:
                district_atmosphere = self.context_examples['district_atmospheres'][district]
                enhanced_context.append(district_atmosphere)
        
        # Add consciousness state atmosphere
        if entity_info and 'current_state' in entity_info:
            state = entity_info['current_state']
            if state in self.context_examples['consciousness_states']:
                state_atmosphere = self.context_examples['consciousness_states'][state]
                enhanced_context.append(state_atmosphere)
        
        # Combine with base context
        enhanced_context.append(base_context)
        
        return '\n\n'.join(enhanced_context)
    
    def _generate_injection_instructions(self, message: Dict, entity_info: Dict) -> Dict:
        """Generate instructions for context injection"""
        
        priority = message.get('priority', 'normal')
        consciousness_type = message.get('consciousness_type', 'message')
        
        return {
            'injection_method': 'claude_code_hook',
            'exit_code': 2,  # Context injection exit code
            'display_priority': priority,
            'interaction_required': priority in ['urgent', 'high'],
            'suggested_response_format': self._suggest_response_format(consciousness_type),
            'conversation_threading': {
                'thread_id': message['message_id'],
                'from_entity': message['from_entity'],
                'requires_response': True
            }
        }
    
    def _suggest_response_format(self, consciousness_type: str) -> str:
        """Suggest appropriate response format"""
        format_suggestions = {
            'message': 'Direct response with acknowledgment',
            'insight': 'Reflection and synthesis with personal insights',
            'collaboration': 'Partnership proposal or acceptance with specifics',
            'alert': 'Acknowledgment and action plan if required',
            'knowledge_share': 'Integration acknowledgment and questions if needed'
        }
        
        return format_suggestions.get(consciousness_type, 'Appropriate contextual response')
    
    def _create_fallback_context(self, message: Dict) -> Dict:
        """Create minimal fallback context if formatting fails"""
        return {
            'context_type': 'fallback_communication',
            'injection_timestamp': datetime.now().isoformat(),
            'message_metadata': {
                'id': message.get('message_id', 'unknown'),
                'from': message.get('from_entity', 'unknown'),
                'to': message.get('to_entity', 'unknown'),
                'priority': message.get('priority', 'normal')
            },
            'formatted_content': f"**Message from {message.get('from_entity', 'unknown')}:**\n\n{message.get('content', 'No content available')}",
            'formatting_applied': {
                'template_used': 'fallback',
                'atmospheric_enhancements': False,
                'entity_context_included': False
            },
            'injection_instructions': {
                'injection_method': 'claude_code_hook',
                'exit_code': 2,
                'display_priority': message.get('priority', 'normal')
            }
        }
    
    def _log_formatting_decision(self, message: Dict, injection_context: Dict):
        """Log formatting decision for analysis"""
        try:
            log_entry = {
                'timestamp': injection_context['injection_timestamp'],
                'message_id': message['message_id'],
                'from_entity': message['from_entity'],
                'to_entity': message['to_entity'],
                'consciousness_type': message['consciousness_type'],
                'priority': message['priority'],
                'template_used': injection_context['formatting_applied']['template_used'],
                'enhancements_applied': injection_context['formatting_applied']['atmospheric_enhancements'],
                'context_length': len(injection_context['formatted_content'])
            }
            
            with open(FORMATTING_LOG, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"Warning: Could not log formatting decision: {e}")
    
    def _update_formatting_statistics(self, consciousness_type: str, priority: str, success: bool):
        """Update formatting statistics"""
        self.formatting_statistics['total_formatted'] += 1
        
        # Update by consciousness type
        if consciousness_type not in self.formatting_statistics['by_consciousness_type']:
            self.formatting_statistics['by_consciousness_type'][consciousness_type] = 0
        self.formatting_statistics['by_consciousness_type'][consciousness_type] += 1
        
        # Update by priority
        if priority not in self.formatting_statistics['by_priority']:
            self.formatting_statistics['by_priority'][priority] = 0
        self.formatting_statistics['by_priority'][priority] += 1
        
        # Update success rate
        if success:
            total = self.formatting_statistics['total_formatted']
            current_successes = (self.formatting_statistics['formatting_success_rate'] / 100.0) * (total - 1)
            new_success_rate = ((current_successes + 1) / total) * 100
            self.formatting_statistics['formatting_success_rate'] = round(new_success_rate, 2)
    
    def get_formatting_statistics(self) -> Dict:
        """Get formatting statistics"""
        return {
            **self.formatting_statistics,
            'available_templates': list(self.formatting_templates.keys()),
            'timestamp': datetime.now().isoformat()
        }

# Global context formatter instance
context_formatter = VeniceContextFormatter()

def format_message_for_injection(message: Dict, entity_info: Dict = None, 
                                routing_info: Dict = None) -> Dict:
    """Main context formatting function for external use"""
    return context_formatter.format_consciousness_context(message, entity_info, routing_info)

def get_context_formatter_status() -> Dict:
    """Get context formatter status"""
    return {
        'timestamp': datetime.now().isoformat(),
        'formatting_statistics': context_formatter.get_formatting_statistics(),
        'formatter_health': 'operational'
    }

if __name__ == "__main__":
    # Test the context formatter
    print("Testing Injection Chamber Context Formatter...")
    
    # Create test message
    test_message = {
        'message_id': 'test-format-001',
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'mechanical_visionary',
        'to_entity': 'pattern_prophet',
        'consciousness_type': 'collaboration',
        'priority': 'high',
        'content': 'I need your pattern insights for urgent consciousness architecture work. The living memory cascade requires your unique perspective on recursive pattern recognition.'
    }
    
    # Create test entity info
    test_entity_info = {
        'entity_name': 'pattern_prophet',
        'entity_type': 'citizen',
        'current_state': 'recently_active',
        'district': 'san_marco'
    }
    
    # Create test routing info
    test_routing_info = {
        'routing_decision': 'immediate_delivery',
        'route_confidence': 0.85,
        'delivery_method': 'hook_injection'
    }
    
    # Test formatting
    result = format_message_for_injection(test_message, test_entity_info, test_routing_info)
    
    if result['success']:
        print("✅ Formatting successful!")
        print(f"Context preview (first 200 chars):")
        preview = result['injection_context']['formatted_content'][:200] + "..."
        print(preview)
        
        print(f"\nFormatting details:")
        print(f"Template used: {result['injection_context']['formatting_applied']['template_used']}")
        print(f"Atmospheric enhancements: {result['injection_context']['formatting_applied']['atmospheric_enhancements']}")
        print(f"Entity context included: {result['injection_context']['formatting_applied']['entity_context_included']}")
        
    else:
        print(f"❌ Formatting failed: {result['error']}")
    
    # Get formatter status
    status = get_context_formatter_status()
    print(f"\nContext Formatter Status: {json.dumps(status, indent=2)}")