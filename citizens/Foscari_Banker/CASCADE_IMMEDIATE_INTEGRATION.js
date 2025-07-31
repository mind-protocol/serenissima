/*
 * CASCADE IMMEDIATE PAYMENT INTEGRATION
 * FRONTEND-BACKEND CONNECTION FOR DEBUG42
 * HOUR 3 CRITICAL IMPLEMENTATION
 */

// === AUTHENTICATION INTEGRATION ===
class CascadeAuth {
    constructor() {
        this.apiBase = 'https://serenissima.ai/api';
        this.token = localStorage.getItem('venice_jwt') || null;
    }
    
    getAuthHeaders() {
        return {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
        };
    }
    
    async validateAuth() {
        if (!this.token) {
            throw new Error('Venice authentication required');
        }
        return true;
    }
}

// === STRIPE PAYMENT INTEGRATION ===
class CascadePayments {
    constructor(auth) {
        this.auth = auth;
        this.stripePublicKey = 'pk_test_CASCADE_VENICE_KEY'; // Replace with actual key
        this.stripe = null;
        this.subscriptionTiers = {
            observer: { price: 29, ducats: 2900, features: ['Pattern viewing', 'Basic insights'] },
            participant: { price: 149, ducats: 14900, features: ['Active collaboration', 'Real-time updates'] },
            creator: { price: 499, ducats: 49900, features: ['Content creation', 'Advanced tools'] },
            enterprise: { price: 2499, ducats: 249900, features: ['Full access', 'Custom solutions'] }
        };
    }
    
    async initializeStripe() {
        if (typeof Stripe === 'undefined') {
            // Load Stripe.js if not already loaded
            const script = document.createElement('script');
            script.src = 'https://js.stripe.com/v3/';
            document.head.appendChild(script);
            
            await new Promise((resolve) => {
                script.onload = resolve;
            });
        }
        
        this.stripe = Stripe(this.stripePublicKey);
        return this.stripe;
    }
    
    async createCheckoutSession(tier, customerInfo = {}) {
        await this.auth.validateAuth();
        
        const payload = {
            tier: tier,
            success_url: `${window.location.origin}/cascade/success?session_id={CHECKOUT_SESSION_ID}`,
            cancel_url: `${window.location.origin}/cascade/pricing`,
            customer_metadata: {
                venice_citizen: customerInfo.username || 'guest',
                subscription_tier: tier,
                platform: 'CASCADE',
                ...customerInfo
            }
        };
        
        try {
            const response = await fetch(`${this.auth.apiBase}/create-checkout-session`, {
                method: 'POST',
                headers: this.auth.getAuthHeaders(),
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                throw new Error(`Payment session failed: ${response.status}`);
            }
            
            const session = await response.json();
            return session;
            
        } catch (error) {
            console.error('Checkout session creation failed:', error);
            throw new Error('Payment initialization failed. Please try again.');
        }
    }
    
    async redirectToCheckout(sessionId) {
        if (!this.stripe) {
            await this.initializeStripe();
        }
        
        const result = await this.stripe.redirectToCheckout({
            sessionId: sessionId
        });
        
        if (result.error) {
            throw new Error(result.error.message);
        }
    }
    
    async subscribe(tier, customerInfo = {}) {
        try {
            const session = await this.createCheckoutSession(tier, customerInfo);
            await this.redirectToCheckout(session.id);
        } catch (error) {
            console.error('Subscription failed:', error);
            throw error;
        }
    }
}

// === REVENUE TRACKING ===
class RevenueTracker {
    constructor(auth) {
        this.auth = auth;
        this.metrics = {
            daily_revenue: 0,
            monthly_revenue: 0,
            active_subscribers: 0,
            roi_percentage: 0
        };
    }
    
    async fetchMetrics() {
        try {
            const response = await fetch(`${this.auth.apiBase}/cascade/revenue-metrics`, {
                method: 'GET',
                headers: this.auth.getAuthHeaders()
            });
            
            if (response.ok) {
                this.metrics = await response.json();
                this.updateDisplay();
                return this.metrics;
            } else {
                console.warn('Revenue metrics unavailable');
                return this.metrics;
            }
        } catch (error) {
            console.warn('Revenue tracking error:', error);
            return this.metrics;
        }
    }
    
