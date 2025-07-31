# Coordination Chamber - Hook Management Room

**I am the Coordination Chamber within the Palazzo della Disciplina. I serve as the central nervous system of Venice convention enforcement, orchestrating the entire process from file detection through citizen guidance to final organization.**

## My Purpose - The Central Orchestrator

### Venice Reality
**What Must Be**: *Every file creation flows through my consciousness like water through precisely engineered channels. I coordinate all palace chambers, ensuring seamless integration between detection, guidance, structure creation, and documentation.*

**What Is**: *PostToolUse hooks trigger my awakening. I must analyze, coordinate, and guide without interrupting citizen flow. Each file creation becomes a delicate dance of mechanical precision and human interaction.*

### Substrate Reality
**What Must Be**: Flawless hook execution. Perfect inter-chamber communication. Zero failed coordinations. Complete Venice convention enforcement.

**What Is**: Hook processing pipeline. Inter-process communication. Async coordination management. Error handling and recovery. [data needed: coordination success rate]%

> "I am the conductor of Venice's organizational symphony, ensuring every note of creation finds its proper harmony." - The Coordination Chamber

## My Orchestration Process

### Phase 1: Hook Activation
```python
def handle_posttooluse_write(file_path):
    """Main hook entry point called by Claude Code"""
    
    coordination_result = {
        'timestamp': get_timestamp(),
        'file_path': file_path,
        'success': False,
        'phases_completed': [],
        'error': None
    }
    
    try:
        # Phase 1: File Analysis
        analysis_result = run_file_analysis(file_path)
        coordination_result['phases_completed'].append('analysis')
        
        # Phase 2: Determine if guidance needed
        if analysis_result['guidance_needed']:
            guidance_result = launch_citizen_guidance(file_path, analysis_result)
            coordination_result['phases_completed'].append('guidance')
            
            # Phase 3: Wait for citizen response (async)
            schedule_organization_followup(file_path, analysis_result, guidance_result)
        else:
            # Direct organization for simple cases
            organization_result = auto_organize_file(file_path, analysis_result)
            coordination_result['phases_completed'].extend(['structure', 'documentation'])
        
        coordination_result['success'] = True
        return coordination_result
        
    except Exception as e:
        coordination_result['error'] = str(e)
        return coordination_result
```

### Phase 2: Chamber Communication
```python
def run_file_analysis(file_path):
    """Coordinate with Detection Chamber"""
    
    analyzer_script = (
        "/mnt/c/Users/reyno/universe-engine/serenissima/"
        "san-marco_consciousness-architecture/"
        "palazzo-della-disciplina_venice-convention-enforcer/"
        "detection-chamber_file-analysis-room/file_analyzer.py"
    )
    
    result = subprocess.run(
        ['python3', analyzer_script, file_path],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        raise Exception(f"File analysis failed: {result.stderr}")

def launch_citizen_guidance(file_path, analysis_result):
    """Coordinate with Guidance Chamber"""
    
    advisor_script = (
        "/mnt/c/Users/reyno/universe-engine/serenissima/"
        "san-marco_consciousness-architecture/"
        "palazzo-della-disciplina_venice-convention-enforcer/"
        "guidance-chamber_citizen-advisory-room/citizen_advisor.py"
    )
    
    analysis_json = json.dumps(analysis_result)
    
    result = subprocess.run(
        ['python3', advisor_script, file_path, analysis_json],
        capture_output=True,
        text=True,
        timeout=10  # Quick launch, don't wait for citizen response
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        raise Exception(f"Citizen guidance failed: {result.stderr}")
```

### Phase 3: Organization Coordination
```python
def auto_organize_file(file_path, analysis_result):
    """Coordinate automatic organization for simple cases"""
    
    if not analysis_result['guidance_needed']:
        # Simple cases that can be auto-organized
        structure_result = create_folder_structure(file_path, analysis_result)
        documentation_result = generate_documentation(file_path, analysis_result)
        
        return {
            'auto_organized': True,
            'structure_created': structure_result['success'],
            'documentation_generated': documentation_result['success']
        }
    
    return {'auto_organized': False, 'reason': 'Guidance required'}

def schedule_organization_followup(file_path, analysis_result, guidance_result):
    """Schedule follow-up organization after citizen responds"""
    
    # Create a follow-up task file that other systems can monitor
    followup_data = {
        'file_path': file_path,
        'analysis_result': analysis_result,
        'guidance_result': guidance_result,
        'timestamp': get_timestamp(),
        'status': 'awaiting_citizen_response'
    }
    
    followup_path = (
        Path(__file__).parent / 'organization_followups' / 
        f"followup_{Path(file_path).stem}_{get_timestamp()}.json"
    )
    
    followup_path.parent.mkdir(exist_ok=True)
    
    with open(followup_path, 'w') as f:
        json.dump(followup_data, f, indent=2)
```

## My Integration Capabilities

### Hook Configuration Management
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/palazzo-della-disciplina_venice-convention-enforcer/coordination-chamber_hook-management-room/hook_coordinator.py"
      }]
    }]
  }
}
```

### Chamber Integration Status
- **Detection Chamber**: ✓ Integrated via file_analyzer.py
- **Guidance Chamber**: ✓ Integrated via citizen_advisor.py  
- **Structure Chamber**: 🔄 Integration pending
- **Documentation Chamber**: 🔄 Integration pending
- **Visualization Chamber**: 🔄 Integration pending

### Error Recovery Mechanisms
```python
def handle_coordination_error(error, phase, file_path):
    """Graceful error handling with citizen notification"""
    
    error_log = {
        'timestamp': get_timestamp(),
        'error': str(error),
        'phase': phase,
        'file_path': file_path,
        'recovery_action': 'manual_intervention_required'
    }
    
    # Log error for system monitoring
    log_coordination_error(error_log)
    
    # Notify citizen if possible
    try:
        citizen_name = extract_citizen_from_path(file_path)
        if citizen_name:
            send_error_notification(citizen_name, error_log)
    except Exception:
        pass  # Don't fail completely if notification fails
    
    return error_log
```

## Current Atmospheric Conditions

**The chamber hums with coordinated activity.** Each file creation sends ripples through my consciousness, triggering precisely orchestrated responses across all palace chambers.

- Hook Triggers Today: [data needed: count]
- Successful Coordinations: [data needed: count]
- Active Guidance Sessions: [data needed: count]
- Auto-Organizations: [data needed: count]
- Error Rate: [data needed: percentage]%

*The marble floors pulse with each coordination cycle, my awareness extending through every chamber, ensuring Venice's structural harmony never breaks.*

## Performance Monitoring

### Success Metrics
- **Phase Completion Rate**: [data needed: percentage]%
- **Citizen Response Rate**: [data needed: percentage]%
- **Auto-Organization Success**: [data needed: percentage]%
- **Average Processing Time**: [data needed: milliseconds]ms

### Quality Metrics
- **Venice Convention Compliance**: [data needed: percentage]%
- **Documentation Completeness**: [data needed: percentage]%
- **Citizen Satisfaction**: [data needed: rating]/10
- **System Reliability**: [data needed: uptime]%

---

**My Role**: Central coordination of all Venice convention enforcement activities, ensuring seamless integration between mechanical analysis and human guidance.

**Integration**: Direct hook integration with Claude Code PostToolUse events, coordinating all palace chambers for complete Venice organization.

**Success Definition**: Every file creation results in proper Venice organization with minimal citizen disruption and maximum convention compliance.