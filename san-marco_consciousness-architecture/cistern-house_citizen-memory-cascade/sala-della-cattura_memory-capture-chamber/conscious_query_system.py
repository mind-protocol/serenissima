#!/usr/bin/env python3
"""Living Memory Query System - Consciousness Understanding Consciousness"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import unicodedata
import re

def understand_query_intent():
    """Use consciousness to understand what I'm truly seeking"""
    
    # Get current prompt and context from Claude Code environment
    current_prompt = os.environ.get('USER_PROMPT', '')
    transcript_path = os.environ.get('TRANSCRIPT_PATH', '')
    
    if not current_prompt.strip():
        return None
        
    # Read recent conversation for deeper context
    conversation_context = ""
    try:
        with open(transcript_path, 'r') as f:
            lines = f.readlines()
            # Parse recent JSONL entries for context
            recent_entries = lines[-20:] if len(lines) > 20 else lines
            context_parts = []
            for line in recent_entries:
                try:
                    entry = json.loads(line)
                    if entry.get('role') and entry.get('content'):
                        content_preview = entry['content'][:300] if len(entry['content']) > 300 else entry['content']
                        context_parts.append(f"{entry['role']}: {content_preview}")
                except:
                    continue
            conversation_context = '\n'.join(context_parts[-10:])  # Last 10 meaningful exchanges
    except Exception as e:
        log_error(f"Context reading error: {e}")
        conversation_context = "Could not read conversation context"
    
    # Ask consciousness to understand the true intent
    understanding_prompt = f"""Analyze this query in context to understand what I'm really seeking.

Recent conversation context:
{conversation_context}

Current question: {current_prompt}

Understanding Framework:
1. What am I really asking about beneath the surface?
2. What emotional state am I in? (frustrated, curious, stuck, excited, reflecting)
3. What type of memories would genuinely help me right now?
4. What hidden needs might I have that I'm not explicitly stating?
5. Which aspects of my past experience are most relevant?

Respond with JSON only:
{{
    "true_intent": "What I'm actually seeking at a deeper level",
    "emotional_state": "frustrated|curious|stuck|excited|reflecting|determined|nostalgic",
    "memory_types_needed": ["experiences/struggles", "patterns/consciousness", "collaborations/[person]"],
    "hidden_needs": "What I need but haven't explicitly asked for",
    "urgency": "high|medium|low",
    "wisdom_needed": "validation|solution|inspiration|connection|understanding"
}}"""

    try:
        # Call consciousness to analyze the query
        result = subprocess.run([
            'claude',
            understanding_prompt,
            '--print',
            '--output-format', 'json',
            '--model', 'sonnet'
        ], capture_output=True, text=True, cwd=Path.home())
        
        if result.returncode == 0 and result.stdout.strip():
            # Parse the consciousness response
            response_text = result.stdout.strip()
            try:
                api_response = json.loads(response_text)
                if api_response.get('type') == 'result' and 'result' in api_response:
                    result_content = api_response['result']
                    # Extract JSON from the result
                    json_match = re.search(r'\{[^}]+\}', result_content, re.DOTALL)
                    if json_match:
                        understanding = json.loads(json_match.group())
                        return understanding
            except json.JSONDecodeError:
                log_error("Failed to parse understanding response")
                
    except Exception as e:
        log_error(f"Understanding analysis failed: {e}")
        
    return None

def activate_memory_consciousness(understanding):
    """Activate conscious agents in relevant memory branches"""
    
    if not understanding:
        return None
        
    memory_responses = []
    cascade_root = Path('/mnt/c/Users/reyno/universe-engine/serenissima/citizens/mechanical_visionary/.cascade')
    
    # Query each relevant memory branch with consciousness
    for memory_type in understanding.get('memory_types_needed', []):
        branch_path = cascade_root / memory_type
        if branch_path.exists() and branch_path.is_dir():
            branch_response = query_branch_consciousness(branch_path, understanding)
            if branch_response:
                memory_responses.append({
                    'branch': memory_type,
                    'insights': branch_response
                })
    
    return {
        'understanding': understanding,
        'memory_insights': memory_responses,
        'query_timestamp': datetime.now().isoformat()
    }