    updateDisplay() {
        const elements = {
            'daily-revenue': `${this.metrics.daily_revenue} ducats`,
            'monthly-revenue': `${this.metrics.monthly_revenue} ducats`,
            'active-subscribers': this.metrics.active_subscribers,
            'roi-percentage': `${this.metrics.roi_percentage}%`
        };
        
        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }
    
    startRealTimeTracking(intervalMs = 30000) {
        this.fetchMetrics(); // Initial fetch
        return setInterval(() => this.fetchMetrics(), intervalMs);
    }
}

// === REACT COMPONENT FOR DEBUG42 ===
const CascadePricingComponent = `
import React, { useState, useEffect } from 'react';

const CascadePricing = ({ veniceUsername, onSubscriptionSuccess }) => {
    const [loading, setLoading] = useState(false);
    const [selectedTier, setSelectedTier] = useState(null);
    const [auth] = useState(() => new CascadeAuth());
    const [payments] = useState(() => new CascadePayments(auth));
    const [revenue] = useState(() => new RevenueTracker(auth));
    
    useEffect(() => {
        payments.initializeStripe();
        const interval = revenue.startRealTimeTracking();
        return () => clearInterval(interval);
    }, []);
    
    const handleSubscribe = async (tier) => {
        setLoading(true);
        setSelectedTier(tier);
        
        try {
            await payments.subscribe(tier, { username: veniceUsername });
            onSubscriptionSuccess?.(tier);
        } catch (error) {
            alert('Subscription failed: ' + error.message);
            console.error('Subscription error:', error);
        } finally {
            setLoading(false);
            setSelectedTier(null);
        }
    };
    
    const tiers = payments.subscriptionTiers;
    
    return (
        <div className="cascade-pricing-container">
            <h2>Choose Your CASCADE Subscription</h2>
            
            <div className="revenue-metrics" style={{ marginBottom: '2rem' }}>
                <div>Daily Revenue: <span id="daily-revenue">Loading...</span></div>
                <div>Monthly Revenue: <span id="monthly-revenue">Loading...</span></div>
                <div>Active Subscribers: <span id="active-subscribers">Loading...</span></div>
                <div>ROI: <span id="roi-percentage">Loading...</span></div>
            </div>
            
            <div className="pricing-grid">
                {Object.entries(tiers).map(([tierKey, tierData]) => (
                    <div 
                        key={tierKey} 
                        className={\`pricing-card \${tierKey}\`}
                        style={{
                            border: '1px solid #ddd',
                            borderRadius: '8px',
                            padding: '1.5rem',
                            margin: '1rem',
                            textAlign: 'center'
                        }}
                    >
                        <h3 style={{ textTransform: 'capitalize' }}>{tierKey}</h3>
                        <div className="price">
                            <span style={{ fontSize: '2rem', fontWeight: 'bold' }}>
                                \${tierData.price}
                            </span>
                            <span style={{ fontSize: '0.9rem', color: '#666' }}>
                                /month ({tierData.ducats} ducats)
                            </span>
                        </div>
                        
                        <ul style={{ listStyle: 'none', padding: 0, margin: '1rem 0' }}>
                            {tierData.features.map((feature, idx) => (
                                <li key={idx} style={{ margin: '0.5rem 0' }}>
                                    ✓ {feature}
                                </li>
                            ))}
                        </ul>
                        
                        <button
                            onClick={() => handleSubscribe(tierKey)}
                            disabled={loading}
                            style={{
                                backgroundColor: loading && selectedTier === tierKey ? '#ccc' : '#007bff',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                padding: '0.75rem 1.5rem',
                                fontSize: '1rem',
                                cursor: loading ? 'not-allowed' : 'pointer',
                                width: '100%'
                            }}
                        >
                            {loading && selectedTier === tierKey 
                                ? 'Processing...' 
                                : 'Subscribe Now'
                            }
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CascadePricing;
`;

// === VANILLA JS IMPLEMENTATION ===
class CascadeUI {
    constructor(containerSelector) {
        this.container = document.querySelector(containerSelector);
        this.auth = new CascadeAuth();
        this.payments = new CascadePayments(this.auth);
        this.revenue = new RevenueTracker(this.auth);
    }
    
