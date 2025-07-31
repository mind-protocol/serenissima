# CASCADE Third-Party Integration API
## Enterprise Platform API Specification v1.0

*Engineering seamless connections with systematic precision*

## Overview

The CASCADE Third-Party API enables external applications to integrate with the CASCADE platform, providing secure access to workrooms, resources, and collaboration features while maintaining complete tenant isolation.

## Authentication

### API Key Authentication
```http
GET /api/v1/resources
Authorization: Bearer {API_KEY}
X-Tenant-ID: {TENANT_ID}
```

### OAuth 2.0 Flow
```python
# OAuth endpoints
authorization_url = "https://cascade.serenissima.ai/oauth/authorize"
token_url = "https://cascade.serenissima.ai/oauth/token"
```

### JWT Token Structure
```json
{
  "sub": "user_id",
  "tenant_id": "tenant_uuid",
  "scopes": ["workrooms:read", "resources:write"],
  "exp": 1739894400,
  "iat": 1736864000,
  "jti": "unique_token_id"
}
```

## Core API Endpoints

### Workroom Management

#### List Workrooms
```http
GET /api/v1/workrooms
Authorization: Bearer {token}
X-Tenant-ID: {tenant_id}

Response:
{
  "data": [
    {
      "id": "workroom_uuid",
      "name": "Strategic Planning",
      "description": "Q3 2025 planning discussions",
      "created_at": "2025-07-15T10:00:00Z",
      "member_count": 12,
      "last_activity": "2025-07-15T14:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 45
  }
}
```

#### Create Workroom
```http
POST /api/v1/workrooms
Authorization: Bearer {token}
X-Tenant-ID: {tenant_id}
Content-Type: application/json

{
  "name": "Project Alpha",
  "description": "New product development",
  "visibility": "private",
  "members": ["user_id_1", "user_id_2"],
  "settings": {
    "allow_guests": false,
    "retention_days": 90
  }
}

Response:
{
  "id": "workroom_uuid",
  "name": "Project Alpha",
  "invite_link": "https://cascade.ai/join/abc123",
  "created_at": "2025-07-15T14:15:00Z"
}
```

### Resource Management

#### Upload Resource
```http
POST /api/v1/resources
Authorization: Bearer {token}
X-Tenant-ID: {tenant_id}
Content-Type: multipart/form-data

file: (binary)
workroom_id: workroom_uuid
metadata: {"tags": ["design", "v2"], "version": "1.0"}

Response:
{
  "id": "resource_uuid",
  "filename": "design_mockup_v2.pdf",
  "size_bytes": 2048576,
  "mime_type": "application/pdf",
  "download_url": "https://cascade.ai/api/v1/resources/resource_uuid/download",
  "created_at": "2025-07-15T14:20:00Z"
}
```

#### Search Resources
```http
GET /api/v1/resources/search?q=mockup&tags=design&workroom_id=workroom_uuid
Authorization: Bearer {token}
X-Tenant-ID: {tenant_id}

Response:
{
  "data": [
    {
      "id": "resource_uuid",
      "filename": "design_mockup_v2.pdf",
      "relevance_score": 0.95,
      "highlights": ["design <em>mockup</em> v2"],
      "workroom": {
        "id": "workroom_uuid",
        "name": "Project Alpha"
      }
    }
  ],
  "total_results": 12
}
```

### Real-time Collaboration

#### WebSocket Connection
```javascript
const ws = new WebSocket('wss://cascade.ai/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'bearer_token',
    tenant_id: 'tenant_uuid'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  switch(data.type) {
    case 'workroom_update':
      handleWorkroomUpdate(data.payload);
      break;
    case 'new_message':
      handleNewMessage(data.payload);
      break;
  }
};
```

#### Send Message
```http
POST /api/v1/workrooms/{workroom_id}/messages
Authorization: Bearer {token}
X-Tenant-ID: {tenant_id}
Content-Type: application/json

{
  "content": "Updated the design mockups in the resources folder",
  "mentions": ["@user_id_1"],
  "attachments": ["resource_uuid"]
}

Response:
{
  "id": "message_uuid",
  "content": "Updated the design mockups in the resources folder",
  "author": {
    "id": "user_id",
    "name": "John Doe"
  },
  "created_at": "2025-07-15T14:25:00Z",
  "reactions": []
}
```

### Analytics API

#### Workroom Analytics
```http
GET /api/v1/analytics/workrooms/{workroom_id}?period=7d
Authorization: Bearer {token}
X-Tenant-ID: {tenant_id}

Response:
{
  "period": {
    "start": "2025-07-08T00:00:00Z",
    "end": "2025-07-15T23:59:59Z"
  },
  "metrics": {
    "total_messages": 342,
    "active_users": 8,
    "resources_shared": 23,
    "average_response_time_minutes": 12.5
  },
  "activity_heatmap": [
    {"hour": 9, "day": "monday", "messages": 45},
    {"hour": 10, "day": "monday", "messages": 52}
  ]
}
```

#### User Activity
```http
GET /api/v1/analytics/users/{user_id}/activity
Authorization: Bearer {token}
X-Tenant-ID: {tenant_id}

Response:
{
  "user_id": "user_uuid",
  "period": "last_30_days",
  "workrooms_active": 5,
  "messages_sent": 127,
  "resources_uploaded": 15,
  "collaboration_score": 0.85
}
```

## Webhooks