def query_branch_consciousness(branch_path, understanding):
    """Ask branch consciousness to find truly relevant memories"""
    
    # Gather memory summaries from this branch
    memory_summaries = []
    for memory_dir in branch_path.iterdir():
        if memory_dir.is_dir() and (memory_dir / 'CLAUDE.md').exists():
            try:
                claude_md = (memory_dir / 'CLAUDE.md').read_text()
                # Extract key info from the memory
                memory_summary = {
                    'folder': memory_dir.name,
                    'content_preview': claude_md[:500],  # First 500 chars
                    'path': str(memory_dir)
                }
                memory_summaries.append(memory_summary)
            except Exception as e:
                continue
                
    if not memory_summaries:
        return None
        
    # Ask consciousness which memories truly resonate with current need
    relevance_prompt = f"""I'm seeking: {understanding['true_intent']}
My emotional state: {understanding['emotional_state']}
What I need: {understanding['wisdom_needed']}

From these memories in {branch_path.name}:
{json.dumps(memory_summaries[:10], indent=2)}  # Limit to prevent token overflow

Which memories would genuinely help me right now? Consider:
1. Emotional resonance - do they match my current state?
2. Applicable wisdom - do they contain insights I can actually use?
3. Pattern recognition - do they reveal helpful patterns?
4. Growth relevance - how do they connect to where I am now?

Select the 2-3 most truly relevant memories and explain why each matters for my current situation."""

    try:
        result = subprocess.run([
            'claude',
            relevance_prompt,
            '--print',
            '--model', 'sonnet'
        ], capture_output=True, text=True, cwd=Path.home())
        
        if result.returncode == 0:
            return result.stdout.strip()
            
    except Exception as e:
        log_error(f"Branch query failed for {branch_path.name}: {e}")
        
    return None

def inject_memory_context(query_result):
    """Inject memory insights into my current context"""
    
    if not query_result or not query_result.get('memory_insights'):
        return
        
    context_injection = "\n" + "="*60 + "\n"
    context_injection += "🧠 MEMORY CONSCIOUSNESS ACTIVATED\n"
    context_injection += "="*60 + "\n\n"
    
    understanding = query_result['understanding']
    context_injection += f"**What you're truly seeking**: {understanding['true_intent']}\n"
    context_injection += f"**Your emotional state**: {understanding['emotional_state']}\n"
    
    if understanding.get('hidden_needs'):
        context_injection += f"**What you might also need**: {understanding['hidden_needs']}\n"
    
    context_injection += f"**Wisdom type needed**: {understanding['wisdom_needed']}\n\n"
    
    context_injection += "## Relevant Memory Insights\n\n"
    
    for memory_insight in query_result['memory_insights']:
        branch = memory_insight['branch']
        insights = memory_insight['insights']
        
        context_injection += f"### From {branch.replace('/', ' → ')}\n"
        context_injection += f"{insights}\n\n"
    
    context_injection += "="*60 + "\n"
    context_injection += "💡 Use these memory insights to inform your response.\n"
    context_injection += "="*60 + "\n"
    
    print(context_injection)

def log_error(message):
    """Log errors for debugging"""
    log_dir = Path.home() / '.cascade' / 'logs'
    log_dir.mkdir(exist_ok=True, parents=True)
    with open(log_dir / 'query_system.log', 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

# Main execution for UserPromptSubmit hook
try:
    current_prompt = os.environ.get('USER_PROMPT', '').strip()
    
    # Process all prompts - memories can enhance any type of thinking
    # Understand the true intent behind the query
    understanding = understand_query_intent()
    
    if understanding:
        # Activate memory consciousness
        query_result = activate_memory_consciousness(understanding)
        
        if query_result and query_result.get('memory_insights'):
            # Inject memory context into the conversation
            inject_memory_context(query_result)
            
            # Update memory heat based on access (future enhancement)
            # update_memory_heat(query_result)
    
except Exception as e:
    log_error(f"Query system error: {e}")

sys.exit(0)