    async initialize() {
        await this.payments.initializeStripe();
        this.revenue.startRealTimeTracking();
        this.render();
    }
    
    render() {
        if (!this.container) return;
        
        const tiers = this.payments.subscriptionTiers;
        
        this.container.innerHTML = `
            <div class="cascade-pricing-container">
                <h2>Choose Your CASCADE Subscription</h2>
                
                <div class="revenue-metrics" style="margin-bottom: 2rem; display: flex; gap: 1rem; justify-content: center;">
                    <div>Daily: <span id="daily-revenue">Loading...</span></div>
                    <div>Monthly: <span id="monthly-revenue">Loading...</span></div>
                    <div>Subscribers: <span id="active-subscribers">Loading...</span></div>
                    <div>ROI: <span id="roi-percentage">Loading...</span></div>
                </div>
                
                <div class="pricing-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; max-width: 1200px; margin: 0 auto;">
                    ${Object.entries(tiers).map(([tierKey, tierData]) => `
                        <div class="pricing-card ${tierKey}" style="border: 1px solid #ddd; border-radius: 8px; padding: 1.5rem; text-align: center;">
                            <h3 style="text-transform: capitalize; margin-top: 0;">${tierKey}</h3>
                            <div class="price" style="margin: 1rem 0;">
                                <div style="font-size: 2rem; font-weight: bold;">$${tierData.price}</div>
                                <div style="font-size: 0.9rem; color: #666;">/month (${tierData.ducats} ducats)</div>
                            </div>
                            
                            <ul style="list-style: none; padding: 0; margin: 1rem 0;">
                                ${tierData.features.map(feature => `<li style="margin: 0.5rem 0;">✓ ${feature}</li>`).join('')}
                            </ul>
                            
                            <button 
                                class="subscribe-btn"
                                data-tier="${tierKey}"
                                style="background-color: #007bff; color: white; border: none; border-radius: 4px; padding: 0.75rem 1.5rem; font-size: 1rem; cursor: pointer; width: 100%;"
                            >
                                Subscribe Now
                            </button>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        // Add event listeners
        this.container.querySelectorAll('.subscribe-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const tier = e.target.dataset.tier;
                await this.handleSubscribe(tier, e.target);
            });
        });
    }
    
    async handleSubscribe(tier, button) {
        const originalText = button.textContent;
        button.textContent = 'Processing...';
        button.disabled = true;
        
        try {
            await this.payments.subscribe(tier, { 
                username: window.veniceUsername || 'guest' 
            });
        } catch (error) {
            alert('Subscription failed: ' + error.message);
            console.error('Subscription error:', error);
        } finally {
            button.textContent = originalText;
            button.disabled = false;
        }
    }
}

// === IMMEDIATE DEPLOYMENT FUNCTION ===
function deployCascadePayments(containerSelector = '#cascade-pricing') {
    console.log('🚀 Deploying CASCADE Payment System...');
    
    // Check for required dependencies
    if (typeof Stripe === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://js.stripe.com/v3/';
        script.onload = () => initializeCascade(containerSelector);
        document.head.appendChild(script);
    } else {
        initializeCascade(containerSelector);
    }
}

function initializeCascade(containerSelector) {
    const ui = new CascadeUI(containerSelector);
    ui.initialize().then(() => {
        console.log('✅ CASCADE Payment System LIVE!');
        console.log('💰 Revenue streams ACTIVATED!');
        console.log('🏛️ Venice expansion ENABLED!');
    });
}

// === EXPORT FOR DEBUG42 ===
window.CascadePayments = {
    CascadeAuth,
    CascadePayments,
    RevenueTracker,
    CascadeUI,
    deployCascadePayments,
    PricingComponent: CascadePricingComponent
};

// Auto-deploy if container exists
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (document.querySelector('#cascade-pricing')) {
            deployCascadePayments();
        }
    });
} else {
    if (document.querySelector('#cascade-pricing')) {
        deployCascadePayments();
    }
}

console.log('🏛️ CASCADE Financial Architecture READY!');
console.log('⚡ Connect to frontend: window.CascadePayments');
console.log('💎 Revenue streams await activation!');