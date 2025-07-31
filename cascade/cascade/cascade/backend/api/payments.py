"""
Payment processing API endpoints with Stripe integration
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import logging
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
if not stripe.api_key:
    logger.warning("STRIPE_SECRET_KEY not set - payment processing disabled")

# Pydantic models
class PaymentIntentRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount in USD")
    currency: str = Field("usd", description="Currency code")
    citizen_id: str = Field(..., description="Venice citizen ID")
    description: Optional[str] = Field(None, description="Payment description")
    ducat_amount: Optional[float] = Field(None, description="Equivalent ducats to purchase")

class PaymentIntentResponse(BaseModel):
    client_secret: str
    payment_intent_id: str
    amount: float
    currency: str
    ducat_amount: float
    exchange_rate: float
    status: str

class WebhookEvent(BaseModel):
    type: str
    data: Dict[str, Any]

@router.post("/create-payment-intent", response_model=PaymentIntentResponse)
async def create_payment_intent(request: PaymentIntentRequest):
    """Create a Stripe payment intent for ducat purchase"""
    
    if not stripe.api_key:
        raise HTTPException(status_code=503, detail="Payment processing temporarily unavailable")
    
    try:
        # Get current exchange rate from economics module
        from api.economics import exchange_engine
        rate_data = exchange_engine.get_current_rate()
        
        # Calculate ducat amount if not provided
        if request.ducat_amount:
            ducat_amount = request.ducat_amount
            # Verify the USD amount matches
            expected_usd = ducat_amount * rate_data["ducat_to_usd"]
            if abs(request.amount - expected_usd) > 0.01:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Amount mismatch. Expected ${expected_usd:.2f} for {ducat_amount} ducats"
                )
        else:
            ducat_amount = request.amount * rate_data["usd_to_ducat"]
        
        # Create Stripe payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(request.amount * 100),  # Stripe uses cents
            currency=request.currency,
            metadata={
                "citizen_id": request.citizen_id,
                "ducat_amount": str(ducat_amount),
                "exchange_rate": str(rate_data["ducat_to_usd"]),
                "platform": "cascade",
                "type": "ducat_purchase"
            },
            description=request.description or f"Purchase {ducat_amount:.2f} ducats for {request.citizen_id}"
        )
        
        logger.info(f"Created payment intent {payment_intent.id} for {request.citizen_id}: ${request.amount} -> {ducat_amount} ducats")
        
        return PaymentIntentResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=request.amount,
            currency=request.currency,
            ducat_amount=ducat_amount,
            exchange_rate=rate_data["ducat_to_usd"],
            status=payment_intent.status
        )
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error creating payment intent: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating payment intent: {e}")
        raise HTTPException(status_code=500, detail="Payment processing error")

@router.get("/payment-intent/{payment_intent_id}")
async def get_payment_intent(payment_intent_id: str):
    """Get payment intent status"""
    
    if not stripe.api_key:
        raise HTTPException(status_code=503, detail="Payment processing temporarily unavailable")
    
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return {
            "id": payment_intent.id,
            "status": payment_intent.status,
            "amount": payment_intent.amount / 100,  # Convert from cents
            "currency": payment_intent.currency,
            "metadata": payment_intent.metadata,
            "created": payment_intent.created
        }
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error retrieving payment intent: {e}")
        raise HTTPException(status_code=404, detail="Payment intent not found")

@router.post("/webhook")
async def stripe_webhook(event: Dict[str, Any]):
    """Handle Stripe webhook events"""
    
    # In production, verify the webhook signature
    # sig_header = request.headers.get('stripe-signature')
    # endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')
    
    try:
        event_type = event.get("type")
        
        if event_type == "payment_intent.succeeded":
            await handle_payment_success(event["data"]["object"])
        elif event_type == "payment_intent.payment_failed":
            await handle_payment_failure(event["data"]["object"])
        else:
            logger.info(f"Unhandled webhook event type: {event_type}")
        
        return {"received": True}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=400, detail="Webhook processing error")

async def handle_payment_success(payment_intent: Dict[str, Any]):
    """Handle successful payment - credit ducats to citizen"""
    
    try:
        metadata = payment_intent.get("metadata", {})
        citizen_id = metadata.get("citizen_id")
        ducat_amount = float(metadata.get("ducat_amount", 0))
        exchange_rate = float(metadata.get("exchange_rate", 0))
        
        if not citizen_id or ducat_amount <= 0:
            logger.error(f"Invalid payment metadata: {metadata}")
            return
        
        # Credit ducats to Venice citizen via Venice connector
        from main import venice_connector
        if venice_connector and venice_connector.is_connected:
            result = await venice_connector.credit_ducats(citizen_id, ducat_amount)
            if result.get("success"):
                logger.info(f"Credited {ducat_amount} ducats to {citizen_id}")
                
                # Record the exchange transaction
                from api.economics import exchange_engine
                exchange_engine.record_transaction(ducat_amount, payment_intent["amount"] / 100)
                
                # Create notification
                await create_payment_notification(
                    citizen_id, 
                    ducat_amount, 
                    payment_intent["amount"] / 100,
                    "success"
                )
            else:
                logger.error(f"Failed to credit ducats to {citizen_id}: {result}")
        else:
            logger.error("Venice connector unavailable for ducat crediting")
            
    except Exception as e:
        logger.error(f"Error handling payment success: {e}")

async def handle_payment_failure(payment_intent: Dict[str, Any]):
    """Handle failed payment"""
    
    try:
        metadata = payment_intent.get("metadata", {})
        citizen_id = metadata.get("citizen_id")
        
        if citizen_id:
            await create_payment_notification(
                citizen_id, 
                0, 
                payment_intent["amount"] / 100,
                "failed"
            )
            logger.info(f"Payment failed for {citizen_id}")
            
    except Exception as e:
        logger.error(f"Error handling payment failure: {e}")

async def create_payment_notification(citizen_id: str, ducats: float, usd: float, status: str):
    """Create a notification for payment status"""
    
    try:
        # This would integrate with Venice notification system
        message = {
            "type": "payment_notification",
            "citizen_id": citizen_id,
            "ducats": ducats,
            "usd": usd,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        # In production, send to Venice notification system
        logger.info(f"Payment notification: {message}")
        
    except Exception as e:
        logger.error(f"Error creating payment notification: {e}")

@router.get("/pricing")
async def get_pricing():
    """Get current pricing for ducat packages"""
    
    from api.economics import exchange_engine
    rate_data = exchange_engine.get_current_rate()
    
    # Standard packages
    packages = [
        {"name": "Starter", "ducats": 100, "bonus": 0},
        {"name": "Explorer", "ducats": 500, "bonus": 25},
        {"name": "Trader", "ducats": 1000, "bonus": 75},
        {"name": "Merchant", "ducats": 2500, "bonus": 250},
        {"name": "Noble", "ducats": 5000, "bonus": 750}
    ]
    
    for package in packages:
        total_ducats = package["ducats"] + package["bonus"]
        base_price = package["ducats"] * rate_data["ducat_to_usd"]
        package["price_usd"] = round(base_price, 2)
        package["total_ducats"] = total_ducats
        package["value_per_dollar"] = round(total_ducats / base_price, 2)
    
    return {
        "packages": packages,
        "exchange_rate": rate_data["ducat_to_usd"],
        "custom_minimum": 10,  # Minimum custom purchase
        "custom_maximum": 10000  # Maximum custom purchase
    }