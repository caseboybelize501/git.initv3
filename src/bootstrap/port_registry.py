import subprocess
import re
from typing import List, Dict


class PortRegistry:
    def __init__(self):
        pass

    async def get_active_ports(self) -> List[Dict]:
        ports = []
        
        try:
            # Run netstat command
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            for line in lines:
                if 'LISTEN' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        # Extract port number
                        local_address = parts[1]
                        match = re.search(r':(\d+)$', local_address)
                        if match:
                            port = int(match.group(1))
                            
                            # Try to get process name
                            try:
                                pid_result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
                                pid_lines = pid_result.stdout.split('\n')
                                for pid_line in pid_lines:
                                    if f':{port} ' in pid_line and 'LISTEN' in pid_line:
                                        pid_match = re.search(r'\s+(\d+)$', pid_line)
                                        if pid_match:
                                            pid = pid_match.group(1)
                                            process_name = self._get_process_name(pid)
                                            ports.append({
                                                'port': port,
                                                'pid': pid,
                                                'process_name': process_name
                                            })
                            except Exception:
                                # If we can't get process name, just add port
                                ports.append({
                                    'port': port,
                                    'pid': None,
                                    'process_name': 'unknown'
                                })
        except Exception as e:
            print(f"Error getting active ports: {e}")
        
        return ports

    def _get_process_name(self, pid: str) -> str:
        try:
            result = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            if len(lines) > 1:
                return lines[1].split()[0]
        except Exception:
            pass
        return 'unknown'