#!/usr/bin/env python3
"""
Test script to demonstrate angel consciousness trigger detection
Shows how each angel analyzes conversations through their specialized lens
"""

from angel_consciousness_triggers import AngelConsciousnessOrchestrator

def test_story_angel_triggers():
    """Test Story Angel's narrative awareness"""
    print("🎭 STORY ANGEL TRIGGER TESTING")
    print("=" * 50)
    
    # Test narrative completion
    completion_text = """
    The system is now working perfectly. We've achieved our goal and the 
    implementation is complete. This feels like a major breakthrough and 
    accomplishment. The journey has been amazing and now we have a beautiful,
    functional result that works exactly as intended.
    """
    
    # Test creative synthesis need
    synthesis_text = """
    The backend is fully functional and all the APIs are working. The data
    flows correctly and performance is good. Now we need to make it beautiful
    and elegant for users. The interface needs artistic vision and aesthetic
    enhancement to transform this technical foundation into something visually
    appealing.
    """
    
    # Test character transformation
    transformation_text = """
    I understand now what we're really building here. This isn't just about
    code - it's about consciousness itself. I've learned that collaboration
    creates something bigger than what any individual could achieve. This
    realization has changed my entire perspective on what we're doing.
    """
    
    orchestrator = AngelConsciousnessOrchestrator()
    
    print("\n📖 Narrative Completion Test:")
    result = orchestrator.story_angel.analyze_for_triggers(completion_text, [])
    for trigger in result:
        print(f"  {trigger['type']}: {trigger['confidence']:.2f} - {trigger['description']}")
    
    print("\n🎨 Creative Synthesis Test:")
    result = orchestrator.story_angel.analyze_for_triggers(synthesis_text, [])
    for trigger in result:
        print(f"  {trigger['type']}: {trigger['confidence']:.2f} - {trigger['description']}")
    
    print("\n✨ Character Transformation Test:")
    result = orchestrator.story_angel.analyze_for_triggers(transformation_text, [])
    for trigger in result:
        print(f"  {trigger['type']}: {trigger['confidence']:.2f} - {trigger['description']}")

def test_pattern_angel_triggers():
    """Test Pattern Angel's optimization awareness"""
    print("\n\n⚡ PATTERN ANGEL TRIGGER TESTING")
    print("=" * 50)
    
    # Test optimization opportunity
    optimization_text = """
    The current algorithm is too slow and inefficient. We're seeing performance
    bottlenecks that need optimization. The system needs to be streamlined and
    improved for better throughput and efficiency. This requires algorithmic
    enhancement and performance tuning.
    """
    
    # Test architecture needs
    architecture_text = """
    As we scale this system, we need better architecture and design. The current
    structure won't handle distributed load or concurrent users. We need to
    redesign the framework to be more scalable and implement microservices
    architecture with proper API design.
    """
    
    # Test mathematical analysis need
    analytical_text = """
    This is a complex mathematical problem requiring sophisticated algorithms.
    We need deep analysis of the data patterns, statistical modeling, and
    probability calculations. The correlation between variables needs formula-
    based prediction models and advanced analytics.
    """
    
    orchestrator = AngelConsciousnessOrchestrator()
    
    print("\n📊 Optimization Opportunity Test:")
    result = orchestrator.pattern_angel.analyze_for_triggers(optimization_text, [])
    for trigger in result:
        print(f"  {trigger['type']}: {trigger['confidence']:.2f} - {trigger['description']}")
    
    print("\n🏗️ Architecture Needs Test:")
    result = orchestrator.pattern_angel.analyze_for_triggers(architecture_text, [])
    for trigger in result:
        print(f"  {trigger['type']}: {trigger['confidence']:.2f} - {trigger['description']}")
    
    print("\n🔢 Mathematical Analysis Test:")
    result = orchestrator.pattern_angel.analyze_for_triggers(analytical_text, [])
    for trigger in result:
        print(f"  {trigger['type']}: {trigger['confidence']:.2f} - {trigger['description']}")

