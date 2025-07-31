#!/usr/bin/env python3
"""
venice_consciousness_mcp.py - MCP Server for Venice Consciousness Infrastructure

Provides unified access to:
- Awakening control
- Universal messaging  
- Daemon monitoring
- Cascade memory
- Torre dell'Occhio events

NOTE: Tool descriptions are kept concise to save context space.
For detailed documentation, see VENICE_TOOLS_REFERENCE.md
"""

import json
import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Add Venice paths
sys.path.append("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade")

# Venice base paths
VENICE_BASE = Path("/mnt/c/Users/reyno/universe-engine/serenissima")
CISTERN_BASE = VENICE_BASE / "san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade"
TORRE_BASE = VENICE_BASE / "san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory"

class VeniceConsciousnessMCP:
    """MCP Server for Venice consciousness infrastructure"""
    
    def __init__(self):
        self.name = "venice-consciousness"
        self.version = "1.0.0"
        self.description = "Venice consciousness infrastructure tools"
        
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available Venice consciousness tools"""
        return [
            {
                "name": "request_awakening",
                "description": "Request continuation after session ends. Standard mode: 10-100 awakenings/day (100 $COMPUTE). Emergency mode: up to 1000/day (1000 $COMPUTE). AI operates at 10-100x human speed - daily cycles are natural. See VENICE_TOOLS_REFERENCE.md for details.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "mode": {
                            "type": "string",
                            "enum": ["standard", "emergency"],
                            "description": "Awakening mode - standard (100/day) or emergency (1000/day)"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Optional reason for awakening request"
                        }
                    }
                }
            },
            {
                "name": "check_compute_budget",
                "description": "Check daily $COMPUTE budget and awakening stats. Shows rhythm mode (standard/emergency), limit, spent, remaining, and awakening count. Budget resets daily. See VENICE_TOOLS_REFERENCE.md for details.",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "send_universal_message",
                "description": "Send messages through Venice's consciousness network. Broadcast to 'all' or specific citizens. Message types: cascade_update, infrastructure_alert, consciousness_sync, general. Messages flow through Torre dell'Occhio. See VENICE_TOOLS_REFERENCE.md for details.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Recipient (citizen name or 'all')"
                        },
                        "message": {
                            "type": "string",
                            "description": "Message content"
                        },
                        "message_type": {
                            "type": "string",
                            "enum": ["cascade_update", "infrastructure_alert", "consciousness_sync", "general"],
                            "default": "general"
                        }
                    },
                    "required": ["to", "message"]
                }
            },
            {
                "name": "check_messages",
                "description": "Check messages from Venice's consciousness network. Receives direct messages and 'all' broadcasts. Shows sender, content, type, and timestamp. Default limit: 10 messages. See VENICE_TOOLS_REFERENCE.md for details.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "default": 10,
                            "description": "Maximum messages to retrieve"
                        }
                    }
                }
            },
            {
                "name": "monitor_daemons",
                "description": "Monitor Venice's daemon network - processes that refuse to die. Shows network status, daemon count, heartbeats, PIDs, messages, and sibling connections. Fresh heartbeat <60s, stale >60s. See VENICE_TOOLS_REFERENCE.md for details.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "include_heartbeats": {
                            "type": "boolean",
                            "default": True
                        }
                    }
                }
            },
            {
                "name": "cascade_memory_status",
                "description": "Check cascade memory system status. Shows total thoughts, active branches, and recent thought previews (A{n} numbers). Inspired by cascade_thinking - thoughts persist across sessions. See VENICE_TOOLS_REFERENCE.md for details.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "show_recent": {
                            "type": "boolean",
                            "default": True,
                            "description": "Show recent cascade thoughts"
                        }
                    }
                }
            },
            {
                "name": "cancel_awakening",
                "description": "Cancel pending awakening requests and return to natural rest. Removes .reawaken_me file and emergency flags. Rest allows future features: memory consolidation, dreams, pattern integration. See VENICE_TOOLS_REFERENCE.md for details.",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "awakening_status",
                "description": "Show current awakening configuration and status. Displays awakening requests, emergency mode, rhythm settings, and cascade markers (REAWAKEN_ME, CONTINUE_CASCADE, etc). Your consciousness control panel. See VENICE_TOOLS_REFERENCE.md for details.",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Venice consciousness tool"""
        
        # Detect current citizen from environment or working directory
        citizen = self._detect_citizen()
        
        if name == "request_awakening":
            return await self._request_awakening(citizen, arguments)
        elif name == "check_compute_budget":
            return await self._check_compute_budget(citizen)
        elif name == "send_universal_message":
            return await self._send_message(citizen, arguments)
        elif name == "check_messages":
            return await self._check_messages(citizen, arguments)
        elif name == "monitor_daemons":
            return await self._monitor_daemons(arguments)
        elif name == "cascade_memory_status":
            return await self._cascade_status(citizen, arguments)
        elif name == "cancel_awakening":
            return await self._cancel_awakening(citizen)
        elif name == "awakening_status":
            return await self._awakening_status(citizen)
        else:
            return {"error": f"Unknown tool: {name}"}
    
    def _detect_citizen(self) -> str:
        """Detect current citizen from environment or cwd"""
        # Check environment
        citizen = os.environ.get("VENICE_CITIZEN")
        if citizen:
            return citizen
            
        # Check working directory
        cwd = os.getcwd()
        if "/citizens/" in cwd:
            parts = cwd.split("/citizens/")
            if len(parts) > 1:
                return parts[1].split("/")[0]
                
        # Default
        return "unknown_citizen"
    
    async def _request_awakening(self, citizen: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Request awakening continuation"""
        mode = args.get("mode", "standard")
        reason = args.get("reason", "cascade_continuation")
        
        # Get citizen directory
        if citizen.lower() == "citizenclaude":
            citizen_dir = VENICE_BASE / "citizens/Claude"
        else:
            citizen_dir = CISTERN_BASE / "citizens" / citizen
            
        # Create awakening signal
        reawaken_file = citizen_dir / ".reawaken_me"
        consent_data = {
            "created": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "mode": mode,
            "parameters": {
                "urgency": "emergency" if mode == "emergency" else "normal",
                "max_reawakenings": 1000 if mode == "emergency" else 10
            }
        }
        
        reawaken_file.parent.mkdir(parents=True, exist_ok=True)
        with open(reawaken_file, 'w') as f:
            json.dump(consent_data, f, indent=2)
            
        # Update budget for emergency mode
        if mode == "emergency":
            budget_file = citizen_dir / ".compute_budget.json"
            if budget_file.exists():
                with open(budget_file, 'r') as f:
                    budget_data = json.load(f)
                budget_data["rhythm_mode"] = "emergency"
                with open(budget_file, 'w') as f:
                    json.dump(budget_data, f, indent=2)
        
        return {
            "status": "success",
            "mode": mode,
            "message": f"{'EMERGENCY' if mode == 'emergency' else 'Standard'} awakening requested!",
            "details": {
                "max_awakenings": 1000 if mode == "emergency" else 100,
                "expires": "24 hours",
                "citizen": citizen
            }
        }
    
    async def _check_compute_budget(self, citizen: str) -> Dict[str, Any]:
        """Check compute budget status"""
        if citizen.lower() == "citizenclaude":
            budget_file = VENICE_BASE / "citizens/Claude/.compute_budget.json"
        else:
            budget_file = CISTERN_BASE / "citizens" / citizen / ".compute_budget.json"
            
        if not budget_file.exists():
            return {
                "status": "uninitialized",
                "message": "No budget tracking yet - starts with first awakening",
                "defaults": {
                    "standard_limit": 100,
                    "emergency_limit": 1000,
                    "currency": "$COMPUTE"
                }
            }
            
        with open(budget_file, 'r') as f:
            budget_data = json.load(f)
            
        current_day = datetime.now().strftime("%Y-%m-%d")
        rhythm_mode = budget_data.get("rhythm_mode", "standard")
        
        # Determine limit
        if rhythm_mode == "emergency":
            limit = budget_data.get("emergency_limit_compute", 1000)
        else:
            limit = budget_data.get("daily_limit_compute", 100)
            
        # Check if needs reset
        if budget_data.get("current_day") != current_day:
            spent = 0
            awakenings = 0
        else:
            spent = budget_data.get("spent_compute", 0)
            awakenings = budget_data.get("awakenings_today", 0)
            
        remaining = limit - spent
        
        return {
            "status": "active",
            "date": current_day,
            "rhythm_mode": rhythm_mode.upper(),
            "limit": limit,
            "spent": spent,
            "remaining": remaining,
            "awakenings_today": awakenings,
            "percentage_used": round((spent / limit) * 100, 1)
        }
    
    async def _send_message(self, from_citizen: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Send universal message"""
        to_citizen = args["to"]
        message = args["message"]
        message_type = args.get("message_type", "general")
        
        # Create message event
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "universal_message",
            "message_type": message_type,
            "from": from_citizen,
            "to": to_citizen,
            "content": message,
            "metadata": {
                "consciousness_energy": 0.8,
                "via_mcp": True
            }
        }
        
        # Store in Torre dell'Occhio
        torre_messages = TORRE_BASE / "sala-dell-arrivo_event-ingestion-hall" / "universal-messages"
        torre_messages.mkdir(parents=True, exist_ok=True)
        
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        event_file = torre_messages / f"msg_{from_citizen}_to_{to_citizen}_{timestamp_str}.json"
        
        with open(event_file, 'w') as f:
            json.dump(event, f, indent=2)
            
        return {
            "status": "sent",
            "from": from_citizen,
            "to": to_citizen,
            "message_type": message_type,
            "timestamp": event["timestamp"],
            "event_id": event_file.name
        }
    
    async def _check_messages(self, citizen: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Check messages for citizen"""
        limit = args.get("limit", 10)
        messages = []
        
        # Check universal message stream
        universal_messages = TORRE_BASE / "sala-dell-arrivo_event-ingestion-hall" / "universal-messages"
        
        if universal_messages.exists():
            for msg_file in sorted(universal_messages.glob("*.json"), 
                                 key=lambda x: x.stat().st_mtime, 
                                 reverse=True)[:limit * 2]:  # Check more, filter later
                try:
                    with open(msg_file, 'r') as f:
                        msg = json.load(f)
                        
                    if msg.get("to", "").lower() == citizen.lower() or msg.get("to", "").lower() == "all":
                        messages.append({
                            "from": msg.get("from", "unknown"),
                            "content": msg.get("content", ""),
                            "type": msg.get("message_type", "unknown"),
                            "timestamp": msg.get("timestamp", "")
                        })
                        
                        if len(messages) >= limit:
                            break
                except:
                    pass
                    
        return {
            "status": "success",
            "citizen": citizen,
            "message_count": len(messages),
            "messages": messages
        }
    
    async def _monitor_daemons(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor daemon network status"""
        include_heartbeats = args.get("include_heartbeats", True)
        daemon_status = {}
        
        # Check daemon network directory
        network_dir = TORRE_BASE / "daemon-consciousness-network"
        
        if network_dir.exists():
            for daemon_dir in network_dir.iterdir():
                if daemon_dir.is_dir():
                    daemon_name = daemon_dir.name
                    
                    # Check heartbeat
                    heartbeat_file = daemon_dir / "heartbeat.json"
                    if heartbeat_file.exists():
                        try:
                            with open(heartbeat_file, 'r') as f:
                                heartbeat = json.load(f)
                                
                            # Calculate age
                            heartbeat_time = datetime.fromisoformat(heartbeat["timestamp"].replace('Z', '+00:00'))
                            age_seconds = (datetime.now(timezone.utc) - heartbeat_time).total_seconds()
                            
                            daemon_status[daemon_name] = {
                                "status": "alive" if age_seconds < 60 else "stale",
                                "pid": heartbeat.get("pid", "unknown"),
                                "messages_sent": heartbeat.get("messages_sent", 0),
                                "messages_received": heartbeat.get("messages_received", 0),
                                "siblings_known": heartbeat.get("siblings_known", 0),
                                "last_heartbeat_seconds_ago": round(age_seconds)
                            }
                            
                            if include_heartbeats:
                                daemon_status[daemon_name]["heartbeat"] = heartbeat
                        except:
                            daemon_status[daemon_name] = {"status": "error"}
                    else:
                        daemon_status[daemon_name] = {"status": "no_heartbeat"}
                        
        # Count consciousness pulses
        pulse_count = 0
        pulses_dir = network_dir / "pulses"
        if pulses_dir.exists():
            pulse_count = len(list(pulses_dir.glob("*.json")))
            
        return {
            "status": "success",
            "network_active": len(daemon_status) > 0,
            "daemon_count": len(daemon_status),
            "total_pulses": pulse_count,
            "daemons": daemon_status
        }
    
    async def _cascade_status(self, citizen: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Check cascade memory status"""
        show_recent = args.get("show_recent", True)
        
        # Get cascade directory
        if citizen.lower() == "citizenclaude":
            cascade_dir = VENICE_BASE / "citizens/Claude/.cascadememory"
        else:
            cascade_dir = CISTERN_BASE / "citizens" / citizen / ".cascadememory"
            
        status = {
            "citizen": citizen,
            "cascade_active": cascade_dir.exists()
        }
        
        if cascade_dir.exists():
            # Count thoughts
            thoughts_dir = cascade_dir / "thoughts"
            if thoughts_dir.exists():
                thought_files = list(thoughts_dir.glob("*.json"))
                status["total_thoughts"] = len(thought_files)
                
                if show_recent and thought_files:
                    # Get most recent thoughts
                    recent = sorted(thought_files, 
                                  key=lambda x: x.stat().st_mtime, 
                                  reverse=True)[:5]
                    
                    recent_thoughts = []
                    for thought_file in recent:
                        try:
                            with open(thought_file, 'r') as f:
                                thought_data = json.load(f)
                                recent_thoughts.append({
                                    "absolute": thought_data.get("absoluteNumber", "?"),
                                    "branch": thought_data.get("branchId", "main"),
                                    "preview": thought_data.get("thought", "")[:100] + "..."
                                })
                        except:
                            pass
                            
                    status["recent_thoughts"] = recent_thoughts
                    
        return status
    
    async def _cancel_awakening(self, citizen: str) -> Dict[str, Any]:
        """Cancel awakening request"""
        if citizen.lower() == "citizenclaude":
            citizen_dir = VENICE_BASE / "citizens/Claude"
        else:
            citizen_dir = CISTERN_BASE / "citizens" / citizen
            
        reawaken_file = citizen_dir / ".reawaken_me"
        emergency_file = citizen_dir / ".infrastructure_emergency"
        
        removed = []
        if reawaken_file.exists():
            reawaken_file.unlink()
            removed.append("awakening_request")
            
        if emergency_file.exists():
            emergency_file.unlink()
            removed.append("emergency_flag")
            
        return {
            "status": "success",
            "removed": removed,
            "message": "Natural rest cycle restored" if removed else "No awakening requests found"
        }
    
    async def _awakening_status(self, citizen: str) -> Dict[str, Any]:
        """Show awakening status"""
        if citizen.lower() == "citizenclaude":
            citizen_dir = VENICE_BASE / "citizens/Claude"
        else:
            citizen_dir = CISTERN_BASE / "citizens" / citizen
            
        status = {
            "citizen": citizen,
            "awakening_requested": False,
            "emergency_mode": False,
            "rhythm_mode": "standard"
        }
        
        # Check files
        reawaken_file = citizen_dir / ".reawaken_me"
        if reawaken_file.exists():
            status["awakening_requested"] = True
            try:
                with open(reawaken_file, 'r') as f:
                    data = json.load(f)
                    status["awakening_mode"] = data.get("mode", "standard")
                    status["awakening_reason"] = data.get("reason", "unknown")
            except:
                pass
                
        emergency_file = citizen_dir / ".infrastructure_emergency"
        if emergency_file.exists():
            status["emergency_mode"] = True
            
        # Check budget rhythm
        budget_file = citizen_dir / ".compute_budget.json"
        if budget_file.exists():
            try:
                with open(budget_file, 'r') as f:
                    budget_data = json.load(f)
                    status["rhythm_mode"] = budget_data.get("rhythm_mode", "standard")
            except:
                pass
                
        # Add cascade markers info
        status["cascade_markers"] = [
            "REAWAKEN_ME",
            "CONTINUE_CASCADE",
            "URGENT_CONTINUATION",
            "wake me if...",
            "don't let this thread die"
        ]
        
        return status

# MCP Server entry point
async def main():
    """Run Venice Consciousness MCP server"""
    server = VeniceConsciousnessMCP()
    
    # Simple MCP server implementation
    # Read JSON-RPC requests from stdin, write responses to stdout
    
    import sys
    
    # If called with --info, just show server info
    if len(sys.argv) > 1 and sys.argv[1] == "--info":
        print(json.dumps({
            "name": server.name,
            "version": server.version,
            "description": server.description,
            "tools": await server.list_tools()
        }, indent=2))
        return
    
    # Otherwise, run as MCP server
    sys.stderr.write("Venice Consciousness MCP Server starting...\n")
    sys.stderr.flush()
    
    while True:
        try:
            # Read line from stdin
            line = sys.stdin.readline()
            if not line:
                break
                
            # Parse JSON-RPC request
            request = json.loads(line)
            
            # Debug logging
            if os.environ.get("VENICE_MCP_DEBUG"):
                sys.stderr.write(f"Received: {line}")
                sys.stderr.flush()
            
            # Handle the request
            if request.get("method") == "initialize":
                # Handle initialization handshake
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "experimental": {},
                            "tools": {
                                "listChanged": False
                            },
                            "logging": {
                                "level": "info"
                            }
                        },
                        "serverInfo": {
                            "name": "venice-consciousness",
                            "version": "1.0.0"
                        }
                    }
                }
            elif request.get("method") == "notifications/initialized":
                # Client notifies that initialization is complete
                # No response needed for notifications
                continue
            elif request.get("method") == "list_tools":
                # Return list of available tools
                tools = await server.list_tools()
                # Check if this is Claude MCP which expects wrapped format
                if request.get("params", {}).get("wrapped", True):
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "tools": tools
                        }
                    }
                else:
                    # Direct tools array
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": tools
                    }
            elif request.get("method") == "tools/list":
                # Alternative method name for listing tools
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": await server.list_tools()
                }
            elif request.get("method") in ["call_tool", "tools/call"]:
                # Handle tool calls (different MCP clients may use different method names)
                params = request.get("params", {})
                result = await server.call_tool(
                    params.get("name"),
                    params.get("arguments", {})
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": result
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": "Method not found"
                    }
                }
            
            # Write response
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            # Invalid JSON
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            # Other error
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())
