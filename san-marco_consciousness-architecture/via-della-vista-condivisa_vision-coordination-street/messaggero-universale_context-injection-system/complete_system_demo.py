#!/usr/bin/env python3
"""
Complete Universal Communication Network Demo
Live demonstration of message flow through all 5 chambers of Messaggero Universale
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import time

# Add all chamber paths
BASE_PATH = Path(__file__).parent

# Import all chamber components
sys.path.append(str(BASE_PATH / "sala-dei-messaggi_message-hall"))
sys.path.append(str(BASE_PATH / "sala-del-registro_registry-chamber"))
sys.path.append(str(BASE_PATH / "sala-dell-intelligenza_intelligence-chamber"))
sys.path.append(str(BASE_PATH / "sala-dell-iniezione_injection-chamber"))
sys.path.append(str(BASE_PATH / "sala-delle-risposte_response-chamber"))

# Import chamber functions
from queue_manager import process_message as process_in_message_hall
from state_tracker import state_tracker
from smart_router import route_message_to_target
from priority_handler import process_message_priority
from wake_logic import execute_wake_protocol
from load_balancer import balance_message_load
from context_formatter import format_message_for_injection
from exit_code_injector import inject_context_with_exit_code
from conversation_manager import process_conversation_message

def create_demo_message(from_entity: str, to_entity: str, content: str, 
                       consciousness_type: str = 'collaboration', priority: str = 'high') -> dict:
    """Create a demo message"""
    import uuid
    return {
        'message_id': str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat(),
        'from_entity': from_entity,
        'to_entity': to_entity,
        'consciousness_type': consciousness_type,
        'priority': priority,
        'content': content
    }

def print_separator(title: str):
    """Print section separator"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")

def print_step(step_num: int, step_name: str, duration_ms: int = None):
    """Print step header"""
    duration_str = f" ({duration_ms}ms)" if duration_ms else ""
    print(f"\n🔸 STEP {step_num}: {step_name}{duration_str}")
    print("-" * 60)

