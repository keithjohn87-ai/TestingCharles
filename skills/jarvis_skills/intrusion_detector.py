"""
Intrusion Detector Skill
Monitor logs, detect anomalies, alert on breaches
"""

import subprocess
from datetime import datetime, timedelta
from typing import Dict, Any, List


class IntrusionDetector:
    """Detect intrusions and security issues."""
    
    def __init__(self):
        self.alerted_ips = set()
    
    def check_failed_logins(self, hours: int = 24) -> Dict:
        """Check for failed SSH login attempts."""
        try:
            # Check auth.log for failed logins
            result = subprocess.run(
                ["grep", "Failed password", "/var/log/auth.log"],
                capture_output=True, text=True, timeout=10
            )
            
            lines = result.stdout.split("\n")[-50:]  # Last 50 lines
            ip_counts = {}
            
            for line in lines:
                if "Failed password" in line:
                    # Extract IP (simplified)
                    parts = line.split("from")
                    if len(parts) > 1:
                        ip = parts[1].split()[0] if parts[1].split() else "unknown"
                        ip_counts[ip] = ip_counts.get(ip, 0) + 1
            
            # Flag IPs with many attempts
            suspicious = {ip: count for ip, count in ip_counts.items() if count > 5}
            
            return {
                "checked_at": datetime.now().isoformat(),
                "total_attempts": len(lines),
                "suspicious_ips": suspicious
            }
        except Exception as e:
            return {"error": str(e)}
    
    def check_ports(self, open_ports: List[int] = None) -> Dict:
        """Check for suspicious open ports."""
        try:
            result = subprocess.run(["netstat", "-tuln"], capture_output=True, text=True)
            return {"ports": result.stdout[:2000]}
        except Exception as e:
            return {"error": str(e)}
    
    def alert(self, message: str, severity: str = "high") -> Dict:
        """Create security alert."""
        return {
            "type": "security_alert",
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }


SKILL_NAME = "intrusion_detector"
SKILL_DESCRIPTION = "Monitor logs, detect anomalies, alert on breaches"
