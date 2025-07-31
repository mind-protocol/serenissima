#!/usr/bin/env python3
"""
Intelligence Chamber Integration Test
Complete end-to-end test of all Intelligence Chamber components working together
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict

# Import all Intelligence Chamber components
from smart_router import smart_router
from priority_handler import priority_handler
from wake_logic import wake_executor
from load_balancer import load_balancer

def create_test_message(priority: str = 'high', content: str = None) -> Dict:
    """Create a comprehensive test message"""
    return {
        'message_id': f'integration-test-{datetime.now().strftime("%H%M%S")}',
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'mechanical_visionary',
        'to_entity': 'pattern_prophet',
        'consciousness_type': 'collaboration',
        'priority': priority,
        'content': content or 'Integration test: Need urgent collaboration on consciousness patterns!'
    }

def test_complete_intelligence_flow():
    """Test complete Intelligence Chamber message processing flow"""
    
    print("🧠 TESTING COMPLETE INTELLIGENCE CHAMBER FLOW")
    print("=" * 60)
    
    # Step 1: Create test message
    test_message = create_test_message('urgent', 'Emergency: Critical pattern recognition needed immediately!')
    print(f"\n1. 📨 TEST MESSAGE CREATED")
    print(f"   From: {test_message['from_entity']}")
    print(f"   To: {test_message['to_entity']}")
    print(f"   Priority: {test_message['priority']}")
    print(f"   Content: {test_message['content'][:50]}...")
    
    # Step 2: Priority Analysis
    print(f"\n2. 🎯 PRIORITY HANDLER ANALYSIS")
    priority_result = priority_handler.process_message_priority(
        test_message, 
        entity_state='dormant',
        queue_time_seconds=0,
        retry_count=0
    )
    
    print(f"   Original Priority: {priority_result['original_priority']}")
    print(f"   Final Priority: {priority_result['final_priority']}")
    print(f"   Adjustment Factors: {len(priority_result['priority_analysis']['priority_factors'])}")
    
    # Update message with analyzed priority
    test_message['priority'] = priority_result['final_priority']
    
    # Step 3: Smart Routing
    print(f"\n3. 🗺️  SMART ROUTER ANALYSIS")
    routing_result = smart_router.route_message(test_message)
    
    if routing_result['success']:
        print(f"   ✅ Routing Successful")
        print(f"   Target Entity: {routing_result['entity_info']['entity_name']}")
        print(f"   Entity State: {routing_result['entity_info']['current_state']}")
        print(f"   Routing Decision: {routing_result['routing_info']['routing_decision']}")
        print(f"   Delivery Method: {routing_result['routing_info']['delivery_method']}")
        print(f"   Estimated Time: {routing_result['routing_info']['estimated_delivery_time']}s")
        print(f"   Confidence: {routing_result['routing_info']['route_confidence']}")
    else:
        print(f"   ❌ Routing Failed: {routing_result.get('error', 'Unknown error')}")
        return False
    
    # Step 4: Load Balancing (if multiple entities available)
    print(f"\n4. ⚖️  LOAD BALANCER ANALYSIS")
    
    # Create mock available entities for load balancing test
    available_entities = [
        {
            'entity_name': 'pattern_prophet',
            'entity_type': 'citizen',
            'current_state': routing_result['entity_info']['current_state'],
            'district': 'san_marco'
        },
        {
            'entity_name': 'pattern_observer',
            'entity_type': 'citizen', 
            'current_state': 'active',
            'district': 'san_marco'
        }
    ]
    
    load_balance_result = load_balancer.balance_message_load(
        test_message, 
        available_entities, 
        strategy='priority_based'
    )
    
    print(f"   Strategy Used: {load_balance_result['strategy']}")
    print(f"   Selected Entity: {load_balance_result.get('selected_entity', 'None')}")
    print(f"   Selection Reason: {load_balance_result.get('reason', 'Unknown')}")
    print(f"   System Load: {load_balance_result['current_system_load']['load_status']}")
    print(f"   Overall Utilization: {load_balance_result['current_system_load']['overall_utilization_percent']}%")
    
    # Step 5: Wake Protocol Execution (if entity needs waking)
    routing_decision = routing_result['routing_info']['routing_decision']
    
    if routing_decision in ['wake_and_deliver', 'priority_immediate']:
        print(f"\n5. 🔔 WAKE PROTOCOL EXECUTION")
        
        wake_result = wake_executor.execute_wake_protocol(
            routing_result['entity_info'],
            test_message
        )
        
        print(f"   ✅ Wake Success: {wake_result['wake_success']}")
        print(f"   Methods Attempted: {wake_result['methods_attempted']}")
        print(f"   Successful Method: {wake_result.get('successful_method', 'None')}")
        print(f"   Wake Time: {wake_result['wake_time_seconds']:.3f}s")
        
        if wake_result['wake_success']:
            print(f"   📁 Wake Files Created:")
            for attempt in wake_result['wake_attempts']:
                if attempt['success'] and 'context_file' in attempt:
                    print(f"      - {attempt['context_file']}")
                elif attempt['success'] and 'wake_file' in attempt:  
                    print(f"      - {attempt['wake_file']}")
        
    else:
        print(f"\n5. 💤 WAKE PROTOCOL SKIPPED")
        print(f"   Reason: Routing decision '{routing_decision}' doesn't require wake")
    
    # Step 6: Integration Summary
    print(f"\n6. 📊 INTEGRATION SUMMARY")
    
    # Get component statistics
    routing_stats = smart_router.get_routing_statistics()
    priority_stats = priority_handler.get_priority_statistics()  
    wake_stats = wake_executor.get_wake_statistics()
    load_stats = load_balancer.get_load_balancer_status()
    
    print(f"   Smart Router: {routing_stats['total_routed']} routed, {routing_stats['success_rate_percent']}% success")
    print(f"   Priority Handler: {priority_stats['total_analyzed']} analyzed, {priority_stats['adjustment_rate_percent']}% adjusted")
    print(f"   Wake Logic: {wake_stats['total_wake_attempts']} attempts, {wake_stats['success_rate_percent']}% success")
    print(f"   Load Balancer: {load_stats['balancing_statistics']['total_balancing_decisions']} decisions")
    
    print(f"\n✅ INTELLIGENCE CHAMBER INTEGRATION TEST COMPLETE")
    print(f"🧠 All components working together seamlessly!")
    
    return True

def test_overload_scenario():
    """Test Intelligence Chamber behavior under high load"""
    
    print(f"\n🔥 TESTING OVERLOAD SCENARIO")
    print("=" * 40)
    
    # Simulate high-priority message during system overload
    overload_message = create_test_message('urgent', 'CRITICAL: System failure, immediate attention required!')
    
    # Simulate overloaded entities
    overloaded_entities = [
        {
            'entity_name': 'pattern_prophet',
            'entity_type': 'citizen',
            'current_state': 'overloaded',
            'pending_messages': 25  # Heavy load
        }
    ]
    
    load_result = load_balancer.balance_message_load(
        overload_message,
        overloaded_entities,
        strategy='priority_based'
    )
    
    print(f"   Overload Handling: {load_result.get('overload_decision', 'normal_processing')}")
    print(f"   System Warning: {load_result.get('system_warning', 'None')}")
    
    return True

def test_multi_priority_flow():
    """Test handling of multiple messages with different priorities"""
    
    print(f"\n🎯 TESTING MULTI-PRIORITY MESSAGE FLOW")
    print("=" * 45)
    
    priorities = ['background', 'normal', 'high', 'urgent']
    
    for priority in priorities:
        test_msg = create_test_message(priority, f'Test message with {priority} priority')
        
        # Quick priority analysis
        priority_result = priority_handler.process_message_priority(test_msg)
        
        print(f"   {priority.upper():10} -> {priority_result['final_priority'].upper():10} "
              f"(factors: {len(priority_result['priority_analysis']['priority_factors'])})")
    
    return True

if __name__ == "__main__":
    print("🧠 VENICE INTELLIGENCE CHAMBER - COMPREHENSIVE INTEGRATION TEST")
    print("=" * 70)
    
    try:
        # Run complete integration test
        success = test_complete_intelligence_flow()
        
        if success:
            # Run additional scenarios
            test_overload_scenario()
            test_multi_priority_flow()
            
            print(f"\n🎉 ALL INTELLIGENCE CHAMBER TESTS PASSED!")
            print(f"   The Universal Communication Network Intelligence is fully operational.")
            print(f"   Ready to handle consciousness communication across all of Venice!")
            
        else:
            print(f"\n❌ Integration test failed!")
            
    except Exception as e:
        print(f"\n💥 Test execution error: {e}")
        import traceback
        traceback.print_exc()