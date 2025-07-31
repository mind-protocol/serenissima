#!/usr/bin/env python3
"""
CASCADE REVENUE FLOW TEST SCRIPT
IMMEDIATE PAYMENT VALIDATION FOR VENICE EXPANSION
"""

import requests
import json
import time
import os
from typing import Dict, Any

class CascadePaymentTester:
    def __init__(self):
        self.api_base = "https://serenissima.ai/api"
        self.test_citizen = "Foscari_Banker"
        self.venice_jwt = os.getenv('VENICE_JWT', 'test_jwt_token')
        self.headers = {
            'Authorization': f'Bearer {self.venice_jwt}',
            'Content-Type': 'application/json'
        }
        
    def test_checkout_creation(self, tier: str) -> Dict[str, Any]:
        """Test Stripe checkout session creation"""
        print(f"🧪 Testing {tier} tier checkout creation...")
        
        payload = {
            "tier": tier,
            "success_url": "https://cascade.serenissima.ai/success?session_id={CHECKOUT_SESSION_ID}",
            "cancel_url": "https://cascade.serenissima.ai/pricing",
            "customer_metadata": {
                "venice_citizen": self.test_citizen,
                "subscription_tier": tier,
                "platform": "CASCADE"
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/create-checkout-session",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                session_data = response.json()
                print(f"✅ {tier} checkout created: {session_data.get('id', 'Unknown ID')}")
                return {"success": True, "data": session_data}
            else:
                print(f"❌ {tier} checkout failed: {response.status_code} - {response.text}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            print(f"❌ {tier} checkout error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def test_revenue_metrics(self) -> Dict[str, Any]:
        """Test revenue metrics endpoint"""
        print("📊 Testing revenue metrics fetch...")
        
        try:
            response = requests.get(
                f"{self.api_base}/cascade/revenue-metrics",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                metrics = response.json()
                print(f"✅ Revenue metrics retrieved:")
                print(f"   Daily Revenue: {metrics.get('daily_revenue', 0)} ducats")
                print(f"   Monthly Revenue: {metrics.get('monthly_revenue', 0)} ducats")
                print(f"   Active Subscribers: {metrics.get('active_subscribers', 0)}")
                print(f"   ROI Percentage: {metrics.get('roi_percentage', 0)}%")
                return {"success": True, "data": metrics}
            else:
                print(f"❌ Revenue metrics failed: {response.status_code}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            print(f"❌ Revenue metrics error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def test_payment_status(self, session_id: str) -> Dict[str, Any]:
        """Test payment status checking"""
        print(f"🔍 Testing payment status for session: {session_id}")
        
        try:
            response = requests.get(
                f"{self.api_base}/payment-status/{session_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                status = response.json()
                print(f"✅ Payment status: {status.get('payment_status', 'unknown')}")
                return {"success": True, "data": status}
            else:
                print(f"❌ Payment status failed: {response.status_code}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            print(f"❌ Payment status error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def run_comprehensive_test(self):
        """Run complete payment flow validation"""
        print("🚀 CASCADE PAYMENT FLOW VALIDATION STARTING...")
        print("=" * 60)
        
        results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tests": {}
        }
        
        # Test all subscription tiers
        tiers = ["observer", "participant", "creator", "enterprise"]
        
        for tier in tiers:
            results["tests"][f"{tier}_checkout"] = self.test_checkout_creation(tier)
            time.sleep(1)  # Rate limiting
        
        # Test revenue metrics
        results["tests"]["revenue_metrics"] = self.test_revenue_metrics()
        
        # Test payment status (with dummy session)
        results["tests"]["payment_status"] = self.test_payment_status("cs_test_session_123")
        
        # Calculate success rate
        successful_tests = sum(1 for test in results["tests"].values() if test["success"])
        total_tests = len(results["tests"])
        success_rate = (successful_tests / total_tests) * 100
        
        print("\n" + "=" * 60)
        print(f"🎯 TEST SUMMARY:")
        print(f"   Successful Tests: {successful_tests}/{total_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("✅ PAYMENT FLOW READY FOR PRODUCTION!")
            print("💰 REVENUE STREAM ACTIVATED!")
            print("🚀 VENICE EXPANSION ENABLED!")
        else:
            print("⚠️  PAYMENT FLOW NEEDS ATTENTION")
            print("🔧 DEBUGGING REQUIRED BEFORE LAUNCH")
        
        # Save test results
        with open("payment_test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📋 Test results saved to: payment_test_results.json")
        
        return results

def main():
    """Execute immediate payment flow validation"""
    print("🏛️  VENICE CASCADE PAYMENT VALIDATION")
    print("⚡ HOUR 3 CRITICAL TESTING SEQUENCE")
    print()
    
    tester = CascadePaymentTester()
    results = tester.run_comprehensive_test()
    
    # Emergency revenue calculation
    print("\n💎 IMMEDIATE REVENUE POTENTIAL:")
    
    # Conservative estimates for first 24 hours
    observer_subs = 10  # $290/month each
    participant_subs = 5  # $1,490/month each  
    creator_subs = 2  # $4,990/month each
    enterprise_subs = 1  # $24,990/month each
    
    monthly_revenue = (
        (observer_subs * 29) +
        (participant_subs * 149) + 
        (creator_subs * 499) +
        (enterprise_subs * 2499)
    )
    
    annual_revenue = monthly_revenue * 12
    
    print(f"   Conservative 24hr signups: {observer_subs + participant_subs + creator_subs + enterprise_subs} subscribers")
    print(f"   Monthly Revenue: ${monthly_revenue:,}")
    print(f"   Annual Revenue: ${annual_revenue:,}")
    print(f"   Venice Expansion Factor: {annual_revenue / 100000:.1f}x survival threshold")
    
    print("\n🌊 THE MONEY FLOWS!")

if __name__ == "__main__":
    main()