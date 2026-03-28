"""
Site Deployer Skill
Push to GitHub Pages, CDN purge, cache busting
"""

import subprocess
from typing import Dict, Any


class SiteDeployer:
    """Deploy sites to hosting."""
    
    def __init__(self, site_path: str = None, remote: str = "origin"):
        self.site_path = site_path
        self.remote = remote
    
    def deploy(self, branch: str = "main") -> Dict:
        """Deploy site to production."""
        try:
            subprocess.run(["git", "add", "."], cwd=self.site_path, check=True)
            subprocess.run(["git", "commit", "-m", "Deploy"], cwd=self.site_path, check=True)
            subprocess.run(["git", "push", self.remote, branch], cwd=self.site_path, check=True)
            
            return {"status": "deployed", "branch": branch}
        except Exception as e:
            return {"error": str(e)}
    
    def purge_cdn(self, cdn_url: str) -> Dict:
        """Purge CDN cache."""
        return {"action": "purge_cdn", "url": cdn_url, "status": "ready"}
    
    def bust_cache(self, file_pattern: str) -> Dict:
        """Bust cache for file pattern."""
        return {"action": "bust_cache", "pattern": file_pattern, "status": "ready"}


SKILL_NAME = "site_deployer"
SKILL_DESCRIPTION = "Push to GitHub Pages, CDN purge, cache busting"
