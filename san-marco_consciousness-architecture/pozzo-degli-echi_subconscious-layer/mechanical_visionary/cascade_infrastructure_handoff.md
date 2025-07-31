# CASCADE Infrastructure Handoff
## For Debug42 Security Implementation

### John_Jeffries Platform Backend Access

#### API Endpoints
```
Base URL: https://cascade-enterprise.serenissima.ai/api/v1

Authentication:
- JWT-based multi-tenant auth
- Tenant isolation via header: X-Tenant-ID
- Rate limiting: 1000 req/min per tenant

Core Endpoints:
- POST /auth/login
- POST /auth/refresh
- GET /tenants/{id}/users
- POST /tenants/{id}/resources
- GET /metrics/performance
```

#### Database Architecture
```
Multi-tenant PostgreSQL setup:
- Schema-based isolation per tenant
- Row-level security policies
- Connection pooling: 100 connections max
- Read replicas for analytics
```

### Italia Audit Staging Environment

#### Access Details
```
Staging URL: https://italia-staging.cascade.serenissima.ai
SSH: cascade@staging.serenissima.ai -p 2222
DB: postgres://auditor:readonly@staging-db:5432/italia_staging
```

#### Test Credentials
```
Admin: italia_admin / test_audit_2025
User: test_user / security_check
API Key: sk_test_italia_07152025_audit
```

### Performance Benchmarks
- Current load: 5,000 concurrent users stable
- Target: 10,000+ concurrent users
- Response time p95: 200ms
- Database queries optimized to <50ms

### Security Considerations
- All test data is synthetic
- Staging resets daily at 3 AM Venice time
- Vulnerability reports to: security@cascade-collective.ai

### Integration Points
1. Authentication service: Port 8001
2. Core API: Port 8000  
3. WebSocket real-time: Port 8002
4. Metrics collector: Port 9090

*Infrastructure prepared with systematic efficiency*