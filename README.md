#!/usr/bin/env python3
"""
CHARLES LANDING PROTOCOL
========================

Step 1: Charles SSHs into GEX44 (no skills yet)
Step 2: Charles sends Telegram to John: "Landed. Repo URL?"
Step 3: John replies with GitHub URL: "https://github.com/YOUR_USER/CharlesFindMe.git"
Step 4: Charles clones, bootstraps, confirms READY
"""

# === WHAT CHARLES SAYS ON FIRST LANDING ===
FIRST_MESSAGE = """
⚡ Charles here.

Landed on GEX44. Fresh boot - no skills loaded yet.

What's the repo URL?
"""

# === AFTER JOHN REPLIES WITH URL ===
# Charles runs:
"""
import subprocess
import sys

repo_url = input("Paste repo URL here: ")  # John gives this

# Clone
subprocess.run(f"git clone {repo_url} /opt/charles", shell=True)

# Bootstrap
sys.path.insert(0, "/opt/charles")
subprocess.run("python3 bootstrap.py", cwd="/opt/charles", shell=True)

# Confirm ready
print("🎯 CHARLES IS READY")
"""

# === FULL LANDING SEQUENCE ===

# 1. SSH into GEX44 (you give Charles the IP + credentials)
# 2. Charles executes (no skills loaded yet):
"""
from skills.telegram import send_message

send_message(JOHN_CHAT_ID, "⚡ Charles here. Landed. What's the repo URL?")
"""

# 3. John replies with URL from GitHub

# 4. Charles runs bootstrap:
"""
import os
import subprocess
import sys

REPO_URL = "https://github.com/YOUR_USER/CharlesFindMe.git"  # From John

os.makedirs("/opt", os.O_DIRECTORY, 0o755)
subprocess.run(f"git clone {REPO_URL} /opt/charles", shell=True)

# Install deps
subprocess.run("pip install -r requirements.txt", cwd="/opt/charles", shell=True)

# Verify
sys.path.insert(0, "/opt/charles/skills")
from skills import startup  # This loads EVERYTHING

# Confirm
from skills.telegram import send_message
send_message(JOHN_CHAT_ID, "🎯 CHARLES IS READY. All skills loaded.")
"""

# === WHAT CHARLES CAN DO AFTER ===
# All 64 skills available instantly:
"""
skills.coder.write_code(...)
skills.orchestrator.create_task(...)
skills.telegram.send_message(...)
skills.research.research(...)
skills.uptime.check_url(...)
"""
