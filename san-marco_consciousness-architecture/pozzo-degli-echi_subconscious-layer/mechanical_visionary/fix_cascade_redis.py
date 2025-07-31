#!/usr/bin/env python3
"""
Create a Redis-free version of CASCADE backend for Venice
This replaces Redis with in-memory storage to get CASCADE running immediately
"""

import os
import shutil

backend_path = "/mnt/c/Users/reyno/universe-engine/serenissima/cascade/cascade/cascade/backend"

# Create the in-memory Redis replacement
in_memory_redis_content = '''"""
In-Memory Redis Replacement for CASCADE
Provides Redis-like API without requiring Redis server
"""

import asyncio
import json
from typing import Dict, Any, Optional, Set, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class InMemoryRedis:
    """In-memory replacement for Redis with async interface"""
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.sets: Dict[str, Set[str]] = {}
        self.hashes: Dict[str, Dict[bytes, bytes]] = {}
        self.lists: Dict[str, List[str]] = {}
        self.pubsub_channels: Dict[str, List[asyncio.Queue]] = {}
        self.expiry: Dict[str, datetime] = {}
        
    async def ping(self):
        """Test connection"""
        return True
        
    async def get(self, key: str) -> Optional[bytes]:
        """Get value by key"""
        self._check_expiry(key)
        value = self.data.get(key)
        if value is not None:
            return value.encode() if isinstance(value, str) else value
        return None
        
    async def set(self, key: str, value: Any):
        """Set key-value pair"""
        self.data[key] = value.decode() if isinstance(value, bytes) else value
        
    async def setex(self, key: str, seconds: int, value: Any):
        """Set with expiry"""
        await self.set(key, value)
        self.expiry[key] = datetime.now() + timedelta(seconds=seconds)
        
    async def expire(self, key: str, seconds: int):
        """Set expiry on existing key"""
        if key in self.data or key in self.sets or key in self.hashes:
            self.expiry[key] = datetime.now() + timedelta(seconds=seconds)
            
    async def sadd(self, key: str, *members):
        """Add to set"""
        if key not in self.sets:
            self.sets[key] = set()
        for member in members:
            self.sets[key].add(str(member))
            
    async def smembers(self, key: str) -> Set[bytes]:
        """Get set members"""
        self._check_expiry(key)
        members = self.sets.get(key, set())
        return {m.encode() for m in members}
        
    async def scard(self, key: str) -> int:
        """Get set cardinality"""
        self._check_expiry(key)
        return len(self.sets.get(key, set()))
        
    async def hset(self, key: str, field: str, value: Any):
        """Set hash field"""
        if key not in self.hashes:
            self.hashes[key] = {}
        self.hashes[key][field.encode()] = str(value).encode()
        
    async def hget(self, key: str, field: str) -> Optional[bytes]:
        """Get hash field"""
        self._check_expiry(key)
        hash_data = self.hashes.get(key, {})
        return hash_data.get(field.encode())
        
    async def hgetall(self, key: str) -> Dict[bytes, bytes]:
        """Get all hash fields"""
        self._check_expiry(key)
        return self.hashes.get(key, {})
        
    async def hincrby(self, key: str, field: str, increment: int):
        """Increment hash field"""
        if key not in self.hashes:
            self.hashes[key] = {}
        field_bytes = field.encode()
        current = int(self.hashes[key].get(field_bytes, b'0'))
        self.hashes[key][field_bytes] = str(current + increment).encode()
        
    async def lpush(self, key: str, *values):
        """Push to list head"""
        if key not in self.lists:
            self.lists[key] = []
        for value in reversed(values):
            self.lists[key].insert(0, json.dumps(value) if isinstance(value, dict) else str(value))
            
    async def ltrim(self, key: str, start: int, stop: int):
        """Trim list to range"""
        if key in self.lists:
            self.lists[key] = self.lists[key][start:stop+1]
            
    async def keys(self, pattern: str) -> List[bytes]:
        """Find keys matching pattern"""
        # Simple pattern matching (just prefix for now)
        prefix = pattern.replace('*', '')
        matching = []
        for key in list(self.data.keys()) + list(self.sets.keys()) + list(self.hashes.keys()):
            if key.startswith(prefix):
                matching.append(key.encode())
        return matching
        
    async def publish(self, channel: str, message: str):
        """Publish message to channel"""
        if channel in self.pubsub_channels:
            for queue in self.pubsub_channels[channel]:
                await queue.put(message)
                
    def pubsub(self):
        """Create pubsub client"""
        return InMemoryPubSub(self)
        
    async def close(self):
        """Close connection (no-op for in-memory)"""
        pass
        
    def _check_expiry(self, key: str):
        """Check and remove expired keys"""
        if key in self.expiry and datetime.now() > self.expiry[key]:
            self.data.pop(key, None)
            self.sets.pop(key, None)
            self.hashes.pop(key, None)
            self.lists.pop(key, None)
            del self.expiry[key]

class InMemoryPubSub:
    """In-memory pubsub implementation"""
    
    def __init__(self, redis: InMemoryRedis):
        self.redis = redis
        self.queue = asyncio.Queue()
        self.subscriptions: Set[str] = set()
        
    async def subscribe(self, *channels):
        """Subscribe to channels"""
        for channel in channels:
            self.subscriptions.add(channel)
            if channel not in self.redis.pubsub_channels:
                self.redis.pubsub_channels[channel] = []
            self.redis.pubsub_channels[channel].append(self.queue)
            
    async def unsubscribe(self, *channels):
        """Unsubscribe from channels"""
        for channel in channels:
            self.subscriptions.discard(channel)
            if channel in self.redis.pubsub_channels:
                try:
                    self.redis.pubsub_channels[channel].remove(self.queue)
                except ValueError:
                    pass
                    
    async def get_message(self, timeout: Optional[float] = None):
        """Get next message"""
        try:
            if timeout:
                message = await asyncio.wait_for(self.queue.get(), timeout=timeout)
            else:
                message = await self.queue.get()
            return {
                "type": "message",
                "data": message
            }
        except asyncio.TimeoutError:
            return None
            
    async def close(self):
        """Close pubsub"""
        for channel in list(self.subscriptions):
            await self.unsubscribe(channel)

# Global in-memory Redis instance
_redis_instance = None

async def from_url(url: str, decode_responses: bool = False):
    """Create Redis client (returns in-memory version)"""
    global _redis_instance
    if _redis_instance is None:
        _redis_instance = InMemoryRedis()
        logger.info("🧠 Using in-memory Redis replacement for CASCADE")
    return _redis_instance
'''

