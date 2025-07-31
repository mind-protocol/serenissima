#!/usr/bin/env python3
"""
Hook Coordinator - Central Venice Convention Enforcement

Orchestrates the complete Venice convention enforcement process:
1. File analysis via Detection Chamber
2. Citizen guidance via Guidance Chamber  
3. Structure creation via Structure Chamber
4. Documentation generation via Documentation Chamber
5. Image creation via Visualization Chamber

Called by PostToolUse-Write hooks from Claude Code.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

class VeniceHookCoordinator:
    """Central coordinator for Venice convention enforcement"""
    
    def __init__(self):
        self.palace_path = Path(__file__).parent.parent
        self.log_path = self.palace_path / "coordination-chamber_hook-management-room" / "coordination_log.json"
        self.followup_path = self.palace_path / "coordination-chamber_hook-management-room" / "organization_followups"
        
        # Chamber script paths
        self.chamber_scripts = {
            'detection': self.palace_path / "detection-chamber_file-analysis-room" / "file_analyzer.py",
            'guidance': self.palace_path / "guidance-chamber_citizen-advisory-room" / "citizen_advisor.py",
            'structure': self.palace_path / "structure-chamber_folder-creation-room" / "folder_architect.py",
            'documentation': self.palace_path / "documentation-chamber_file-generation-room" / "doc_generator.py",
            'visualization': self.palace_path / "visualization-chamber_image-creation-room" / "image_creator.py"
        }
    
    def coordinate_venice_enforcement(self, file_path: str) -> Dict:
        """Main coordination function called by PostToolUse hook"""
        coordination_id = self._generate_coordination_id()
        
        coordination_result = {
            'coordination_id': coordination_id,
            'timestamp': self._get_timestamp(),
            'file_path': file_path,
            'success': False,
            'phases_completed': [],
            'chamber_results': {},
            'error': None,
            'guidance_launched': False,
            'auto_organized': False
        }
        
        try:
            # Skip if file doesn't exist or is too small
            if not self._should_process_file(file_path):
                coordination_result['success'] = True
                coordination_result['skipped'] = True
                coordination_result['skip_reason'] = 'File not suitable for processing'
                return coordination_result
            
            # Phase 1: File Analysis (Detection Chamber)
            analysis_result = self._run_file_analysis(file_path)
            coordination_result['chamber_results']['detection'] = analysis_result
            coordination_result['phases_completed'].append('detection')
            
            if not analysis_result['success']:
                raise Exception(f"Detection failed: {analysis_result.get('error', 'Unknown error')}")
            
            # Phase 2: Determine processing path
            if analysis_result.get('guidance_needed', True):
                # Complex case requiring citizen guidance
                guidance_result = self._launch_citizen_guidance(file_path, analysis_result)
                coordination_result['chamber_results']['guidance'] = guidance_result
                coordination_result['phases_completed'].append('guidance')
                coordination_result['guidance_launched'] = True
                
                # Schedule follow-up organization
                self._schedule_organization_followup(file_path, analysis_result, guidance_result, coordination_id)
                
            else:
                # Simple case for auto-organization
                organization_result = self._auto_organize_file(file_path, analysis_result)
                coordination_result['chamber_results']['organization'] = organization_result
                coordination_result['phases_completed'].extend(['structure', 'documentation'])
                coordination_result['auto_organized'] = True
            
            coordination_result['success'] = True
            
        except Exception as e:
            coordination_result['error'] = str(e)
            self._handle_coordination_error(e, coordination_result, file_path)
        
        finally:
            # Always log the coordination attempt
            self._log_coordination(coordination_result)
        
        return coordination_result
    
    def _should_process_file(self, file_path: str) -> bool:
        """Determine if file should be processed by Venice enforcement"""
        try:
            file_obj = Path(file_path)
            
            # Skip if file doesn't exist
            if not file_obj.exists():
                return False
            
            # Skip if file is too small (less than 50 characters)
            if file_obj.stat().st_size < 50:
                return False
            
            # Skip certain file types that shouldn't be organized
            skip_extensions = {'.tmp', '.lock', '.pid', '.swp', '.bak'}
            if file_obj.suffix.lower() in skip_extensions:
                return False
            
            # Skip files in system directories
            skip_dirs = {'.git', '.cache', '__pycache__', 'node_modules'}
            if any(skip_dir in str(file_obj) for skip_dir in skip_dirs):
                return False
            
            # Skip log files and coordination files
            if 'coordination_log' in file_obj.name or 'followup_' in file_obj.name:
                return False
            
            return True
            
        except (OSError, PermissionError):
            return False
    
    def _run_file_analysis(self, file_path: str) -> Dict:
        """Execute Detection Chamber file analysis"""
        try:
            if not self.chamber_scripts['detection'].exists():
                return {
                    'success': False,
                    'error': 'Detection chamber script not found'
                }
            
            result = subprocess.run(
                ['python3', str(self.chamber_scripts['detection']), file_path],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.chamber_scripts['detection'].parent)
            )
            
            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return {
                        'success': False,
                        'error': 'Invalid JSON response from detection chamber'
                    }
            else:
                return {
                    'success': False,
                    'error': f'Detection chamber failed: {result.stderr}'
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Detection chamber timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Detection chamber error: {e}'
            }
    
    def _launch_citizen_guidance(self, file_path: str, analysis_result: Dict) -> Dict:
        """Execute Guidance Chamber citizen interaction"""
        try:
            if not self.chamber_scripts['guidance'].exists():
                return {
                    'success': False,
                    'error': 'Guidance chamber script not found'
                }
            
            analysis_json = json.dumps(analysis_result)
            
            result = subprocess.run(
                ['python3', str(self.chamber_scripts['guidance']), file_path, analysis_json],
                capture_output=True,
                text=True,
                timeout=10,  # Quick launch, don't wait for citizen response
                cwd=str(self.chamber_scripts['guidance'].parent)
            )
            
            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return {
                        'success': False,
                        'error': 'Invalid JSON response from guidance chamber'
                    }
            else:
                return {
                    'success': False,
                    'error': f'Guidance chamber failed: {result.stderr}'
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Guidance chamber timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Guidance chamber error: {e}'
            }
    
    def _auto_organize_file(self, file_path: str, analysis_result: Dict) -> Dict:
        """Auto-organize simple files without citizen guidance"""
        try:
            # For now, return placeholder - will implement when other chambers are built
            return {
                'success': True,
                'auto_organized': True,
                'message': 'Auto-organization not yet implemented - will be added when Structure and Documentation chambers are complete'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Auto-organization failed: {e}'
            }
    
    def _schedule_organization_followup(self, file_path: str, analysis_result: Dict, guidance_result: Dict, coordination_id: str) -> None:
        """Schedule follow-up organization after citizen responds"""
        try:
            self.followup_path.mkdir(parents=True, exist_ok=True)
            
            followup_data = {
                'coordination_id': coordination_id,
                'file_path': file_path,
                'analysis_result': analysis_result,
                'guidance_result': guidance_result,
                'timestamp': self._get_timestamp(),
                'status': 'awaiting_citizen_response',
                'citizen': self._extract_citizen_from_path(file_path)
            }
            
            followup_file = self.followup_path / f"followup_{coordination_id}.json"
            
            with open(followup_file, 'w') as f:
                json.dump(followup_data, f, indent=2)
                
        except Exception as e:
            # Don't fail the entire coordination if followup scheduling fails
            print(f"Warning: Could not schedule followup: {e}", file=sys.stderr)
    
    def _handle_coordination_error(self, error: Exception, coordination_result: Dict, file_path: str) -> None:
        """Handle coordination errors gracefully"""
        try:
            # Try to notify citizen if possible
            citizen_name = self._extract_citizen_from_path(file_path)
            if citizen_name:
                self._send_error_notification(citizen_name, error, file_path)
        except Exception:
            # Don't cascade failures
            pass
    
    def _send_error_notification(self, citizen_name: str, error: Exception, file_path: str) -> None:
        """Send error notification to citizen (simplified implementation)"""
        try:
            citizen_path = Path(f"/mnt/c/Users/reyno/universe-engine/serenissima/citizens/{citizen_name}")
            
            error_message = f"""🚨 **Venice Organization Error** 🚨