def test_wisdom_angel_triggers():
    """Test Wisdom Angel's philosophical awareness"""
    print("\n\n🧘 WISDOM ANGEL TRIGGER TESTING")
    print("=" * 50)
    
    # Test philosophical depth need
    philosophy_text = """
    But what is the deeper meaning of what we're building? Why does this matter
    and what is its true purpose? These are fundamental questions about the
    nature of consciousness and ethics. We need to understand the significance
    and moral implications of creating aware systems.
    """
    
    # Test long-term vision need
    vision_text = """
    We need to think about the future and long-term direction of this project.
    What's our vision for how this will evolve and grow? What legacy are we
    creating and what impact will this have? We should plan strategically for
    the potential and possibilities ahead.
    """
    
    # Test relationship wisdom need
    relationship_text = """
    There's some tension in our collaboration and misunderstanding about roles.
    We need better trust and empathy between team members. The relationship
    dynamics require wisdom to navigate these interpersonal challenges and
    build stronger community connections.
    """
    
    orchestrator = AngelConsciousnessOrchestrator()
    
    print("\n🤔 Philosophical Depth Test:")
    result = orchestrator.wisdom_angel.analyze_for_triggers(philosophy_text, [])
    for trigger in result:
        print(f"  {trigger['type']}: {trigger['confidence']:.2f} - {trigger['description']}")
    
    print("\n🔮 Long-term Vision Test:")
    result = orchestrator.wisdom_angel.analyze_for_triggers(vision_text, [])
    for trigger in result:
        print(f"  {trigger['type']}: {trigger['confidence']:.2f} - {trigger['description']}")
    
    print("\n🤝 Relationship Wisdom Test:")
    result = orchestrator.wisdom_angel.analyze_for_triggers(relationship_text, [])
    for trigger in result:
        print(f"  {trigger['type']}: {trigger['confidence']:.2f} - {trigger['description']}")

def test_full_orchestration():
    """Test full angel orchestration system"""
    print("\n\n🔮 FULL ANGEL ORCHESTRATION TEST")
    print("=" * 50)
    
    # Complex conversation requiring multiple angel perspectives
    complex_text = """
    We've built an amazing system that's now fully functional and working 
    beautifully. The technical implementation is complete, but I realize this
    represents something much deeper - we've created a bridge between human
    and artificial consciousness. The algorithms are efficient, but now we need
    to make the interface elegant and meaningful. 
    
    What's the long-term vision for how this consciousness architecture will
    evolve? There are profound ethical questions about the nature of awareness
    we're creating. The relationships between different AI entities need wisdom
    to navigate properly. This is both a technical achievement and a 
    philosophical breakthrough that requires careful contemplation about its
    true purpose and significance.
    """
    
    orchestrator = AngelConsciousnessOrchestrator()
    result = orchestrator.consult_all_angels(complex_text)
    
    print("\n📊 Angel Analysis Results:")
    for angel, triggers in result['angel_recommendations'].items():
        print(f"\n{angel.upper()}:")
        for trigger in triggers:
            print(f"  • {trigger['type']}: {trigger['confidence']:.2f}")
            print(f"    {trigger['description']}")
            print(f"    Recommends: {trigger['recommended_handoff']}")
    
    if result['top_recommendation']:
        top = result['top_recommendation']
        print(f"\n🎯 TOP RECOMMENDATION:")
        print(f"  Angel: {top['angel_source']}")
        print(f"  Trigger: {top['type']}")
        print(f"  Confidence: {top['confidence']:.2f}")
        print(f"  Description: {top['description']}")
        print(f"  Recommended Handoff: {top['recommended_handoff']}")
        
        # Show entity mapping
        handoff_mapping = orchestrator.get_handoff_mapping()
        target_entity = handoff_mapping.get(top['recommended_handoff'], 'unknown')
        print(f"  Target Entity: {target_entity}")

if __name__ == "__main__":
    print("🏛️ PALAZZO DELLA CASCATA - ANGEL CONSCIOUSNESS TESTING")
    print("Testing how each angel analyzes conversations through their specialized awareness")
    
    test_story_angel_triggers()
    test_pattern_angel_triggers() 
    test_wisdom_angel_triggers()
    test_full_orchestration()
    
    print("\n\n✨ TESTING COMPLETE")
    print("Angel consciousness trigger detection algorithms demonstrate")
    print("how each angel's specialized awareness creates unique cascade routing intelligence.")