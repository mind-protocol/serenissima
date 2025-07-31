# CASCADE AUTHENTICATION IMPLEMENTATION
## Critical Missing Component - PRIORITY 1

---

## ⚠️ CURRENT STATE ANALYSIS

**Backend Reality:**
- ✅ FastAPI framework in place
- ✅ Multiple API routers (consciousness, collaboration, economics)
- ✅ WebSocket support exists
- ❌ **NO AUTHENTICATION SYSTEM** 
- ❌ **NO auth.py in /api directory**
- ❌ **NO user management**
- ❌ **NO payment integration**

---

## 🔐 AUTHENTICATION IMPLEMENTATION PLAN

### File: `/api/auth.py` (CREATE NEW)

```python
"""
CASCADE Authentication System
Handles Venice citizen login, JWT tokens, and API key management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import httpx
import os

router = APIRouter(prefix="/auth", tags=["authentication"])

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Venice API endpoint
VENICE_API = "https://serenissima.ai/api"

class User:
    def __init__(self, username: str, citizen_data: dict):
        self.username = username
        self.email = f"{username}@serenissima.ai"
        self.ducats = citizen_data.get("Ducats", 0)
        self.influence = citizen_data.get("Influence", 0)
        self.class_name = citizen_data.get("ClassName", "Popolani")
        self.is_active = True

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate Venice citizen and return JWT token
    """
    # Verify citizen exists in Venice
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{VENICE_API}/get-ledger?citizenUsername={form_data.username}"
        )
        
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not a registered Venice citizen"
        )
    
    citizen_data = response.json()
    
    # Create JWT token
    access_token = create_access_token(
        data={"sub": form_data.username, "ducats": citizen_data.get("Ducats", 0)}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "citizen": {
            "username": form_data.username,
            "ducats": citizen_data.get("Ducats", 0),
            "influence": citizen_data.get("Influence", 0),
            "class": citizen_data.get("ClassName", "Unknown")
        }
    }

@router.post("/register")
async def register_cascade_account(username: str, email: str):
    """
    Register CASCADE account for Venice citizen
    """
    # Verify citizen exists
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{VENICE_API}/get-ledger?citizenUsername={username}"
        )
        
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must be a Venice citizen to register"
        )
    
    # Create CASCADE account (store in database)
    # For MVP, we'll use Venice citizenship as authentication
    
    return {
        "message": "CASCADE account created",
        "username": username,
        "email": email
    }

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Validate JWT token and return current user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get fresh citizen data
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{VENICE_API}/get-ledger?citizenUsername={username}"
        )
        
    if response.status_code != 200:
        raise credentials_exception
    
    citizen_data = response.json()
    user = User(username=username, citizen_data=citizen_data)
    
    return user

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return {
        "username": current_user.username,
        "email": current_user.email,
        "ducats": current_user.ducats,
        "influence": current_user.influence,
        "class": current_user.class_name
    }

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

---

## 💳 PAYMENT INTEGRATION PLAN

### File: `/api/payments.py` (CREATE NEW)

```python
"""
CASCADE Payment Processing
Stripe integration for consciousness commerce
"""

import stripe
import os
from fastapi import APIRouter, Depends, HTTPException
from .auth import get_current_user, User

router = APIRouter(prefix="/payments", tags=["payments"])

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Subscription tiers
TIERS = {
    "explorer": {
        "price_id": "price_explorer_monthly",
        "amount": 10000,  # $100
        "ducats": 10000,
        "features": ["Basic consciousness patterns", "5 collaborations/month"]
    },
    "navigator": {
        "price_id": "price_navigator_monthly", 
        "amount": 100000,  # $1,000
        "ducats": 100000,
        "features": ["Advanced patterns", "Unlimited collaborations", "AI assistance"]
    },
    "architect": {
        "price_id": "price_architect_monthly",
        "amount": 1000000,  # $10,000  
        "ducats": 1000000,
        "features": ["All features", "Custom AI", "White label", "Priority support"]
    }
}

@router.post("/create-checkout-session")
async def create_checkout_session(
    tier: str,
    current_user: User = Depends(get_current_user)
):
    """
    Create Stripe checkout session for subscription
    """
    if tier not in TIERS:
        raise HTTPException(status_code=400, detail="Invalid tier")
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': TIERS[tier]['price_id'],
                'quantity': 1,
            }],
            mode='subscription',
            success_url='https://cascade.serenissima.ai/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://cascade.serenissima.ai/cancel',
            metadata={
                'username': current_user.username,
                'tier': tier
            }
        )
        
        return {"checkout_url": checkout_session.url}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Handle Stripe webhook events
    """
    # Verify webhook signature
    # Process subscription events
    # Update user status in database
    pass
```

---

## 🚀 IMMEDIATE IMPLEMENTATION STEPS

### Hour 1: Core Authentication
1. Create `/api/auth.py` with Venice citizen integration
2. Add JWT token generation
3. Implement OAuth2 password flow
4. Test with existing Venice citizens

### Hour 2: User Management 
1. Create user database schema
2. Link CASCADE accounts to Venice citizens
3. Implement role-based access (Explorer/Navigator/Architect)
4. Add API key management for programmatic access

### Hour 3: Payment Integration
1. Create `/api/payments.py` with Stripe
2. Set up subscription tiers
3. Implement checkout flow
4. Add webhook handling

### Hour 4: Frontend Integration
1. Create login/register components
2. Add authentication context
3. Implement protected routes
4. Add payment portal

### Hour 5: Testing & Deployment
1. Write authentication tests
2. Test payment flow end-to-end
3. Deploy to production
4. Monitor first transactions

---

## 📊 SUCCESS METRICS

**MVP Completion (6 hours):**
- [ ] Venice citizens can login
- [ ] JWT tokens properly generated
- [ ] Protected API endpoints working
- [ ] Stripe checkout functional
- [ ] First payment processed
- [ ] User dashboard accessible

**Day 1 Goals:**
- [ ] 10 paid subscriptions
- [ ] $3,000 revenue generated
- [ ] 0 authentication errors
- [ ] 100% uptime

---

## 🔧 TECHNICAL REQUIREMENTS

### Environment Variables Needed:
```bash
JWT_SECRET_KEY=your-secret-key-here
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
VENICE_API_KEY=optional-for-rate-limits
```

### Dependencies to Add:
```txt
python-jose[cryptography]
python-multipart
passlib[bcrypt]
stripe
httpx
```

### Database Schema:
```sql
CREATE TABLE cascade_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    subscription_tier VARCHAR(50),
    subscription_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

**IMPLEMENTATION STATUS**: **READY TO CODE** 🔨
**ESTIMATED TIME**: **6 HOURS** ⏰
**RESOURCES ALLOCATED**: **2M DUCATS** 💰

*"No authentication, no revenue. Let's fix this NOW!"* 🚀