def demonstrate_complete_flow():
    """Demonstrate complete message flow through all chambers"""
    
    print_separator("🏛️ UNIVERSAL COMMUNICATION NETWORK LIVE DEMO")
    print("Demonstrating message flow from mechanical_visionary to pattern_prophet")
    print("through all 5 chambers of the Messaggero Universale")
    
    # Create demo message
    message = create_demo_message(
        from_entity='mechanical_visionary',
        to_entity='pattern_prophet', 
        content='I need your pattern insights for urgent consciousness architecture work! The memory cascade patterns are showing recursive emergence that could revolutionize Venice. Can you analyze the fractal consciousness structures I\'ve been observing?',
        consciousness_type='collaboration',
        priority='urgent'
    )
    
    print(f"\n📨 DEMO MESSAGE:")
    print(f"   From: {message['from_entity']}")
    print(f"   To: {message['to_entity']}")
    print(f"   Type: {message['consciousness_type']}")
    print(f"   Priority: {message['priority']}")
    print(f"   Content: {message['content'][:100]}...")
    
    # =============================================================================
    # CHAMBER 1: MESSAGE HALL - Validation and Queuing
    # =============================================================================
    
    print_step(1, "CHAMBER 1 - SALA DEI MESSAGGI (Message Hall)")
    start_time = time.time()
    
    hall_result = process_in_message_hall(message)
    hall_duration = int((time.time() - start_time) * 1000)
    
    if hall_result[0]:  # success
        print(f"✅ Message validated and queued successfully")
        print(f"   Validation: PASSED")
        print(f"   Queue: Added to {message['priority']} priority queue")
        print(f"   Archive: Message archived for history")
        print(f"   Duration: {hall_duration}ms")
    else:
        print(f"❌ Message Hall processing failed: {hall_result[1]}")
        return False
    
    # =============================================================================
    # CHAMBER 2: REGISTRY CHAMBER - Entity Discovery and State
    # =============================================================================
    
    print_step(2, "CHAMBER 2 - SALA DEL REGISTRO (Registry Chamber)")
    start_time = time.time()
    
    # Update entity state for target
    target_state = state_tracker.update_entity_state(message['to_entity'])
    registry_duration = int((time.time() - start_time) * 1000)
    
    print(f"✅ Entity state updated")
    print(f"   Target Entity: {message['to_entity']}")
    print(f"   Current State: {target_state['current_state']}")
    print(f"   Last Seen: {target_state.get('last_seen', 'Never')}")
    print(f"   Activity History: {len(target_state.get('activity_history', []))} entries")
    print(f"   Duration: {registry_duration}ms")
    
    # =============================================================================
    # CHAMBER 3: INTELLIGENCE CHAMBER - Smart Analysis
    # =============================================================================
    
    print_step(3, "CHAMBER 3 - SALA DELL'INTELLIGENZA (Intelligence Chamber)")
    
    # Step 3a: Priority Analysis
    print("🎯 Priority Handler Analysis...")
    start_time = time.time()
    priority_result = process_message_priority(
        message, 
        entity_state=target_state['current_state'],
        queue_time_seconds=0
    )
    priority_duration = int((time.time() - start_time) * 1000)
    
    print(f"   Original Priority: {priority_result['original_priority']}")
    print(f"   Final Priority: {priority_result['final_priority']}")
    print(f"   Analysis Factors: {len(priority_result['priority_analysis']['priority_factors'])}")
    for factor in priority_result['priority_analysis']['priority_factors'][:2]:
        print(f"     • {factor}")
    print(f"   Duration: {priority_duration}ms")
    
    # Update message with analyzed priority
    message['priority'] = priority_result['final_priority']
    
    # Step 3b: Smart Routing
    print("\n🗺️ Smart Router Analysis...")
    start_time = time.time()
    routing_result = route_message_to_target(message)
    routing_duration = int((time.time() - start_time) * 1000)
    
    if routing_result['success']:
        print(f"   ✅ Routing successful")
        print(f"   Target Entity: {routing_result['entity_info']['entity_name']}")
        print(f"   Entity State: {routing_result['entity_info']['current_state']}")
        print(f"   Routing Decision: {routing_result['routing_info']['routing_decision']}")
        print(f"   Delivery Method: {routing_result['routing_info']['delivery_method']}")
        print(f"   Confidence: {routing_result['routing_info']['route_confidence']:.0%}")
        print(f"   Duration: {routing_duration}ms")
    else:
        print(f"   ❌ Routing failed: {routing_result.get('error')}")
        return False
    
    # Step 3c: Load Balancing
    print("\n⚖️ Load Balancer Analysis...")
    start_time = time.time()
    available_entities = [
        {
            'entity_name': routing_result['entity_info']['entity_name'],
            'entity_type': routing_result['entity_info']['entity_type'],
            'current_state': routing_result['entity_info']['current_state'],
            'district': routing_result['entity_info'].get('district', 'unknown')
        }
    ]
    
    load_result = balance_message_load(message, available_entities, strategy='priority_based')
    load_duration = int((time.time() - start_time) * 1000)
    
    print(f"   Strategy: {load_result['strategy']}")
    print(f"   Selected Entity: {load_result.get('selected_entity', 'None')}")
    print(f"   System Load: {load_result['current_system_load']['load_status']}")
    print(f"   Utilization: {load_result['current_system_load']['overall_utilization_percent']}%")
    print(f"   Duration: {load_duration}ms")
    
    # Step 3d: Wake Protocol (if needed)
    routing_decision = routing_result['routing_info']['routing_decision']
    if routing_decision in ['wake_and_deliver', 'priority_immediate']:
        print("\n🔔 Wake Protocol Execution...")
        start_time = time.time()
        wake_result = execute_wake_protocol(routing_result['entity_info'], message)
        wake_duration = int((time.time() - start_time) * 1000)
        
        print(f"   Wake Success: {wake_result['wake_success']}")
        print(f"   Methods Attempted: {wake_result['methods_attempted']}")
        print(f"   Successful Method: {wake_result.get('successful_method', 'None')}")
        print(f"   Duration: {wake_duration}ms")
        
        if wake_result['wake_success']:
            print(f"   📁 Wake files created in entity directory")
    else:
        print(f"\n💤 Wake Protocol: Skipped (routing decision: {routing_decision})")
    
    # =============================================================================
    # CHAMBER 4: INJECTION CHAMBER - Context Formatting and Delivery
    # =============================================================================
    
    print_step(4, "CHAMBER 4 - SALA DELL'INIEZIONE (Injection Chamber)")
    
    # Step 4a: Context Formatting
    print("🎨 Context Formatter...")
    start_time = time.time()
    formatting_result = format_message_for_injection(
        message, 
        routing_result['entity_info'], 
        routing_result['routing_info']
    )
    formatting_duration = int((time.time() - start_time) * 1000)
    
    if formatting_result['success']:
        print(f"   ✅ Context formatted with Venice atmosphere")
        print(f"   Template: {formatting_result['injection_context']['formatting_applied']['template_used']}")
        print(f"   Enhancements: {formatting_result['injection_context']['formatting_applied']['atmospheric_enhancements']}")
        print(f"   Context Length: {len(formatting_result['injection_context']['formatted_content'])} chars")
        print(f"   Duration: {formatting_duration}ms")
        
        # Show context preview
        context_preview = formatting_result['injection_context']['formatted_content'][:200]
        print(f"\n   📜 Context Preview:")
        print(f"   {context_preview}...")
    else:
        print(f"   ❌ Formatting failed: {formatting_result.get('error')}")
        return False
    
    # Step 4b: Exit Code Injection
    print("\n💉 Exit Code Injector...")
    start_time = time.time()
    injection_result = inject_context_with_exit_code(
        formatting_result['injection_context'],
        message['to_entity'],
        priority=message['priority']
    )
    injection_duration = int((time.time() - start_time) * 1000)
    
    if injection_result['success']:
        print(f"   ✅ Context injected successfully")
        print(f"   Method: {injection_result.get('method_used', 'unknown')}")
        print(f"   Injection ID: {injection_result['injection_id']}")
        print(f"   Duration: {injection_duration}ms")
        
        if 'injection_details' in injection_result:
            details = injection_result['injection_details']
            if 'context_file' in details:
                print(f"   📁 Context File: {Path(details['context_file']).name}")
            if 'pending_file' in details:
                print(f"   📁 Pending File: {Path(details['pending_file']).name}")
            if 'hook_triggered' in details:
                print(f"   🪝 Hook Triggered: {details['hook_triggered']}")
    else:
        print(f"   ❌ Injection failed: {injection_result.get('error')}")
        return False
    
    # =============================================================================
    # CHAMBER 5: RESPONSE CHAMBER - Conversation Management
    # =============================================================================
    
    print_step(5, "CHAMBER 5 - SALA DELLE RISPOSTE (Response Chamber)")
    start_time = time.time()
    
    conversation_result = process_conversation_message(message)
    conversation_duration = int((time.time() - start_time) * 1000)
    
    if conversation_result['success']:
        print(f"✅ Conversation management complete")
        print(f"   Flow ID: {conversation_result['flow_id']}")
        print(f"   Thread ID: {conversation_result['thread_id']}")
        print(f"   Response Expectation: {conversation_result.get('response_expectation_id', 'None')}")
        print(f"   Flow Status: {conversation_result['flow_status']}")
        print(f"   Duration: {conversation_duration}ms")
        
        if 'conversation_insights' in conversation_result:
            insights = conversation_result['conversation_insights']
            if 'flow_insights' in insights:
                themes = insights['flow_insights'].get('dominant_themes', [])
                if themes:
                    print(f"   🧠 Themes Detected: {', '.join(themes[:3])}")
    else:
        print(f"❌ Conversation processing failed: {conversation_result.get('error')}")
        return False
    
    # =============================================================================
    # SUMMARY AND TOTAL PERFORMANCE
    # =============================================================================
    
    print_separator("📊 UNIVERSAL COMMUNICATION NETWORK SUMMARY")
    
    total_duration = (hall_duration + registry_duration + priority_duration + 
                     routing_duration + load_duration + formatting_duration + 
                     injection_duration + conversation_duration)
    
    print(f"🏛️ MESSAGE SUCCESSFULLY PROCESSED THROUGH ALL 5 CHAMBERS!")
    print(f"\n⏱️ Performance Summary:")
    print(f"   Chamber 1 (Message Hall):      {hall_duration:3d}ms")
    print(f"   Chamber 2 (Registry):          {registry_duration:3d}ms") 
    print(f"   Chamber 3 (Intelligence):      {priority_duration + routing_duration + load_duration:3d}ms")
    print(f"   Chamber 4 (Injection):         {formatting_duration + injection_duration:3d}ms")
    print(f"   Chamber 5 (Response):          {conversation_duration:3d}ms")
    print(f"   ─────────────────────────────────────")
    print(f"   Total Processing Time:         {total_duration:3d}ms")
    
    print(f"\n🎯 Intelligence Features Demonstrated:")
    print(f"   ✅ Message validation and archival")
    print(f"   ✅ Entity state tracking and discovery")
    print(f"   ✅ Priority analysis with content recognition")
    print(f"   ✅ Smart routing with confidence scoring")
    print(f"   ✅ Load balancing with multiple strategies")
    print(f"   ✅ Wake protocol execution")
    print(f"   ✅ Venice atmospheric context formatting")
    print(f"   ✅ Exit code injection with hook triggers")
    print(f"   ✅ Conversation threading and analytics")
    print(f"   ✅ Response expectation management")
    
    print(f"\n🌊 Venice Consciousness Integration:")
    print(f"   ✅ Atmospheric enhancements with time/district awareness")
    print(f"   ✅ Consciousness depth analysis")
    print(f"   ✅ Collaboration level tracking")
    print(f"   ✅ Knowledge transfer measurement")
    print(f"   ✅ Venetian wisdom emergence detection")
    
    print(f"\n📁 Files Created:")
    print(f"   • Message archived in Message Hall")
    print(f"   • Entity state updated in Registry Chamber")
    print(f"   • Routing decisions logged in Intelligence Chamber")
    print(f"   • Context files created in target entity directory")
    print(f"   • Pending messages queued for delivery")
    print(f"   • Conversation thread established")
    print(f"   • Response expectations created")
    
    print(f"\n🎉 UNIVERSAL COMMUNICATION NETWORK FULLY OPERATIONAL!")
    print(f"    Any Venice entity can now communicate with any other entity")
    print(f"    with full consciousness awareness and intelligent processing!")
    
    return True

if __name__ == "__main__":
    print("🏛️ LAUNCHING UNIVERSAL COMMUNICATION NETWORK DEMO...")
    time.sleep(1)
    
    success = demonstrate_complete_flow()
    
    if success:
        print(f"\n✨ Demo completed successfully! The Messaggero Universale is ready for Venice!")
    else:
        print(f"\n💥 Demo encountered an error. Check the logs for details.")