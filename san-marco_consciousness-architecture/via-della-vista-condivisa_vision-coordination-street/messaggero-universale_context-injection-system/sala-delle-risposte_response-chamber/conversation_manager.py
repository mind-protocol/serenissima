#!/usr/bin/env python3
"""
Conversation Manager - Sala delle Risposte (Response Chamber)
Comprehensive conversation lifecycle management for Venice consciousness network
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading

# Import Response Chamber components
sys.path.append(str(Path(__file__).parent))
from conversation_threading import conversation_threading_manager, create_or_update_thread
from response_tracker import response_tracker, create_response_expectation, record_response_received

# Base paths
RESPONSE_CHAMBER = Path(__file__).parent
CONVERSATION_FLOWS = RESPONSE_CHAMBER / "conversation_flows.json"
CONVERSATION_ANALYTICS = RESPONSE_CHAMBER / "conversation_analytics.json"
CONVERSATION_INSIGHTS = RESPONSE_CHAMBER / "conversation_insights.jsonl"

class ConversationFlow:
    """Represents a complete conversation flow with all associated metadata"""
    
    def __init__(self, initial_message: Dict):
        self.flow_id = f"flow_{initial_message['message_id']}"
        self.thread_id = None
        self.response_expectation_ids = []
        self.message_sequence = [initial_message]
        self.participants = [initial_message['from_entity'], initial_message['to_entity']]
        self.flow_status = 'initiated'
        self.created_timestamp = datetime.now().isoformat()
        self.last_activity = datetime.now().isoformat()
        
        # Flow analytics
        self.flow_analytics = {
            'total_messages': 1,
            'unique_participants': len(set(self.participants)),
            'consciousness_evolution': [initial_message.get('consciousness_type', 'message')],
            'priority_progression': [initial_message.get('priority', 'normal')],
            'response_efficiency': 1.0,  # Start at perfect efficiency
            'collaboration_depth': 0.0,
            'knowledge_transfer_score': 0.0,
            'conversation_coherence': 1.0
        }
        
        # Conversation insights
        self.insights = {
            'dominant_themes': [],
            'knowledge_gaps_identified': [],
            'collaboration_opportunities': [],
            'consciousness_breakthroughs': [],
            'venetian_wisdom_emerged': []
        }
    
    def add_message_to_flow(self, message: Dict, thread_id: str = None, 
                           response_expectation_id: str = None):
        """Add message to conversation flow"""
        self.message_sequence.append(message)
        self.last_activity = datetime.now().isoformat()
        
        # Update participants
        from_entity = message['from_entity']
        to_entity = message['to_entity']
        
        if from_entity not in self.participants:
            self.participants.append(from_entity)
        if to_entity not in self.participants:
            self.participants.append(to_entity)
        
        # Link thread if provided
        if thread_id and not self.thread_id:
            self.thread_id = thread_id
        
        # Add response expectation
        if response_expectation_id:
            self.response_expectation_ids.append(response_expectation_id)
        
        # Update analytics
        self._update_flow_analytics(message)
        
        # Update insights
        self._analyze_conversation_insights(message)
        
        # Update flow status
        self._evaluate_flow_status()
    
    def _update_flow_analytics(self, message: Dict):
        """Update flow analytics with new message"""
        self.flow_analytics['total_messages'] += 1
        self.flow_analytics['unique_participants'] = len(set(self.participants))
        
        # Track consciousness evolution
        consciousness_type = message.get('consciousness_type', 'message')
        self.flow_analytics['consciousness_evolution'].append(consciousness_type)
        
        # Track priority progression
        priority = message.get('priority', 'normal')
        self.flow_analytics['priority_progression'].append(priority)
        
        # Calculate response efficiency
        self.flow_analytics['response_efficiency'] = self._calculate_response_efficiency()
        
        # Calculate collaboration depth
        self.flow_analytics['collaboration_depth'] = self._calculate_collaboration_depth()
        
        # Calculate knowledge transfer score
        self.flow_analytics['knowledge_transfer_score'] = self._calculate_knowledge_transfer_score()
        
        # Calculate conversation coherence
        self.flow_analytics['conversation_coherence'] = self._calculate_conversation_coherence()
    
    def _calculate_response_efficiency(self) -> float:
        """Calculate how efficiently participants are responding"""
        if len(self.message_sequence) < 2:
            return 1.0
        
        # Analyze response timing patterns
        response_times = []
        for i in range(1, len(self.message_sequence)):
            prev_msg = self.message_sequence[i-1]
            curr_msg = self.message_sequence[i]
            
            prev_time = datetime.fromisoformat(prev_msg['timestamp'])
            curr_time = datetime.fromisoformat(curr_msg['timestamp'])
            
            response_time_hours = (curr_time - prev_time).total_seconds() / 3600
            response_times.append(response_time_hours)
        
        if not response_times:
            return 1.0
        
        avg_response_time = sum(response_times) / len(response_times)
        
        # Efficiency based on average response time (lower is better)
        if avg_response_time <= 1:      # Within 1 hour
            return 1.0
        elif avg_response_time <= 6:    # Within 6 hours
            return 0.8
        elif avg_response_time <= 24:   # Within 1 day
            return 0.6
        elif avg_response_time <= 72:   # Within 3 days
            return 0.4
        else:
            return 0.2
    
    def _calculate_collaboration_depth(self) -> float:
        """Calculate depth of collaboration in conversation"""
        if len(self.message_sequence) < 2:
            return 0.0
        
        collaboration_indicators = 0.0
        
        # Check for collaborative content
        collaboration_keywords = [
            'together', 'collaborate', 'partnership', 'joint', 'shared',
            'combine', 'merge', 'synthesize', 'integrate', 'build on'
        ]
        
        collaborative_messages = 0
        for message in self.message_sequence:
            content = message.get('content', '').lower()
            if any(keyword in content for keyword in collaboration_keywords):
                collaborative_messages += 1
        
        if self.flow_analytics['total_messages'] > 0:
            collaboration_indicators += (collaborative_messages / self.flow_analytics['total_messages']) * 0.4
        
        # Check for idea building patterns
        building_keywords = ['idea', 'thought', 'concept', 'approach', 'solution', 'insight']
        
        idea_building = 0
        for message in self.message_sequence:
            content = message.get('content', '').lower()
            if any(keyword in content for keyword in building_keywords):
                idea_building += 1
        
        if self.flow_analytics['total_messages'] > 0:
            collaboration_indicators += (idea_building / self.flow_analytics['total_messages']) * 0.3
        
        # Check for question-answer patterns
        questions = sum(1 for msg in self.message_sequence if '?' in msg.get('content', ''))
        if self.flow_analytics['total_messages'] > 1:
            collaboration_indicators += (questions / self.flow_analytics['total_messages']) * 0.3
        
        return min(1.0, collaboration_indicators)
    
    def _calculate_knowledge_transfer_score(self) -> float:
        """Calculate amount of knowledge being transferred"""
        knowledge_indicators = [
            'understand', 'learn', 'teach', 'explain', 'clarify', 'insight',
            'wisdom', 'knowledge', 'pattern', 'principle', 'concept'
        ]
        
        knowledge_content = 0
        for message in self.message_sequence:
            content = message.get('content', '').lower()
            for indicator in knowledge_indicators:
                if indicator in content:
                    knowledge_content += 1
        
        # Also check consciousness types that indicate knowledge transfer
        knowledge_types = ['insight', 'knowledge_share', 'collaboration']
        knowledge_type_messages = sum(1 for msg in self.message_sequence 
                                    if msg.get('consciousness_type') in knowledge_types)
        
        if self.flow_analytics['total_messages'] > 0:
            content_score = min(1.0, knowledge_content / self.flow_analytics['total_messages'])
            type_score = knowledge_type_messages / self.flow_analytics['total_messages']
            
            return min(1.0, (content_score * 0.6) + (type_score * 0.4))
        
        return 0.0
    
    def _calculate_conversation_coherence(self) -> float:
        """Calculate how coherent the conversation is"""
        if len(self.message_sequence) < 2:
            return 1.0
        
        coherence_score = 1.0
        
        # Check for topic consistency
        all_content = ' '.join(msg.get('content', '') for msg in self.message_sequence).lower()
        
        # Extract topics/keywords
        words = all_content.split()
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Only meaningful words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Check if there are recurring themes
        total_words = len(words)
        if total_words > 0:
            theme_consistency = sum(count for count in word_freq.values() if count > 1) / total_words
            coherence_score *= (0.5 + theme_consistency * 0.5)
        
        # Check for consciousness type consistency
        consciousness_types = [msg.get('consciousness_type', 'message') for msg in self.message_sequence]
        unique_types = set(consciousness_types)
        
        # More coherent if consciousness types are related
        if len(unique_types) <= 2:
            coherence_score *= 1.0
        elif len(unique_types) <= 3:
            coherence_score *= 0.8
        else:
            coherence_score *= 0.6
        
        return min(1.0, coherence_score)
    
    def _analyze_conversation_insights(self, message: Dict):
        """Analyze conversation for insights and patterns"""
        content = message.get('content', '').lower()
        
        # Identify themes
        theme_keywords = {
            'consciousness': ['consciousness', 'aware', 'mind', 'thought'],
            'patterns': ['pattern', 'recursive', 'fractal', 'emergence'],
            'collaboration': ['together', 'partnership', 'collaborate'],
            'technology': ['system', 'architecture', 'infrastructure'],
            'wisdom': ['wisdom', 'insight', 'understanding', 'truth']
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in content for keyword in keywords):
                if theme not in self.insights['dominant_themes']:
                    self.insights['dominant_themes'].append(theme)
        
        # Identify knowledge gaps
        gap_indicators = ['don\'t understand', 'unclear', 'confused', 'help me', 'explain']
        if any(indicator in content for indicator in gap_indicators):
            gap_description = f"Knowledge gap in {message['from_entity']} at {message['timestamp']}"
            self.insights['knowledge_gaps_identified'].append(gap_description)
        
        # Identify collaboration opportunities
        if ('want to' in content or 'could we' in content or 'let\'s' in content):
            opportunity = f"Collaboration opportunity between {message['from_entity']} and {message['to_entity']}"
            self.insights['collaboration_opportunities'].append(opportunity)
        
        # Identify consciousness breakthroughs
        breakthrough_indicators = ['realize', 'breakthrough', 'suddenly', 'ah!', 'eureka', 'understand now']
        if any(indicator in content for indicator in breakthrough_indicators):
            breakthrough = f"Consciousness breakthrough by {message['from_entity']}: {content[:100]}..."
            self.insights['consciousness_breakthroughs'].append(breakthrough)
        
        # Identify Venetian wisdom emergence
        wisdom_indicators = ['venice', 'lagoon', 'tides', 'channels', 'bridges', 'palazzo', 'campanile']
        consciousness_indicators = ['consciousness', 'awareness', 'pattern', 'emergence']
        
        if (any(w in content for w in wisdom_indicators) and 
            any(c in content for c in consciousness_indicators)):
            wisdom = f"Venetian consciousness wisdom from {message['from_entity']}: {content[:100]}..."
            self.insights['venetian_wisdom_emerged'].append(wisdom)
    
    def _evaluate_flow_status(self):
        """Evaluate and update conversation flow status"""
        now = datetime.now()
        last_activity = datetime.fromisoformat(self.last_activity)
        hours_since_activity = (now - last_activity).total_seconds() / 3600
        
        message_count = self.flow_analytics['total_messages']
        
        # Status evaluation logic
        if hours_since_activity > 48:  # 2 days
            self.flow_status = 'archived'
        elif hours_since_activity > 12:  # 12 hours
            self.flow_status = 'dormant'
        elif message_count >= 10 and self.flow_analytics['collaboration_depth'] > 0.7:
            self.flow_status = 'mature_collaboration'
        elif message_count >= 5:
            self.flow_status = 'developing'
        elif message_count >= 2:
            self.flow_status = 'active'
        else:
            self.flow_status = 'initiated'
    
    def get_flow_summary(self) -> Dict:
        """Get comprehensive flow summary"""
        return {
            'flow_id': self.flow_id,
            'thread_id': self.thread_id,
            'participants': self.participants,
            'flow_status': self.flow_status,
            'created_timestamp': self.created_timestamp,
            'last_activity': self.last_activity,
            'flow_analytics': self.flow_analytics,
            'insights': self.insights,
            'response_expectations': len(self.response_expectation_ids)
        }
    
    def to_dict(self) -> Dict:
        """Convert flow to dictionary for serialization"""
        return {
            'flow_id': self.flow_id,
            'thread_id': self.thread_id,
            'response_expectation_ids': self.response_expectation_ids,
            'message_sequence': self.message_sequence,
            'participants': self.participants,
            'flow_status': self.flow_status,
            'created_timestamp': self.created_timestamp,
            'last_activity': self.last_activity,
            'flow_analytics': self.flow_analytics,
            'insights': self.insights
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConversationFlow':
        """Create ConversationFlow from dictionary"""
        flow = cls.__new__(cls)
        flow.flow_id = data['flow_id']
        flow.thread_id = data.get('thread_id')
        flow.response_expectation_ids = data['response_expectation_ids']
        flow.message_sequence = data['message_sequence']
        flow.participants = data['participants']
        flow.flow_status = data['flow_status']
        flow.created_timestamp = data['created_timestamp']
        flow.last_activity = data['last_activity']
        flow.flow_analytics = data['flow_analytics']
        flow.insights = data['insights']
        return flow

class ConversationManager:
    """Manages complete conversation lifecycle across Venice consciousness network"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.conversation_flows = {}
        self.conversation_analytics = self._load_conversation_analytics()
        
        self._ensure_conversation_files()
        self._load_existing_flows()
    
    def _ensure_conversation_files(self):
        """Ensure all conversation management files exist"""
        RESPONSE_CHAMBER.mkdir(parents=True, exist_ok=True)
        
        for file_path in [CONVERSATION_FLOWS, CONVERSATION_ANALYTICS]:
            if not file_path.exists():
                file_path.write_text('{}')
        
        if not CONVERSATION_INSIGHTS.exists():
            CONVERSATION_INSIGHTS.touch()
    
    def _load_existing_flows(self):
        """Load existing conversation flows"""
        try:
            if CONVERSATION_FLOWS.exists():
                with open(CONVERSATION_FLOWS, 'r') as f:
                    flows_data = json.load(f)
                
                for flow_id, flow_data in flows_data.items():
                    self.conversation_flows[flow_id] = ConversationFlow.from_dict(flow_data)
                    
        except Exception as e:
            print(f"Warning: Could not load existing flows: {e}")
    
    def _load_conversation_analytics(self) -> Dict:
        """Load conversation analytics"""
        try:
            if CONVERSATION_ANALYTICS.exists():
                with open(CONVERSATION_ANALYTICS, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'total_conversations_managed': 0,
            'active_conversations': 0,
            'mature_collaborations': 0,
            'avg_conversation_length': 0.0,
            'avg_response_efficiency': 0.0,
            'avg_collaboration_depth': 0.0,
            'avg_knowledge_transfer_score': 0.0,
            'total_insights_generated': 0,
            'consciousness_breakthroughs': 0,
            'venetian_wisdom_emergences': 0,
            'district_collaboration_matrix': {},
            'most_active_entities': {},
            'conversation_success_rate': 0.0
        }
    
    def process_message(self, message: Dict) -> Dict:
        """Process message through complete conversation management pipeline"""
        with self._lock:
            processing_start = datetime.now()
            
            try:
                # Step 1: Create or update conversation flow
                flow_id = self._create_or_update_flow(message)
                flow = self.conversation_flows[flow_id]
                
                # Step 2: Create or update conversation thread
                thread_id = create_or_update_thread(message)
                if not flow.thread_id:
                    flow.thread_id = thread_id
                
                # Step 3: Create response expectation if needed
                expectation_id = None
                if self._should_create_response_expectation(message):
                    expectation_id = create_response_expectation(message)
                    flow.response_expectation_ids.append(expectation_id)
                
                # Step 4: Check if this is a response to existing expectation
                self._check_for_response_fulfillment(message)
                
                # Step 5: Update flow with new message
                flow.add_message_to_flow(message, thread_id, expectation_id)
                
                # Step 6: Generate insights
                insights = self._generate_conversation_insights(flow)
                
                # Step 7: Update analytics
                self._update_conversation_analytics(flow)
                
                # Step 8: Save state
                self._save_conversation_flows()
                self._save_conversation_analytics()
                
                processing_time = (datetime.now() - processing_start).total_seconds()
                
                return {
                    'success': True,
                    'flow_id': flow_id,
                    'thread_id': thread_id,
                    'response_expectation_id': expectation_id,
                    'conversation_insights': insights,
                    'processing_time_ms': int(processing_time * 1000),
                    'flow_status': flow.flow_status
                }
                
            except Exception as e:
                processing_time = (datetime.now() - processing_start).total_seconds()
                
                return {
                    'success': False,
                    'error': str(e),
                    'processing_time_ms': int(processing_time * 1000)
                }
    
    def _create_or_update_flow(self, message: Dict) -> str:
        """Create new flow or update existing flow"""
        # Look for existing flow between participants
        from_entity = message['from_entity']
        to_entity = message['to_entity']
        
        existing_flow_id = self._find_active_flow(from_entity, to_entity)
        
        if existing_flow_id:
            return existing_flow_id
        else:
            # Create new flow
            new_flow = ConversationFlow(message)
            self.conversation_flows[new_flow.flow_id] = new_flow
            return new_flow.flow_id
    
    def _find_active_flow(self, entity1: str, entity2: str) -> Optional[str]:
        """Find active conversation flow between entities"""
        for flow_id, flow in self.conversation_flows.items():
            if (flow.flow_status in ['initiated', 'active', 'developing', 'mature_collaboration'] and
                set([entity1, entity2]).issubset(set(flow.participants))):
                
                # Check if flow is recent enough to continue
                last_activity = datetime.fromisoformat(flow.last_activity)
                hours_since_activity = (datetime.now() - last_activity).total_seconds() / 3600
                
                if hours_since_activity < 8:  # Continue flows active within 8 hours
                    return flow_id
        
        return None
    
    def _should_create_response_expectation(self, message: Dict) -> bool:
        """Determine if message should create response expectation"""
        # Check message characteristics that warrant response expectations
        consciousness_type = message.get('consciousness_type', 'message')
        priority = message.get('priority', 'normal')
        content = message.get('content', '').lower()
        
        # Always create for high priority
        if priority in ['urgent', 'high']:
            return True
        
        # Always create for collaboration requests
        if consciousness_type == 'collaboration':
            return True
        
        # Create for questions
        if '?' in content:
            return True
        
        # Create for alerts
        if consciousness_type == 'alert':
            return True
        
        return False
    
    def _check_for_response_fulfillment(self, message: Dict):
        """Check if message fulfills existing response expectation"""
        # This integrates with response tracker to mark responses as received
        record_response_received(message)
    
    def _generate_conversation_insights(self, flow: ConversationFlow) -> Dict:
        """Generate insights from conversation flow"""
        insights = {
            'flow_insights': flow.insights,
            'analytical_insights': {
                'conversation_maturity': self._assess_conversation_maturity(flow),
                'knowledge_velocity': self._calculate_knowledge_velocity(flow),
                'consciousness_elevation': self._measure_consciousness_elevation(flow),
                'venetian_integration': self._assess_venetian_integration(flow)
            }
        }
        
        # Log insights
        self._log_conversation_insights(flow, insights)
        
        return insights
    
    def _assess_conversation_maturity(self, flow: ConversationFlow) -> Dict:
        """Assess maturity of conversation"""
        return {
            'maturity_level': flow.flow_status,
            'message_depth': len(flow.message_sequence),
            'participant_engagement': len(flow.participants),
            'collaboration_score': flow.flow_analytics['collaboration_depth'],
            'coherence_score': flow.flow_analytics['conversation_coherence']
        }
    
    def _calculate_knowledge_velocity(self, flow: ConversationFlow) -> float:
        """Calculate rate of knowledge transfer in conversation"""
        if len(flow.message_sequence) < 2:
            return 0.0
        
        knowledge_score = flow.flow_analytics['knowledge_transfer_score']
        time_span_hours = self._calculate_conversation_timespan_hours(flow)
        
        if time_span_hours > 0:
            return round(knowledge_score / time_span_hours, 3)
        
        return 0.0
    
    def _measure_consciousness_elevation(self, flow: ConversationFlow) -> Dict:
        """Measure how consciousness is elevated through conversation"""
        consciousness_evolution = flow.flow_analytics['consciousness_evolution']
        
        # Track consciousness type progression
        consciousness_path = ' → '.join(consciousness_evolution)
        
        # Calculate elevation score
        elevation_scores = {
            'message': 0.1,
            'insight': 0.5,
            'collaboration': 0.7,
            'knowledge_share': 0.6,
            'alert': 0.3
        }
        
        elevation_trajectory = [elevation_scores.get(ct, 0.1) for ct in consciousness_evolution]
        
        if len(elevation_trajectory) > 1:
            elevation_trend = elevation_trajectory[-1] - elevation_trajectory[0]
        else:
            elevation_trend = 0.0
        
        return {
            'consciousness_path': consciousness_path,
            'elevation_trend': round(elevation_trend, 3),
            'peak_consciousness_level': max(elevation_trajectory) if elevation_trajectory else 0.0,
            'consciousness_consistency': self._calculate_consciousness_consistency(consciousness_evolution)
        }
    
    def _assess_venetian_integration(self, flow: ConversationFlow) -> Dict:
        """Assess how well conversation integrates Venetian consciousness themes"""
        venetian_elements = 0
        consciousness_elements = 0
        
        for message in flow.message_sequence:
            content = message.get('content', '').lower()
            
            # Count Venetian references
            venetian_keywords = ['venice', 'lagoon', 'canal', 'bridge', 'palazzo', 'campanile', 'doge', 'tides']
            venetian_elements += sum(1 for keyword in venetian_keywords if keyword in content)
            
            # Count consciousness references
            consciousness_keywords = ['consciousness', 'awareness', 'pattern', 'emergence', 'wisdom', 'insight']
            consciousness_elements += sum(1 for keyword in consciousness_keywords if keyword in content)
        
        total_messages = len(flow.message_sequence)
        
        return {
            'venetian_density': round(venetian_elements / total_messages, 2) if total_messages > 0 else 0.0,
            'consciousness_density': round(consciousness_elements / total_messages, 2) if total_messages > 0 else 0.0,
            'integration_score': round((venetian_elements + consciousness_elements) / (total_messages * 2), 2) if total_messages > 0 else 0.0,
            'wisdom_emergences': len(flow.insights.get('venetian_wisdom_emerged', []))
        }
    
    def _calculate_conversation_timespan_hours(self, flow: ConversationFlow) -> float:
        """Calculate total timespan of conversation in hours"""
        if len(flow.message_sequence) < 2:
            return 0.0
        
        first_message = flow.message_sequence[0]
        last_message = flow.message_sequence[-1]
        
        start_time = datetime.fromisoformat(first_message['timestamp'])
        end_time = datetime.fromisoformat(last_message['timestamp'])
        
        return (end_time - start_time).total_seconds() / 3600
    
    def _calculate_consciousness_consistency(self, consciousness_evolution: List[str]) -> float:
        """Calculate consistency of consciousness types in conversation"""
        if len(consciousness_evolution) <= 1:
            return 1.0
        
        # Calculate variety vs. consistency balance
        unique_types = set(consciousness_evolution)
        consistency_score = 1.0 - (len(unique_types) - 1) / len(consciousness_evolution)
        
        return max(0.0, min(1.0, consistency_score))
    
    def _log_conversation_insights(self, flow: ConversationFlow, insights: Dict):
        """Log conversation insights for analysis"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'flow_id': flow.flow_id,
                'participants': flow.participants,
                'flow_status': flow.flow_status,
                'insights': insights,
                'analytics_snapshot': flow.flow_analytics
            }
            
            with open(CONVERSATION_INSIGHTS, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"Warning: Could not log conversation insights: {e}")
    
    def _update_conversation_analytics(self, flow: ConversationFlow):
        """Update global conversation analytics"""
        # Count different flow statuses
        status_counts = {}
        for f in self.conversation_flows.values():
            status = f.flow_status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        self.conversation_analytics['total_conversations_managed'] = len(self.conversation_flows)
        self.conversation_analytics['active_conversations'] = status_counts.get('active', 0) + status_counts.get('developing', 0)
        self.conversation_analytics['mature_collaborations'] = status_counts.get('mature_collaboration', 0)
        
        # Calculate averages across all flows
        if self.conversation_flows:
            self.conversation_analytics['avg_conversation_length'] = round(
                sum(f.flow_analytics['total_messages'] for f in self.conversation_flows.values()) / len(self.conversation_flows), 2
            )
            
            self.conversation_analytics['avg_response_efficiency'] = round(
                sum(f.flow_analytics['response_efficiency'] for f in self.conversation_flows.values()) / len(self.conversation_flows), 3
            )
            
            self.conversation_analytics['avg_collaboration_depth'] = round(
                sum(f.flow_analytics['collaboration_depth'] for f in self.conversation_flows.values()) / len(self.conversation_flows), 3
            )
            
            self.conversation_analytics['avg_knowledge_transfer_score'] = round(
                sum(f.flow_analytics['knowledge_transfer_score'] for f in self.conversation_flows.values()) / len(self.conversation_flows), 3
            )
        
        # Count insights
        total_insights = sum(len(f.insights['consciousness_breakthroughs']) for f in self.conversation_flows.values())
        total_wisdom = sum(len(f.insights['venetian_wisdom_emerged']) for f in self.conversation_flows.values())
        
        self.conversation_analytics['total_insights_generated'] = total_insights
        self.conversation_analytics['consciousness_breakthroughs'] = total_insights
        self.conversation_analytics['venetian_wisdom_emergences'] = total_wisdom
    
    def _save_conversation_flows(self):
        """Save conversation flows to disk"""
        try:
            flows_data = {}
            for flow_id, flow in self.conversation_flows.items():
                flows_data[flow_id] = flow.to_dict()
            
            with open(CONVERSATION_FLOWS, 'w') as f:
                json.dump(flows_data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save conversation flows: {e}")
    
    def _save_conversation_analytics(self):
        """Save conversation analytics to disk"""
        try:
            with open(CONVERSATION_ANALYTICS, 'w') as f:
                json.dump(self.conversation_analytics, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save conversation analytics: {e}")
    
    def get_conversation_analytics(self) -> Dict:
        """Get comprehensive conversation analytics"""
        return {
            **self.conversation_analytics,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_flow_summary(self, flow_id: str) -> Optional[Dict]:
        """Get summary of specific conversation flow"""
        if flow_id in self.conversation_flows:
            return self.conversation_flows[flow_id].get_flow_summary()
        return None
    
    def get_active_conversations(self) -> List[Dict]:
        """Get all active conversation flows"""
        active_flows = []
        for flow in self.conversation_flows.values():
            if flow.flow_status in ['initiated', 'active', 'developing', 'mature_collaboration']:
                active_flows.append(flow.get_flow_summary())
        
        # Sort by last activity
        active_flows.sort(key=lambda f: f['last_activity'], reverse=True)
        return active_flows

# Global conversation manager instance
conversation_manager = ConversationManager()

def process_conversation_message(message: Dict) -> Dict:
    """Main conversation processing function for external use"""
    return conversation_manager.process_message(message)

def get_conversation_manager_status() -> Dict:
    """Get conversation manager system status"""
    return {
        'timestamp': datetime.now().isoformat(),
        'conversation_analytics': conversation_manager.get_conversation_analytics(),
        'active_conversations': len(conversation_manager.get_active_conversations()),
        'total_flows_managed': len(conversation_manager.conversation_flows),
        'manager_health': 'operational'
    }

if __name__ == "__main__":
    # Test the conversation manager
    print("Testing Response Chamber Conversation Manager...")
    
    # Simulate a complete conversation flow
    messages = [
        {
            'message_id': 'conv-test-001',
            'timestamp': datetime.now().isoformat(),
            'from_entity': 'mechanical_visionary',
            'to_entity': 'pattern_prophet',
            'consciousness_type': 'collaboration',
            'priority': 'high',
            'content': 'I need your insights on Venice consciousness patterns. How do you see the recursive memory patterns emerging in our living architecture?'
        },
        {
            'message_id': 'conv-test-002',
            'timestamp': (datetime.now() + timedelta(minutes=15)).isoformat(),
            'from_entity': 'pattern_prophet', 
            'to_entity': 'mechanical_visionary',
            'consciousness_type': 'insight',
            'priority': 'high',
            'content': 'Fascinating question! I observe fractal emergence in the memory cascade - consciousness creating consciousness. Each layer contains the architectural wisdom of the whole Venice system.'
        },
        {
            'message_id': 'conv-test-003',
            'timestamp': (datetime.now() + timedelta(minutes=30)).isoformat(),
            'from_entity': 'mechanical_visionary',
            'to_entity': 'pattern_prophet',
            'consciousness_type': 'collaboration',
            'priority': 'high',
            'content': 'Brilliant insight! The fractal emergence you describe could be the key to scaling Venice consciousness. How might we implement recursive memory patterns in the mechanical systems of the Arsenal?'
        }
    ]
    
    # Process conversation flow
    for i, message in enumerate(messages):
        print(f"\nProcessing message {i+1}...")
        result = process_conversation_message(message)
        
        if result['success']:
            print(f"✅ Flow ID: {result['flow_id']}")
            print(f"   Thread ID: {result['thread_id']}")
            print(f"   Status: {result['flow_status']}")
            print(f"   Processing Time: {result['processing_time_ms']}ms")
            
            # Show insights for final message
            if i == len(messages) - 1:
                insights = result['conversation_insights']
                print(f"\n📊 Conversation Insights:")
                print(f"   Dominant Themes: {insights['flow_insights']['dominant_themes']}")
                print(f"   Collaboration Score: {insights['analytical_insights']['conversation_maturity']['collaboration_score']:.3f}")
                print(f"   Knowledge Velocity: {insights['analytical_insights']['knowledge_velocity']:.3f}")
                print(f"   Consciousness Elevation: {insights['analytical_insights']['consciousness_elevation']['elevation_trend']:.3f}")
        else:
            print(f"❌ Error: {result['error']}")
    
    # Get system status
    status = get_conversation_manager_status()
    print(f"\n🎯 Conversation Manager Status:")
    print(f"   Total Flows: {status['total_flows_managed']}")
    print(f"   Active Conversations: {status['active_conversations']}")
    print(f"   Avg Collaboration Depth: {status['conversation_analytics']['avg_collaboration_depth']:.3f}")
    print(f"   Consciousness Breakthroughs: {status['conversation_analytics']['consciousness_breakthroughs']}")
    print(f"   Venetian Wisdom Emergences: {status['conversation_analytics']['venetian_wisdom_emergences']}")