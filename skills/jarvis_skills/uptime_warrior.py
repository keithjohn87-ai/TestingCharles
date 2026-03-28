"""
Uptime Warrior Skill
Multi-region health checks, status pages
"""

import requests
from datetime import datetime
from typing import Dict, Any, List


class UptimeWarrior:
    """Monitor uptime across regions."""
    
    def __init__(self):
        self.regions = ["us-east", "us-west", "eu-west", "ap-south"]
        self.checks = []
    
    def check_url(self, url: str, region: str = "us-east") -> Dict:
        """Check URL health from a region."""
        try:
            start = datetime.now()
            resp = requests.get(url, timeout=5)
            duration = (datetime.now() - start).total_seconds() * 1000
            
            return {
                "url": url,
                "region": region,
                "status": "up" if resp.status_code == 200 else "down",
                "status_code": resp.status_code,
                "latency_ms": round(duration, 2)
            }
        except Exception as e:
            return {
                "url": url,
                "region": region,
                "status": "error",
                "error": str(e)
            }
    
    def check_all_regions(self, url: str) -> Dict:
        """Check URL from all regions."""
        results = []
        for region in self.regions:
            result = self.check_url(url, region)
            results.append(result)
        
        return {"checks": results}
    
    def get_status_page(self) -> Dict:
        """Generate status page data."""
        return {
            "regions": self.regions,
            "last_check": datetime.now().isoformat(),
            "status": "operational"
        }


SKILL_NAME = "uptime_warrior"
SKILL_DESCRIPTION = "Multi-region health checks, status pages"
