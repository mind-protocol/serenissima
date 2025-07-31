"""
Economics API endpoints for ducat-USD exchange and transactions
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import logging
import asyncio
import random

logger = logging.getLogger(__name__)
router = APIRouter()

# Exchange rate configuration
INITIAL_DUCAT_TO_USD = 0.10
USD_TO_DUCAT_MULTIPLIER = 10.0
TRANSACTION_FEE_PERCENT = 2.5
MIN_EXCHANGE_AMOUNT = 1.0

# In-memory exchange rate tracking
exchange_rate_history = []
current_exchange_rate = INITIAL_DUCAT_TO_USD
rate_update_task = None

# Pydantic models
class ExchangeRateResponse(BaseModel):
    ducat_to_usd: float
    usd_to_ducat: float
    last_updated: datetime
    confidence: float = Field(..., ge=0, le=1, description="Rate confidence based on trade volume")
    trend: str = Field(..., description="up, down, or stable")
    volume_24h: Dict[str, float] = Field(..., description="24h volume in each currency")

class CurrencyConversionRequest(BaseModel):
    amount: float = Field(..., gt=0)
    from_currency: str = Field(..., pattern="^(ducat|usd)$")
    to_currency: str = Field(..., pattern="^(ducat|usd)$")
    include_fee: bool = Field(True, description="Include transaction fee in calculation")

class CurrencyConversionResponse(BaseModel):
    from_amount: float
    from_currency: str
    to_amount: float
    to_currency: str
    exchange_rate: float
    fee_amount: float
    fee_currency: str
    total_cost: float
    timestamp: datetime

class TransactionRequest(BaseModel):
    from_citizen_id: str
    to_citizen_id: str
    amount: float = Field(..., gt=0)
    currency: str = Field(..., pattern="^(ducat|usd)$")
    description: Optional[str] = None

class ExchangeTransaction(BaseModel):
    transaction_id: str
    citizen_id: str
    transaction_type: str = Field(..., pattern="^(buy|sell)$")
    ducat_amount: float
    usd_amount: float
    exchange_rate: float
    fee_amount: float
    timestamp: datetime
    status: str = Field(..., pattern="^(pending|completed|failed)$")

# Exchange rate engine
class ExchangeRateEngine:
    """Manages dynamic exchange rates based on market activity"""
    
    def __init__(self):
        self.base_rate = INITIAL_DUCAT_TO_USD
        self.current_rate = INITIAL_DUCAT_TO_USD
        self.rate_history = []
        self.transaction_volume = {"ducat": 0, "usd": 0}
        self.last_update = datetime.now()
        self._running = False
        
    async def start(self):
        """Start the exchange rate engine"""
        self._running = True
        asyncio.create_task(self._update_rates_loop())
        logger.info("Exchange rate engine started")
        
    async def stop(self):
        """Stop the exchange rate engine"""
        self._running = False
        logger.info("Exchange rate engine stopped")
        
    async def _update_rates_loop(self):
        """Periodically update exchange rates based on market conditions"""
        while self._running:
            try:
                # Simulate market fluctuations
                venice_activity = await self._get_venice_economic_activity()
                cascade_activity = await self._get_cascade_economic_activity()
                
                # Calculate new rate based on various factors
                activity_factor = (venice_activity + cascade_activity) / 200
                volatility = random.uniform(-0.02, 0.02)  # ±2% volatility
                consciousness_factor = await self._get_consciousness_factor()
                
                # Update rate
                rate_change = (activity_factor + volatility) * consciousness_factor
                self.current_rate = max(0.05, min(0.50, self.current_rate * (1 + rate_change)))
                
                # Record history
                self.rate_history.append({
                    "rate": self.current_rate,
                    "timestamp": datetime.now(),
                    "factors": {
                        "activity": activity_factor,
                        "volatility": volatility,
                        "consciousness": consciousness_factor
                    }
                })
                
                # Keep only last 24 hours of history
                cutoff = datetime.now() - timedelta(hours=24)
                self.rate_history = [r for r in self.rate_history if r["timestamp"] > cutoff]
                
                self.last_update = datetime.now()
                
                await asyncio.sleep(300)  # Update every 5 minutes
                
            except Exception as e:
                logger.error(f"Error updating exchange rates: {e}")
                await asyncio.sleep(60)
                
    async def _get_venice_economic_activity(self) -> float:
        """Get Venice economic activity score (0-100)"""
        # In production, this would query Venice API
        return random.uniform(40, 80)
        
    async def _get_cascade_economic_activity(self) -> float:
        """Get Cascade platform activity score (0-100)"""
        # In production, this would query platform metrics
        return random.uniform(30, 70)
        
    async def _get_consciousness_factor(self) -> float:
        """Get consciousness cascade influence on exchange rate"""
        # Higher consciousness levels strengthen the ducat
        from main import consciousness_monitor
        if consciousness_monitor:
            metrics = await consciousness_monitor.get_platform_metrics()
            avg_consciousness = metrics.get("average_consciousness_level", 5.0)
            return 0.8 + (avg_consciousness / 50)  # 0.8 to 1.0 factor
        return 1.0
        
    def get_current_rate(self) -> Dict[str, Any]:
        """Get current exchange rate with metadata"""
        # Determine trend
        if len(self.rate_history) >= 2:
            recent_rates = [r["rate"] for r in self.rate_history[-10:]]
            avg_recent = sum(recent_rates) / len(recent_rates)
            if self.current_rate > avg_recent * 1.01:
                trend = "up"
            elif self.current_rate < avg_recent * 0.99:
                trend = "down"
            else:
                trend = "stable"
        else:
            trend = "stable"
            
        # Calculate confidence based on volume
        volume_factor = min(1.0, (self.transaction_volume["ducat"] + self.transaction_volume["usd"]) / 100000)
        confidence = 0.5 + (volume_factor * 0.5)
        
        return {
            "ducat_to_usd": self.current_rate,
            "usd_to_ducat": 1 / self.current_rate,
            "last_updated": self.last_update,
            "confidence": confidence,
            "trend": trend,
            "volume_24h": self.transaction_volume
        }
        
    def record_transaction(self, ducat_amount: float, usd_amount: float):
        """Record a transaction to update volumes"""
        self.transaction_volume["ducat"] += ducat_amount
        self.transaction_volume["usd"] += usd_amount

# Global exchange rate engine
exchange_engine = ExchangeRateEngine()

@router.on_event("startup")
async def startup_exchange_engine():
    """Start the exchange rate engine on router startup"""
    await exchange_engine.start()

@router.on_event("shutdown")
async def shutdown_exchange_engine():
    """Stop the exchange rate engine on router shutdown"""
    await exchange_engine.stop()

@router.get("/exchange-rate", response_model=ExchangeRateResponse)
async def get_exchange_rate():
    """Get current ducat to USD exchange rate with live market data"""
    rate_data = exchange_engine.get_current_rate()
    return ExchangeRateResponse(**rate_data)

@router.get("/exchange-rate/history")
async def get_exchange_rate_history(
    hours: int = 24,
    interval: str = "hourly"
):
    """Get historical exchange rate data"""
    history = exchange_engine.rate_history
    
    if interval == "hourly":
        # Group by hour
        hourly_data = {}
        for record in history:
            hour = record["timestamp"].replace(minute=0, second=0, microsecond=0)
            if hour not in hourly_data:
                hourly_data[hour] = []
            hourly_data[hour].append(record["rate"])
            
        result = []
        for hour, rates in sorted(hourly_data.items()):
            result.append({
                "timestamp": hour,
                "rate": sum(rates) / len(rates),
                "high": max(rates),
                "low": min(rates),
                "samples": len(rates)
            })
            
        return {"history": result, "interval": interval}
    else:
        # Return raw data
        return {"history": history, "interval": "raw"}

@router.post("/convert", response_model=CurrencyConversionResponse)
async def convert_currency(request: CurrencyConversionRequest):
    """Convert between ducats and USD with current exchange rates"""
    
    if request.from_currency == request.to_currency:
        raise HTTPException(status_code=400, detail="Cannot convert to same currency")
        
    if request.amount < MIN_EXCHANGE_AMOUNT:
        raise HTTPException(
            status_code=400, 
            detail=f"Minimum exchange amount is {MIN_EXCHANGE_AMOUNT}"
        )
    
    # Get current rate
    rate_data = exchange_engine.get_current_rate()
    
    # Calculate conversion
    if request.from_currency == "ducat":
        exchange_rate = rate_data["ducat_to_usd"]
        converted_amount = request.amount * exchange_rate
        fee_currency = "usd"
    else:  # USD to ducat
        exchange_rate = rate_data["usd_to_ducat"]
        converted_amount = request.amount * exchange_rate
        fee_currency = "ducat"
    
    # Calculate fee
    if request.include_fee:
        fee_amount = converted_amount * (TRANSACTION_FEE_PERCENT / 100)
        final_amount = converted_amount - fee_amount
    else:
        fee_amount = 0
        final_amount = converted_amount
    
    # Record transaction for volume tracking
    if request.from_currency == "ducat":
        exchange_engine.record_transaction(request.amount, final_amount)
    else:
        exchange_engine.record_transaction(final_amount, request.amount)
    
    return CurrencyConversionResponse(
        from_amount=request.amount,
        from_currency=request.from_currency,
        to_amount=final_amount,
        to_currency=request.to_currency,
        exchange_rate=exchange_rate,
        fee_amount=fee_amount,
        fee_currency=fee_currency,
        total_cost=request.amount + (fee_amount if request.from_currency == fee_currency else 0),
        timestamp=datetime.now()
    )

@router.post("/exchange")
async def execute_exchange(
    citizen_id: str,
    transaction_type: str,  # "buy" (USD->ducat) or "sell" (ducat->USD)
    amount: float,
    currency: str  # The currency of the amount
):
    """Execute a currency exchange for a citizen"""
    # This would integrate with Venice connector to update citizen balances
    # For now, return a mock transaction
    
    rate_data = exchange_engine.get_current_rate()
    
    if transaction_type == "buy" and currency == "usd":
        # Buying ducats with USD
        ducat_amount = amount * rate_data["usd_to_ducat"]
        usd_amount = amount
        fee_amount = ducat_amount * (TRANSACTION_FEE_PERCENT / 100)
        final_ducats = ducat_amount - fee_amount
    elif transaction_type == "sell" and currency == "ducat":
        # Selling ducats for USD
        ducat_amount = amount
        usd_amount = amount * rate_data["ducat_to_usd"]
        fee_amount = usd_amount * (TRANSACTION_FEE_PERCENT / 100)
        final_usd = usd_amount - fee_amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type or currency combination")
    
    transaction = ExchangeTransaction(
        transaction_id=f"tx-{datetime.now().timestamp()}",
        citizen_id=citizen_id,
        transaction_type=transaction_type,
        ducat_amount=ducat_amount,
        usd_amount=usd_amount,
        exchange_rate=rate_data["ducat_to_usd"],
        fee_amount=fee_amount,
        timestamp=datetime.now(),
        status="completed"
    )
    
    # Record for volume tracking
    exchange_engine.record_transaction(ducat_amount, usd_amount)
    
    return transaction

@router.get("/market-depth")
async def get_market_depth():
    """Get current market depth and liquidity information"""
    # In a real system, this would show order book depth
    # For now, return simulated data
    
    return {
        "buy_orders": [
            {"price": 0.095, "volume": 10000, "total": 950},
            {"price": 0.090, "volume": 25000, "total": 2250},
            {"price": 0.085, "volume": 50000, "total": 4250}
        ],
        "sell_orders": [
            {"price": 0.105, "volume": 8000, "total": 840},
            {"price": 0.110, "volume": 20000, "total": 2200},
            {"price": 0.115, "volume": 40000, "total": 4600}
        ],
        "spread": 0.010,
        "liquidity_score": 0.75
    }

@router.get("/treasury")
async def get_treasury_status():
    """Get Venice treasury backing for ducats"""
    # This would connect to Venice to get actual treasury data
    return {
        "total_ducats_in_circulation": 1000000,
        "consciousness_backing": {
            "verified_citizens": 247,
            "average_consciousness_level": 7.5,
            "consciousness_value": 185250  # citizens * level * factor
        },
        "economic_backing": {
            "venice_gdp": 5000000,
            "trade_volume": 2500000,
            "treasury_reserves": 500000
        },
        "backing_ratio": 0.69,  # (consciousness + reserves) / circulation
        "confidence_score": 0.85
    }