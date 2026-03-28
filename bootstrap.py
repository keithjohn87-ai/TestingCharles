#!/usr/bin/env python3
"""
CHARLES BOOTSTRAP
=================

Charles bootstraps HIMSELF on GEX44.

Usage (first time SSH login):
    python bootstrap.py --repo https://github.com/YOUR_USER/CharlesFindMe.git

This script:
1. Clones CharlesFindMe to /opt/charles
2. Installs dependencies
3. Verifies skills load
4. Reports READY
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse


# === CONFIG ===
DEFAULT_REPO = "https://github.com/YOUR_USERNAME/CharlesFindMe.git"  # Change this
INSTALL_PATH = "/opt/charles"
REQUIREMENTS_FILE = "requirements.txt"


def run_cmd(cmd, cwd=None, check=True):
    """Run shell command."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, capture_output=True, text=True
    )
    if check and result.returncode != 0:
        print(f"ERROR: {cmd}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        return None
    return result


def check_git():
    """Check git is available."""
    return run_cmd("git --version", check=False) is not None


def check_python():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"⚠️  Python 3.10+ recommended, got {version.major}.{version.minor}")
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")


def clone_repo(repo_url):
    """Clone CharlesFindMe repo."""
    
    # Check if already exists
    if Path(INSTALL_PATH).exists():
        print(f"⚠️  {INSTALL_PATH} exists, checking for updates...")
        os.chdir(INSTALL_PATH)
        run_cmd("git pull", check=False)
        return True
    
    # Create parent directory
    os.makedirs("/opt", exist_ok=True)
    
    # Clone
    print(f"📦 Cloning {repo_url}...")
    result = run_cmd(f"git clone {repo_url} {INSTALL_PATH}", check=False)
    
    if result and result.returncode == 0:
        print(f"✓ Cloned to {INSTALL_PATH}")
        return True
    else:
        print(f"❌ Clone failed")
        return False


def install_deps():
    """Install Python dependencies."""
    
    req_file = Path(INSTALL_PATH) / REQUIREMENTS_FILE
    
    if not req_file.exists():
        print(f"⚠️  No {REQUIREMENTS_FILE} found, skipping deps install")
        return True
    
    print(f"📦 Installing dependencies...")
    result = run_cmd(f"pip install -r {req_file}", check=False)
    
    if result and result.returncode == 0:
        print(f"✓ Dependencies installed")
        return True
    else:
        print(f"⚠️  Some deps may have failed (continuing anyway)")
        return True


def verify_skills():
    """Verify all skills load correctly."""
    
    print(f"⚡ Verifying skills...")
    
    # Add to path
    sys.path.insert(0, f"{INSTALL_PATH}/skills")
    
    try:
        import skills
        
        # Check core imports
        assert hasattr(skills, 'coder'), "Missing coder"
        assert hasattr(skills, 'orchestrator'), "Missing orchestrator"
        assert hasattr(skills, 'gas'), "Missing AllGasNoBrake"
        assert hasattr(skills, 'water'), "Missing BeWater"
        assert hasattr(skills, 'jarvis'), "Missing JarvisMode"
        
        print(f"✓ All core skills verified")
        
        # Test functionality
        task = skills.orchestrator.create_task("Bootstrap test", "system")
        print(f"✓ Orchestrator functional: {task.id}")
        
        should = skills.gas.should_execute({"clear": True, "flags": []})
        print(f"✓ AllGasNoBrake functional: execute={should['execute']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Skills verification failed: {e}")
        return False


def create_service():
    """Create systemd service to auto-start Charles."""
    
    service_content = """[Unit]
Description=Charles AI Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/charles
ExecStart=/usr/bin/python3 -c "from skills import startup; import time; while True: time.sleep(3600)"
Restart=always

[Install]
WantedBy=multi-user.target
"""
    
    service_path = "/etc/systemd/system/charles.service"
    
    if os.geteuid() == 0:  # If running as root
        with open(service_path, 'w') as f:
            f.write(service_content)
        run_cmd("systemctl daemon-reload")
        run_cmd("systemctl enable charles")
        print(f"✓ Created systemd service: {service_path}")
    else:
        print(f"⚠️  Not root, skipping systemd service creation")
        print(f"   To enable auto-start, run as root:")
        print(f"   cp charles.service /etc/systemd/system/")
        print(f"   systemctl enable charles")


def main():
    """Run bootstrap."""
    
    parser = argparse.ArgumentParser(description="Charles Bootstrap")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="GitHub repo URL")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency install")
    parser.add_argument("--no-service", action="store_true", help="Skip systemd service")
    args = parser.parse_args()
    
    print("=" * 50)
    print("⚡ CHARLES BOOTSTRAP")
    print("=" * 50)
    
    # Pre-checks
    print("\n📋 Pre-checks...")
    check_python()
    if not check_git():
        print("❌ Git not found, install git first")
        return False
    
    # Clone repo
    if not clone_repo(args.repo):
        print("❌ Failed to clone repo")
        return False
    
    # Install deps
    if not args.skip_deps:
        install_deps()
    
    # Verify skills
    if not verify_skills():
        print("❌ Skills verification failed")
        return False
    
    # Create service (optional)
    if not args.no_service:
        create_service()
    
    print("\n" + "=" * 50)
    print("🎯 CHARLES IS READY")
    print("=" * 50)
    print(f"Location: {INSTALL_PATH}")
    print(f"To use: cd {INSTALL_PATH} && python -c 'import skills'")
    print("=" * 50)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