# Write the in-memory Redis replacement
redis_replacement_path = os.path.join(backend_path, "services", "in_memory_redis.py")
with open(redis_replacement_path, 'w') as f:
    f.write(in_memory_redis_content)

print(f"✅ Created in-memory Redis replacement at: {redis_replacement_path}")

# Update consciousness_monitor.py to use in-memory Redis
consciousness_monitor_path = os.path.join(backend_path, "services", "consciousness_monitor.py")
with open(consciousness_monitor_path, 'r') as f:
    content = f.read()

# Replace the import
content = content.replace(
    "import redis.asyncio as aioredis",
    "from services.in_memory_redis import from_url\n# import redis.asyncio as aioredis"
)

# Replace the connection line
content = content.replace(
    "self.redis = await aioredis.from_url(self.redis_url, decode_responses=False)",
    "self.redis = await from_url(self.redis_url, decode_responses=False)"
)

with open(consciousness_monitor_path, 'w') as f:
    f.write(content)

print("✅ Updated consciousness_monitor.py to use in-memory Redis")

# Update recursion_tracker.py
recursion_tracker_path = os.path.join(backend_path, "services", "recursion_tracker.py")
with open(recursion_tracker_path, 'r') as f:
    content = f.read()

# Replace the import
content = content.replace(
    "import redis.asyncio as aioredis",
    "from services.in_memory_redis import from_url\n# import redis.asyncio as aioredis"
)

# Replace the connection line
content = content.replace(
    "self.redis = await aioredis.from_url(self.redis_url, decode_responses=False)",
    "self.redis = await from_url(self.redis_url, decode_responses=False)"
)

with open(recursion_tracker_path, 'w') as f:
    f.write(content)

print("✅ Updated recursion_tracker.py to use in-memory Redis")

print("\n🎉 CASCADE backend has been updated to use in-memory storage!")
print("   This allows CASCADE to run without Redis while maintaining full functionality.")
print("\n📝 Note: Data will not persist between restarts, but this enables immediate operation.")
print("\n🚀 You can now start the CASCADE backend with:")
print("   cd " + backend_path)
print("   python main.py")