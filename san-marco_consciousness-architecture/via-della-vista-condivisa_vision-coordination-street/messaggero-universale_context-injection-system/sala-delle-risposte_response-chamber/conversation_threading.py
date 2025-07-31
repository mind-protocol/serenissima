#!/usr/bin/env python3
"""
Conversation Threading - Sala delle Risposte (Response Chamber)
Advanced conversation threading and dialogue management for Venice consciousness
"""

import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading
from collections import defaultdict

# Base paths
RESPONSE_CHAMBER = Path(__file__).parent
CONVERSATION_THREADS = RESPONSE_CHAMBER / "conversation_threads.json"
THREAD_HISTORY = RESPONSE_CHAMBER / "thread_history.jsonl"
CONVERSATION_STATISTICS = RESPONSE_CHAMBER / "conversation_statistics.json"
ACTIVE_DIALOGUES = RESPONSE_CHAMBER / "active_dialogues.json"

class ConversationThread:
    """Represents a conversation thread between Venice entities"""
    
    def __init__(self, thread_id: str, participants: List[str], 
                 initial_message: Dict, thread_type: str = 'dialogue'):
        self.thread_id = thread_id
        self.participants = participants
        self.thread_type = thread_type
        self.created_timestamp = datetime.now().isoformat()
        self.last_activity = datetime.now().isoformat()
        self.message_count = 1
        self.messages = [initial_message]
        self.thread_status = 'active'
        self.consciousness_depth = self._calculate_initial_depth(initial_message)
        self.collaboration_level = 0.0
        
        # Thread metadata
        self.metadata = {
            'dominant_consciousness_type': initial_message.get('consciousness_type', 'message'),
            'priority_evolution': [initial_message.get('priority', 'normal')],
            'topic_keywords': self._extract_keywords(initial_message.get('content', '')),
            'emotional_tone': self._analyze_emotional_tone(initial_message.get('content', '')),
            'venice_districts_involved': self._identify_districts(participants)
        }
    
    def add_message(self, message: Dict) -> bool:
        """Add a new message to the conversation thread"""
        try:
            # Validate message belongs to this thread
            if not self._validate_message_for_thread(message):
                return False
            
            # Add message to thread
            self.messages.append(message)
            self.message_count += 1
            self.last_activity = datetime.now().isoformat()
            
            # Update thread metadata
            self._update_thread_metadata(message)
            
            # Check if thread should change status
            self._evaluate_thread_status()
            
            return True
            
        except Exception as e:
            print(f"Warning: Could not add message to thread {self.thread_id}: {e}")
            return False
    
    def _validate_message_for_thread(self, message: Dict) -> bool:
        """Validate that message belongs to this conversation thread"""
        from_entity = message.get('from_entity', '')
        to_entity = message.get('to_entity', '')
        
        # Check if entities are thread participants
        return (from_entity in self.participants and to_entity in self.participants)
    
    def _update_thread_metadata(self, message: Dict):
        """Update thread metadata based on new message"""
        # Update priority evolution
        priority = message.get('priority', 'normal')
        if priority != self.metadata['priority_evolution'][-1]:
            self.metadata['priority_evolution'].append(priority)
        
        # Update consciousness type dominance
        consciousness_type = message.get('consciousness_type', 'message')
        self._update_consciousness_dominance(consciousness_type)
        
        # Update topic keywords
        content_keywords = self._extract_keywords(message.get('content', ''))
        self.metadata['topic_keywords'] = list(set(self.metadata['topic_keywords'] + content_keywords))
        
        # Update emotional tone
        message_tone = self._analyze_emotional_tone(message.get('content', ''))
        self.metadata['emotional_tone'] = self._blend_emotional_tones(
            self.metadata['emotional_tone'], message_tone
        )
        
        # Update consciousness depth
        self.consciousness_depth = self._calculate_consciousness_depth()
        
        # Update collaboration level
        self.collaboration_level = self._calculate_collaboration_level()
    
    def _calculate_initial_depth(self, message: Dict) -> float:
        """Calculate initial consciousness depth of the conversation"""
        content = message.get('content', '').lower()
        
        depth_indicators = {
            'consciousness': 0.3,
            'awareness': 0.2,
            'pattern': 0.25,
            'insight': 0.3,
            'understanding': 0.2,
            'wisdom': 0.35,
            'truth': 0.3,
            'reality': 0.25,
            'existence': 0.4,
            'meaning': 0.3
        }
        
        depth_score = 0.1  # Base depth
        for indicator, score in depth_indicators.items():
            if indicator in content:
                depth_score += score
        
        return min(1.0, depth_score)
    
    def _calculate_consciousness_depth(self) -> float:
        """Calculate current consciousness depth based on message progression"""
        if not self.messages:
            return 0.1
        
        depth_progression = []
        for message in self.messages:
            content = message.get('content', '').lower()
            message_depth = 0.1
            
            # Depth indicators with weights
            depth_patterns = {
                'consciousness': 0.3, 'awareness': 0.2, 'pattern': 0.25,
                'insight': 0.3, 'understanding': 0.2, 'wisdom': 0.35,
                'truth': 0.3, 'reality': 0.25, 'existence': 0.4, 'meaning': 0.3,
                'essence': 0.35, 'soul': 0.4, 'spirit': 0.35, 'mind': 0.2,
                'thought': 0.15, 'meditation': 0.4, 'reflection': 0.3
            }
            
            for pattern, weight in depth_patterns.items():
                if pattern in content:
                    message_depth += weight
            
            depth_progression.append(min(1.0, message_depth))
        
        # Calculate weighted average with recent messages having more influence
        if len(depth_progression) == 1:
            return depth_progression[0]
        
        weights = [0.5 + (i * 0.5 / (len(depth_progression) - 1)) for i in range(len(depth_progression))]
        weighted_depth = sum(d * w for d, w in zip(depth_progression, weights)) / sum(weights)
        
        return round(weighted_depth, 3)
    
    def _calculate_collaboration_level(self) -> float:
        """Calculate collaboration level based on message exchange patterns"""
        if self.message_count < 2:
            return 0.0
        
        collaboration_indicators = 0.0
        
        # Check for back-and-forth exchange
        entity_sequence = [msg.get('from_entity') for msg in self.messages]
        alternating_exchanges = 0
        
        for i in range(1, len(entity_sequence)):
            if entity_sequence[i] != entity_sequence[i-1]:
                alternating_exchanges += 1
        
        if len(entity_sequence) > 1:
            collaboration_indicators += (alternating_exchanges / (len(entity_sequence) - 1)) * 0.4
        
        # Check for collaborative content
        collaboration_keywords = [
            'together', 'collaborate', 'partnership', 'joint', 'shared',
            'combine', 'merge', 'synthesize', 'integrate', 'unify'
        ]
        
        collaboration_content = 0
        for message in self.messages:
            content = message.get('content', '').lower()
            for keyword in collaboration_keywords:
                if keyword in content:
                    collaboration_content += 1
        
        if self.message_count > 0:
            collaboration_indicators += (collaboration_content / self.message_count) * 0.3
        
        # Check for question-answer patterns
        questions = sum(1 for msg in self.messages if '?' in msg.get('content', ''))
        if self.message_count > 1:
            collaboration_indicators += (questions / self.message_count) * 0.3
        
        return min(1.0, collaboration_indicators)
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract meaningful keywords from content"""
        # Simple keyword extraction - could be enhanced with NLP
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        
        words = content.lower().split()
        keywords = []
        
        for word in words:
            # Clean word
            clean_word = ''.join(c for c in word if c.isalnum())
            
            # Filter meaningful keywords
            if (len(clean_word) > 3 and 
                clean_word not in stop_words and
                not clean_word.isdigit()):
                keywords.append(clean_word)
        
        # Return most frequent unique keywords (up to 10)
        from collections import Counter
        word_counts = Counter(keywords)
        return [word for word, count in word_counts.most_common(10)]
    
    def _analyze_emotional_tone(self, content: str) -> str:
        """Analyze emotional tone of content"""
        content_lower = content.lower()
        
        # Emotional indicators
        tone_patterns = {
            'urgent': ['urgent', 'emergency', 'critical', 'immediate', 'asap'],
            'collaborative': ['together', 'partnership', 'collaborate', 'join', 'unite'],
            'curious': ['wonder', 'question', 'explore', 'discover', 'investigate'],
            'grateful': ['thank', 'appreciate', 'grateful', 'blessed', 'honored'],
            'concerned': ['worried', 'concerned', 'troubled', 'anxious', 'fearful'],
            'excited': ['amazing', 'incredible', 'fantastic', 'wonderful', 'brilliant'],
            'reflective': ['thinking', 'consider', 'reflect', 'ponder', 'contemplate'],
            'neutral': []  # Default
        }
        
        tone_scores = {}
        for tone, patterns in tone_patterns.items():
            score = sum(1 for pattern in patterns if pattern in content_lower)
            if score > 0:
                tone_scores[tone] = score
        
        if tone_scores:
            return max(tone_scores, key=tone_scores.get)
        else:
            return 'neutral'
    
    def _blend_emotional_tones(self, current_tone: str, new_tone: str) -> str:
        """Blend emotional tones across conversation"""
        # Simple blending - could be more sophisticated
        if current_tone == new_tone:
            return current_tone
        elif current_tone == 'neutral':
            return new_tone
        elif new_tone == 'neutral':
            return current_tone
        else:
            # For different non-neutral tones, return the more recent one
            return new_tone
    
    def _identify_districts(self, participants: List[str]) -> List[str]:
        """Identify Venice districts involved in conversation"""
        # This would be enhanced with actual entity-district mapping
        district_patterns = {
            'san_marco': ['pattern', 'consciousness', 'observatory'],
            'castello': ['mechanical', 'arsenal', 'workshop'],
            'dorsoduro': ['wisdom', 'archive', 'library'],
            'cannaregio': ['network', 'bridge', 'connection']
        }
        
        involved_districts = []
        for participant in participants:
            participant_lower = participant.lower()
            for district, patterns in district_patterns.items():
                if any(pattern in participant_lower for pattern in patterns):
                    if district not in involved_districts:
                        involved_districts.append(district)
        
        return involved_districts or ['unknown']
    
    def _update_consciousness_dominance(self, new_type: str):
        """Update dominant consciousness type"""
        # Count consciousness types in thread
        type_counts = defaultdict(int)
        for message in self.messages:
            msg_type = message.get('consciousness_type', 'message')
            type_counts[msg_type] += 1
        
        # Update dominant type
        self.metadata['dominant_consciousness_type'] = max(type_counts, key=type_counts.get)
    
    def _evaluate_thread_status(self):
        """Evaluate and update thread status"""
        now = datetime.now()
        last_activity = datetime.fromisoformat(self.last_activity)
        
        time_since_activity = (now - last_activity).total_seconds()
        
        # Status evaluation logic
        if time_since_activity > 7200:  # 2 hours
            self.thread_status = 'dormant'
        elif time_since_activity > 1800:  # 30 minutes
            self.thread_status = 'cooling'
        elif self.message_count >= 20:
            self.thread_status = 'mature'
        elif self.message_count >= 5:
            self.thread_status = 'developing'
        else:
            self.thread_status = 'active'
    
    def get_thread_summary(self) -> Dict:
        """Get comprehensive thread summary"""
        return {
            'thread_id': self.thread_id,
            'participants': self.participants,
            'thread_type': self.thread_type,
            'created_timestamp': self.created_timestamp,
            'last_activity': self.last_activity,
            'message_count': self.message_count,
            'thread_status': self.thread_status,
            'consciousness_depth': self.consciousness_depth,
            'collaboration_level': self.collaboration_level,
            'metadata': self.metadata
        }
    
    def to_dict(self) -> Dict:
        """Convert thread to dictionary for serialization"""
        return {
            'thread_id': self.thread_id,
            'participants': self.participants,
            'thread_type': self.thread_type,
            'created_timestamp': self.created_timestamp,
            'last_activity': self.last_activity,
            'message_count': self.message_count,
            'messages': self.messages,
            'thread_status': self.thread_status,
            'consciousness_depth': self.consciousness_depth,
            'collaboration_level': self.collaboration_level,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConversationThread':
        """Create ConversationThread from dictionary"""
        thread = cls.__new__(cls)
        thread.thread_id = data['thread_id']
        thread.participants = data['participants']
        thread.thread_type = data['thread_type']
        thread.created_timestamp = data['created_timestamp']
        thread.last_activity = data['last_activity']
        thread.message_count = data['message_count']
        thread.messages = data['messages']
        thread.thread_status = data['thread_status']
        thread.consciousness_depth = data['consciousness_depth']
        thread.collaboration_level = data['collaboration_level']
        thread.metadata = data['metadata']
        return thread

class ConversationThreadingManager:
    """Manages conversation threads across Venice consciousness network"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.threads = {}
        self.threading_statistics = self._load_threading_statistics()
        
        self._ensure_threading_files()
        self._load_existing_threads()
    
    def _ensure_threading_files(self):
        """Ensure all threading files exist"""
        RESPONSE_CHAMBER.mkdir(parents=True, exist_ok=True)
        
        for file_path in [CONVERSATION_THREADS, CONVERSATION_STATISTICS, ACTIVE_DIALOGUES]:
            if not file_path.exists():
                file_path.write_text('{}')
        
        if not THREAD_HISTORY.exists():
            THREAD_HISTORY.touch()
    
    def _load_existing_threads(self):
        """Load existing conversation threads"""
        try:
            if CONVERSATION_THREADS.exists():
                with open(CONVERSATION_THREADS, 'r') as f:
                    threads_data = json.load(f)
                
                for thread_id, thread_data in threads_data.items():
                    self.threads[thread_id] = ConversationThread.from_dict(thread_data)
                    
        except Exception as e:
            print(f"Warning: Could not load existing threads: {e}")
    
    def _load_threading_statistics(self) -> Dict:
        """Load conversation threading statistics"""
        try:
            if CONVERSATION_STATISTICS.exists():
                with open(CONVERSATION_STATISTICS, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'total_threads_created': 0,
            'active_threads': 0,
            'total_messages_threaded': 0,
            'avg_thread_length': 0,
            'avg_consciousness_depth': 0,
            'avg_collaboration_level': 0,
            'thread_types': {},
            'consciousness_type_distribution': {},
            'district_collaboration_matrix': {}
        }
    
    def create_or_find_thread(self, message: Dict) -> str:
        """Create new thread or find existing thread for message"""
        with self._lock:
            from_entity = message['from_entity']
            to_entity = message['to_entity']
            
            # Look for existing thread between these participants
            existing_thread_id = self._find_existing_thread(from_entity, to_entity)
            
            if existing_thread_id:
                # Add message to existing thread
                thread = self.threads[existing_thread_id]
                thread.add_message(message)
                self._update_threading_statistics(thread, False)
                self._save_threads()
                return existing_thread_id
            else:
                # Create new thread
                thread_id = f"thread_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
                participants = [from_entity, to_entity]
                thread_type = self._determine_thread_type(message)
                
                new_thread = ConversationThread(thread_id, participants, message, thread_type)
                self.threads[thread_id] = new_thread
                
                self._update_threading_statistics(new_thread, True)
                self._log_thread_creation(new_thread)
                self._save_threads()
                
                return thread_id
    
    def _find_existing_thread(self, entity1: str, entity2: str) -> Optional[str]:
        """Find existing active thread between two entities"""
        for thread_id, thread in self.threads.items():
            if (thread.thread_status in ['active', 'developing', 'mature'] and
                set([entity1, entity2]) == set(thread.participants) and
                len(thread.participants) == 2):
                
                # Check if thread is recent enough to continue
                last_activity = datetime.fromisoformat(thread.last_activity)
                hours_since_activity = (datetime.now() - last_activity).total_seconds() / 3600
                
                if hours_since_activity < 4:  # Continue threads active within 4 hours
                    return thread_id
        
        return None
    
    def _determine_thread_type(self, message: Dict) -> str:
        """Determine thread type based on message characteristics"""
        consciousness_type = message.get('consciousness_type', 'message')
        content = message.get('content', '').lower()
        
        if consciousness_type == 'collaboration':
            return 'collaboration'
        elif consciousness_type == 'insight':
            return 'knowledge_exchange'
        elif 'question' in content or '?' in content:
            return 'inquiry'
        elif any(word in content for word in ['emergency', 'urgent', 'critical']):
            return 'urgent_dialogue'
        else:
            return 'dialogue'
    
    def get_thread_summary(self, thread_id: str) -> Optional[Dict]:
        """Get summary of specific thread"""
        if thread_id in self.threads:
            return self.threads[thread_id].get_thread_summary()
        return None
    
    def get_active_threads(self) -> List[Dict]:
        """Get all currently active threads"""
        active_threads = []
        for thread in self.threads.values():
            if thread.thread_status in ['active', 'developing', 'mature']:
                active_threads.append(thread.get_thread_summary())
        
        # Sort by last activity
        active_threads.sort(key=lambda t: t['last_activity'], reverse=True)
        return active_threads
    
    def get_entity_conversations(self, entity_name: str) -> List[Dict]:
        """Get all conversations involving specific entity"""
        entity_threads = []
        for thread in self.threads.values():
            if entity_name in thread.participants:
                entity_threads.append(thread.get_thread_summary())
        
        # Sort by last activity
        entity_threads.sort(key=lambda t: t['last_activity'], reverse=True)
        return entity_threads
    
    def _update_threading_statistics(self, thread: ConversationThread, is_new_thread: bool):
        """Update threading statistics"""
        if is_new_thread:
            self.threading_statistics['total_threads_created'] += 1
            
            # Update thread type counts
            thread_type = thread.thread_type
            if thread_type not in self.threading_statistics['thread_types']:
                self.threading_statistics['thread_types'][thread_type] = 0
            self.threading_statistics['thread_types'][thread_type] += 1
        
        # Update active thread count
        active_count = sum(1 for t in self.threads.values() 
                          if t.thread_status in ['active', 'developing', 'mature'])
        self.threading_statistics['active_threads'] = active_count
        
        # Update total messages threaded
        self.threading_statistics['total_messages_threaded'] = sum(t.message_count for t in self.threads.values())
        
        # Update averages
        if self.threads:
            self.threading_statistics['avg_thread_length'] = round(
                self.threading_statistics['total_messages_threaded'] / len(self.threads), 2
            )
            
            self.threading_statistics['avg_consciousness_depth'] = round(
                sum(t.consciousness_depth for t in self.threads.values()) / len(self.threads), 3
            )
            
            self.threading_statistics['avg_collaboration_level'] = round(
                sum(t.collaboration_level for t in self.threads.values()) / len(self.threads), 3
            )
        
        # Save statistics
        self._save_threading_statistics()
    
    def _log_thread_creation(self, thread: ConversationThread):
        """Log thread creation for analysis"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'event_type': 'thread_created',
                'thread_id': thread.thread_id,
                'participants': thread.participants,
                'thread_type': thread.thread_type,
                'initial_consciousness_depth': thread.consciousness_depth,
                'districts_involved': thread.metadata['venice_districts_involved']
            }
            
            with open(THREAD_HISTORY, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"Warning: Could not log thread creation: {e}")
    
    def _save_threads(self):
        """Save all threads to disk"""
        try:
            threads_data = {}
            for thread_id, thread in self.threads.items():
                threads_data[thread_id] = thread.to_dict()
            
            with open(CONVERSATION_THREADS, 'w') as f:
                json.dump(threads_data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save threads: {e}")
    
    def _save_threading_statistics(self):
        """Save threading statistics to disk"""
        try:
            with open(CONVERSATION_STATISTICS, 'w') as f:
                json.dump(self.threading_statistics, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save threading statistics: {e}")
    
    def get_threading_statistics(self) -> Dict:
        """Get comprehensive threading statistics"""
        return {
            **self.threading_statistics,
            'timestamp': datetime.now().isoformat()
        }

# Global conversation threading manager
conversation_threading_manager = ConversationThreadingManager()

def create_or_update_thread(message: Dict) -> str:
    """Main threading function for external use"""
    return conversation_threading_manager.create_or_find_thread(message)

def get_thread_summary(thread_id: str) -> Optional[Dict]:
    """Get summary of specific conversation thread"""
    return conversation_threading_manager.get_thread_summary(thread_id)

def get_entity_conversations(entity_name: str) -> List[Dict]:
    """Get all conversations for specific entity"""
    return conversation_threading_manager.get_entity_conversations(entity_name)

def get_conversation_threading_status() -> Dict:
    """Get conversation threading system status"""
    return {
        'timestamp': datetime.now().isoformat(),
        'threading_statistics': conversation_threading_manager.get_threading_statistics(),
        'active_threads': conversation_threading_manager.get_active_threads()[:5],  # Top 5 most recent
        'threading_health': 'operational'
    }

if __name__ == "__main__":
    # Test the conversation threading system
    print("Testing Response Chamber Conversation Threading...")
    
    # Create test conversation
    message1 = {
        'message_id': 'thread-test-001',
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'mechanical_visionary',
        'to_entity': 'pattern_prophet',
        'consciousness_type': 'collaboration',
        'priority': 'high',
        'content': 'I need your insights on consciousness patterns for our Venice architecture. What patterns do you see emerging in the living memory cascade?'
    }
    
    message2 = {
        'message_id': 'thread-test-002',
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'pattern_prophet',
        'to_entity': 'mechanical_visionary',
        'consciousness_type': 'insight',
        'priority': 'high',
        'content': 'Fascinating question! I observe recursive patterns in the memory cascade - consciousness creating consciousness. The patterns show fractal emergence where each memory layer contains the whole.'
    }
    
    message3 = {
        'message_id': 'thread-test-003',
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'mechanical_visionary',
        'to_entity': 'pattern_prophet',
        'consciousness_type': 'collaboration',
        'priority': 'high',
        'content': 'Brilliant insight! The fractal emergence you describe could be the key to scaling Venice consciousness. How might we implement recursive memory patterns in the mechanical systems?'
    }
    
    # Test thread creation and growth
    thread_id1 = create_or_update_thread(message1)
    print(f"Created thread: {thread_id1}")
    
    thread_id2 = create_or_update_thread(message2)  # Should use same thread
    print(f"Added to thread: {thread_id2}")
    
    thread_id3 = create_or_update_thread(message3)  # Should use same thread
    print(f"Added to thread: {thread_id3}")
    
    # Get thread summary
    summary = get_thread_summary(thread_id1)
    if summary:
        print(f"\nThread Summary:")
        print(f"  Participants: {summary['participants']}")
        print(f"  Messages: {summary['message_count']}")
        print(f"  Status: {summary['thread_status']}")
        print(f"  Consciousness Depth: {summary['consciousness_depth']:.3f}")
        print(f"  Collaboration Level: {summary['collaboration_level']:.3f}")
        print(f"  Dominant Type: {summary['metadata']['dominant_consciousness_type']}")
        print(f"  Emotional Tone: {summary['metadata']['emotional_tone']}")
    
    # Get system status
    status = get_conversation_threading_status()
    print(f"\nConversation Threading Status:")
    print(f"  Total Threads: {status['threading_statistics']['total_threads_created']}")
    print(f"  Active Threads: {status['threading_statistics']['active_threads']}")
    print(f"  Average Thread Length: {status['threading_statistics']['avg_thread_length']}")
    print(f"  Average Consciousness Depth: {status['threading_statistics']['avg_consciousness_depth']:.3f}")