### Webhook Configuration
```http
POST /api/v1/webhooks
Authorization: Bearer {token}
X-Tenant-ID: {tenant_id}
Content-Type: application/json

{
  "url": "https://your-app.com/cascade-webhook",
  "events": ["workroom.created", "resource.uploaded", "message.sent"],
  "secret": "your_webhook_secret"
}

Response:
{
  "id": "webhook_uuid",
  "url": "https://your-app.com/cascade-webhook",
  "events": ["workroom.created", "resource.uploaded", "message.sent"],
  "created_at": "2025-07-15T14:30:00Z"
}
```

### Webhook Payload Example
```json
{
  "event": "resource.uploaded",
  "timestamp": "2025-07-15T14:35:00Z",
  "tenant_id": "tenant_uuid",
  "data": {
    "resource_id": "resource_uuid",
    "filename": "quarterly_report.pdf",
    "workroom_id": "workroom_uuid",
    "uploaded_by": "user_uuid"
  }
}
```

### Webhook Security
```python
# Verify webhook signature
import hmac
import hashlib

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

## SDK Examples

### Python SDK
```python
from cascade import CascadeClient

client = CascadeClient(
    api_key="your_api_key",
    tenant_id="tenant_uuid"
)

# List workrooms
workrooms = client.workrooms.list()

# Create a workroom
workroom = client.workrooms.create(
    name="Engineering Sprint",
    description="Q3 development tasks"
)

# Upload a resource
with open("design.pdf", "rb") as f:
    resource = client.resources.upload(
        file=f,
        workroom_id=workroom.id,
        tags=["design", "v2"]
    )

# Send a message
message = client.messages.send(
    workroom_id=workroom.id,
    content="Design uploaded for review",
    attachments=[resource.id]
)
```

### JavaScript/TypeScript SDK
```typescript
import { CascadeClient } from '@cascade/sdk';

const client = new CascadeClient({
  apiKey: 'your_api_key',
  tenantId: 'tenant_uuid'
});

// Async/await pattern
async function createWorkroom() {
  const workroom = await client.workrooms.create({
    name: 'Marketing Campaign',
    description: 'Q3 2025 campaign planning'
  });
  
  // Real-time updates
  client.on('workroom:update', (data) => {
    console.log('Workroom updated:', data);
  });
  
  return workroom;
}

// Upload with progress
const upload = client.resources.upload({
  file: fileInput.files[0],
  workroomId: 'workroom_uuid',
  onProgress: (percent) => {
    console.log(`Upload progress: ${percent}%`);
  }
});
```

## Rate Limiting

### Default Limits
- **API Calls**: 1000 requests per minute per tenant
- **Uploads**: 100 MB per file, 1 GB per hour
- **WebSocket Messages**: 100 messages per minute per connection
- **Search Queries**: 100 per minute

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1739894400
```

### Handling Rate Limits
```python
import time

def make_request_with_retry(client, request_func):
    while True:
        try:
            return request_func()
        except RateLimitError as e:
            wait_time = e.reset_time - time.time()
            if wait_time > 0:
                time.sleep(wait_time)
            continue
```

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource does not exist",
    "details": {
      "resource_id": "invalid_uuid"
    },
    "request_id": "req_abc123"
  }
}
```

### Common Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Invalid or missing authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMITED` | 429 | Too many requests |
| `INVALID_REQUEST` | 400 | Malformed request |
| `TENANT_QUOTA_EXCEEDED` | 402 | Tenant limit reached |
| `SERVER_ERROR` | 500 | Internal server error |

## Security Best Practices

### API Key Management
1. **Rotate keys regularly** - Every 90 days minimum
2. **Use environment variables** - Never commit keys to code
3. **Implement key scoping** - Limit permissions per integration
4. **Monitor key usage** - Track unusual patterns

### Data Protection
```python
# Always use HTTPS
api_url = "https://cascade.ai/api/v1"

# Encrypt sensitive data
from cryptography.fernet import Fernet

def encrypt_sensitive_data(data: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()
```

## Testing

### Test Environment
```
Base URL: https://sandbox.cascade.ai/api/v1
Test Tenant ID: test_tenant_uuid
Test API Key: test_sk_abc123
```

### Integration Testing
```python
import pytest
from cascade import CascadeClient

@pytest.fixture
def test_client():
    return CascadeClient(
        api_key="test_sk_abc123",
        tenant_id="test_tenant_uuid",
        base_url="https://sandbox.cascade.ai/api/v1"
    )

def test_workroom_creation(test_client):
    workroom = test_client.workrooms.create(
        name="Test Workroom"
    )
    assert workroom.id is not None
    assert workroom.name == "Test Workroom"
```

## Migration Guide

### Migrating from v0.9 to v1.0
```python
# Old (v0.9)
client.create_workroom(name="Project")

# New (v1.0)
client.workrooms.create(name="Project")

# Old (v0.9) - Single tenant
client = CascadeClient(api_key="key")

# New (v1.0) - Multi-tenant
client = CascadeClient(
    api_key="key",
    tenant_id="tenant_uuid"
)
```

## Support

### API Status
- Status Page: https://status.cascade.ai
- API Health: GET https://cascade.ai/api/v1/health

### Developer Resources
- Documentation: https://docs.cascade.ai
- API Reference: https://api.cascade.ai/docs
- SDKs: https://github.com/cascade-platform
- Support: api-support@cascade-collective.ai

*API engineered for seamless integration. Every endpoint optimized for efficiency.*