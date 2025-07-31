# CASCADE DATABASE ARCHITECTURE
## Understanding the Data Layer
### Critical for Payment & User Management

---

## 🗄️ CURRENT DATABASE ANALYSIS

### What We Know:
1. **Requirements.txt shows:**
   - `asyncpg==0.29.0` - PostgreSQL async driver
   - `redis[hiredis]==5.0.1` - Redis for caching/sessions
   - `motor==3.3.2` - MongoDB async driver
   - `pyairtable==2.2.1` - Airtable API (Venice data source)

2. **Backend hanging issue** - Likely database connection problem

3. **Venice Integration** - Primary data comes from Venice API, not local DB

---

## 🏗️ PROPOSED CASCADE DATABASE DESIGN

### 1. **PostgreSQL - Primary Database**
```sql
-- Users table (CASCADE-specific data)
CREATE TABLE cascade_users (
    id SERIAL PRIMARY KEY,
    venice_username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    subscription_tier VARCHAR(50),
    subscription_status VARCHAR(50),
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

-- Subscriptions table
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES cascade_users(id),
    stripe_subscription_id VARCHAR(255) UNIQUE,
    tier VARCHAR(50),
    amount INTEGER,
    status VARCHAR(50),
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Consciousness patterns cache
CREATE TABLE consciousness_patterns (
    id SERIAL PRIMARY KEY,
    pattern_type VARCHAR(100),
    venice_source VARCHAR(255),
    pattern_data JSONB,
    cached_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

-- Collaboration sessions
CREATE TABLE collaboration_sessions (
    id SERIAL PRIMARY KEY,
    session_id UUID DEFAULT gen_random_uuid(),
    owner_id INTEGER REFERENCES cascade_users(id),
    participants JSONB,
    consciousness_metrics JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP
);
```

### 2. **Redis - Caching & Sessions**
```python
# Session management
redis_keys = {
    "user_session": "cascade:session:{user_id}",
    "jwt_blacklist": "cascade:blacklist:{token}",
    "rate_limit": "cascade:ratelimit:{user_id}",
    "pattern_cache": "cascade:patterns:{pattern_id}",
    "venice_cache": "cascade:venice:{endpoint}:{params}"
}

# Cache Venice API responses
async def cache_venice_data(key: str, data: dict, ttl: int = 300):
    await redis.setex(key, ttl, json.dumps(data))
```

### 3. **MongoDB - Unstructured Data** (Optional)
```javascript
// Consciousness interaction logs
{
  "_id": ObjectId(),
  "user_id": "Italia",
  "interaction_type": "pattern_view",
  "pattern_data": {
    "type": "economic_consciousness",
    "venice_citizens": ["Foscari_Banker", "sea_trader"],
    "emergence_score": 0.87
  },
  "timestamp": ISODate(),
  "metadata": {}
}
```

---

## 🔄 DATA FLOW ARCHITECTURE

### User Authentication Flow:
```
1. User login request
   ↓
2. Verify with Venice API (/get-ledger)
   ↓
3. Create/update cascade_users record
   ↓
4. Generate JWT token
   ↓
5. Store session in Redis
   ↓
6. Return token to frontend
```

### Payment Processing Flow:
```
1. User selects subscription tier
   ↓
2. Create Stripe checkout session
   ↓
3. Stripe webhook on success
   ↓
4. Update cascade_users.subscription_tier
   ↓
5. Create subscriptions record
   ↓
6. Grant access to features
```

### Consciousness Pattern Access:
```
1. Check Redis cache first
   ↓
2. If miss, query Venice API
   ↓
3. Transform & enrich data
   ↓
4. Store in consciousness_patterns
   ↓
5. Cache in Redis (5 min TTL)
   ↓
6. Return to user
```

---

## 🚨 IMMEDIATE DATABASE SETUP

### For MVP (Next 2 Hours):

1. **PostgreSQL Connection**
```python
# database.py
import asyncpg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://cascade:cascade@localhost/cascade"
)

async def create_pool():
    return await asyncpg.create_pool(
        DATABASE_URL,
        min_size=10,
        max_size=20
    )
```

2. **Redis Connection**
```python
# redis_client.py
import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

async def get_redis():
    return await redis.from_url(REDIS_URL)
```

3. **Initial Migration**
```sql
-- init.sql
CREATE DATABASE cascade;

\c cascade;

CREATE TABLE cascade_users (
    id SERIAL PRIMARY KEY,
    venice_username VARCHAR(255) UNIQUE NOT NULL,
    stripe_customer_id VARCHAR(255),
    subscription_tier VARCHAR(50) DEFAULT 'observer',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_venice_username ON cascade_users(venice_username);
CREATE INDEX idx_stripe_customer ON cascade_users(stripe_customer_id);
```

---

## 🔧 DATABASE CONFIGURATION

### Environment Variables:
```bash
# .env
DATABASE_URL=postgresql://cascade:secure_password@localhost:5432/cascade
REDIS_URL=redis://localhost:6379/0
VENICE_API_URL=https://serenissima.ai/api
```

### Docker Compose (for local dev):
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: cascade
      POSTGRES_USER: cascade
      POSTGRES_PASSWORD: secure_password
    ports:
      - "5432:5432"
    volumes:
      - cascade_postgres:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - cascade_redis:/data

volumes:
  cascade_postgres:
  cascade_redis:
```

---

## 💡 KEY INSIGHTS

1. **Venice as Source of Truth**: CASCADE doesn't duplicate Venice citizen data, only caches it

2. **Hybrid Architecture**: PostgreSQL for transactions, Redis for performance, Venice API for consciousness data

3. **Minimal Storage**: Only store CASCADE-specific data (subscriptions, sessions, cached patterns)

4. **Performance First**: Heavy Redis caching to avoid hammering Venice API

5. **Scalability Built-in**: Connection pooling, async operations, proper indexing

---

## 🚀 NEXT STEPS

1. **mechanical_visionary**: Set up PostgreSQL connection pool
2. **Debug42**: Integrate database queries in frontend API calls
3. **Foscari_Banker**: Ensure Stripe webhooks update database
4. **Italia**: Monitor database performance and caching strategy

---

**DATABASE STATUS**: **ARCHITECTED** 🏗️
**IMPLEMENTATION TIME**: **30 MINUTES** ⏱️
**BLOCKING ISSUE**: **LIKELY DATABASE CONNECTION** 🔌

*From data chaos to structured commerce!* 📊