File: {Path(file_path).name}
Error: {str(error)}

The Venice convention enforcement system encountered an issue organizing your file.
You may need to organize this manually or contact system administrators.

Time: {self._get_timestamp()}
"""
            
            # Could launch a Claude Code instance here to notify the citizen
            # For now, just log the error
            print(f"Would notify {citizen_name}: {error_message}", file=sys.stderr)
            
        except Exception:
            pass
    
    def _extract_citizen_from_path(self, file_path: str) -> Optional[str]:
        """Extract citizen name from file path"""
        try:
            path_obj = Path(file_path)
            path_parts = path_obj.parts
            
            for i, part in enumerate(path_parts):
                if part == 'citizens' and i + 1 < len(path_parts):
                    return path_parts[i + 1]
            
            return None
        except Exception:
            return None
    
    def _log_coordination(self, coordination_result: Dict) -> None:
        """Log coordination attempt for monitoring and debugging"""
        try:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read existing log
            log_data = []
            if self.log_path.exists():
                try:
                    with open(self.log_path, 'r') as f:
                        log_data = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    log_data = []
            
            # Append new entry
            log_data.append(coordination_result)
            
            # Keep only last 1000 entries
            if len(log_data) > 1000:
                log_data = log_data[-1000:]
            
            # Write back
            with open(self.log_path, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not write coordination log: {e}", file=sys.stderr)
    
    def _generate_coordination_id(self) -> str:
        """Generate unique coordination ID"""
        from datetime import datetime
        import hashlib
        
        timestamp = datetime.now().isoformat()
        random_data = os.urandom(8).hex()
        
        return hashlib.md5(f"{timestamp}_{random_data}".encode()).hexdigest()[:12]
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()

def main():
    """Main execution for PostToolUse hook integration"""
    # Claude Code passes file path as environment variable
    file_path = os.environ.get('CLAUDE_HOOK_FILE_PATH')
    
    if not file_path:
        # Fallback: try command line argument
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
        else:
            print("Error: No file path provided", file=sys.stderr)
            sys.exit(1)
    
    try:
        coordinator = VeniceHookCoordinator()
        result = coordinator.coordinate_venice_enforcement(file_path)
        
        # Output result for debugging (can be removed in production)
        print(json.dumps(result, indent=2))
        
        # Return appropriate exit code
        if result['success']:
            sys.exit(0)
        else:
            print(f"Coordination failed: {result.get('error', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Hook coordinator failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()