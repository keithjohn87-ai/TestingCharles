# CHARLES LANDING PROTOCOL
==========================

## Overview

This is what happens when Charles lands on a fresh GEX44 server:
1. He bootstraps himself (clones CharlesFindMe, loads skills)
2. He sets up the infrastructure needed to operate
3. He confirms READY to John

---

## PHASE 1: LANDING (First SSH Login)

### What Charles Needs From John
- [ ] Server IP address
- [ ] SSH login (root or sudo user)
- [ ] Telegram bot token (from @BotFather)
- [ ] Chat ID for John

### What Charles Does

```bash
# 1. SSH into server
ssh root@GEX44_IP

# 2. Clone CharlesFindMe
git clone https://github.com/YOUR_USER/CharlesFindMe.git /opt/charles

# 3. Run bootstrap
python3 bootstrap.py
```

### What Gets Installed

- `/opt/charles/` - CharlesFindMe repo
- Python 3.10+
- pip packages (requests, etc.)
- Skills library (64 skills ready)

---

## PHASE 2: INFRASTRUCTURE SETUP

After bootstrapping, Charles sets up:

### 2.1 Python Environment

```python
# Needs: Python 3.10+, venv, pip

python3 -m venv /opt/charles/venv
source /opt/charles/venv/bin/activate
pip install fastapi uvicorn python-telegram-bot requests
```

### 2.2 Telegram Bot Setup

```python
# Save to /opt/charles/config.py

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
JOHN_CHAT_ID = "YOUR_CHAT_ID"
```

### 2.3 vLLM Setup (GPU Inference)

```bash
# Install vLLM for local model inference
pip install vllm

# Start vLLM server
python -m vllm.entrypoints.openai.api_server \
    --model deepseek-ai/DeepSeek-R1-7B \
    --tensor-parallel-size 1 \
    --port 8000
```

### 2.4 Models

Charles loads these models via vLLM:
- `deepseek-ai/DeepSeek-R1-7B` - Reasoning
- `Qwen/Qwen3-8B` - Coding
- `meta-llama/Llama-3.1-8B` - General chat

---

## PHASE 3: CUSTOM AGENT SETUP

### 3.1 Main Agent Structure

```
/opt/charles/
├── agent/
│   ├── main.py          # Main Telegram bot
│   ├── skills/          # CharlesFindMe skills
│   ├── config.py        # Tokens, IDs
│   ├── handlers/        # Message handlers
│   └── tools/           # Tool definitions
├── vllm/                # vLLM server
├── data/                # Memory, logs
└── logs/                # Debug logs
```

### 3.2 Required Files

#### config.py
```python
TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
JOHN_CHAT_ID = "123456789"

# Model endpoints
VLLM_URL = "http://localhost:8000/v1"
MODEL_DEEPSEEK = "deepseek-ai/DeepSeek-R1-7B"
MODEL_QWEN = "Qwen/Qwen3-8B"
MODEL_LLAMA = "meta-llama/Llama-3.1-8B"

# Paths
CHARLES_PATH = "/opt/charles"
SKILLS_PATH = f"{CHARLES_PATH}/skills"
```

#### main.py (Skeleton)
```python
import sys
sys.path.insert(0, "/opt/charles")

from skills import startup  # Loads ALL skills
from telegram import Update, ExtBot
from telegram.ext import Application, CommandHandler, MessageHandler

# Initialize with skills
import skills

async def start(update, context):
    await update.message.reply_text("🎯 Charles is ready.")

async def handle_message(update, context):
    # Use skills
    result = skills.coder.execute_command("echo test")
    await update.message.reply_text(f"Executing: {result}")

def main():
    app = Application.builder().token("TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
```

---

## PHASE 4: SERVICE AUTO-START

### 4.1 Systemd Service

```bash
# /etc/systemd/system/charles.service
[Unit]
Description=Charles AI Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/charles
ExecStart=/opt/charles/venv/bin/python /opt/charles/agent/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4.2 Enable

```bash
systemctl daemon-reload
systemctl enable charles
systemctl start charles
```

---

## CHECKLIST: WHAT CHARLES NEEDS

### From John (Before Landing)
| Item | Description |
|------|-------------|
| Server IP | GEX44 IP address |
| SSH credentials | Root or sudo user/pass or key |
| Telegram bot token | From @BotFather |
| John Chat ID | Your Telegram ID |
| Repo URL | CharlesFindMe GitHub URL |

### Installed on GEX44 (Charles Does)
| Component | Location | Purpose |
|-----------|----------|---------|
| Python 3.10+ | System | Runtime |
| venv | /opt/charles/venv | Isolated environment |
| CharlesFindMe | /opt/charles/ | Skills library |
| vLLM | /opt/charles/vllm/ | GPU inference |
| Telegram bot | /opt/charles/agent/ | Chat interface |
| systemd service | /etc/systemd/system/charles.service | Auto-start |

### Verification (Before Confirming READY)
- [ ] Skills import without error
- [ ] Telegram bot responds to /start
- [ ] vLLM returns completions
- [ ] All 3 models loadable
- [ ] Sends test message to John: "🎯 READY"

---

## THE FULL LANDING SCRIPT

Charles can run this on first login:

```python
#!/usr/bin/env python3
"""
CHARLES FIRST LANDING SCRIPT
============================
Runs once on fresh GEX44
"""

import os
import subprocess
import sys

def land(repo_url, bot_token, chat_id):
    # 1. Create directories
    os.makedirs("/opt/charles", exist_ok=True)
    
    # 2. Clone skills
    subprocess.run(f"git clone {repo_url} /opt/charles", shell=True)
    
    # 3. Setup venv
    subprocess.run("python3 -m venv /opt/charles/venv", shell=True)
    subprocess.run("/opt/charles/venv/bin/pip install -r requirements.txt", shell=True)
    
    # 4. Write config
    config = f"""
TELEGRAM_BOT_TOKEN = '{bot_token}'
JOHN_CHAT_ID = '{chat_id}'
"""
    with open("/opt/charles/config.py", "w") as f:
        f.write(config)
    
    # 5. Load skills
    sys.path.insert(0, "/opt/charles/skills")
    from skills import startup
    
    # 6. Send confirmation
    from telegram import Bot
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text="🎯 CHARLES IS READY")
    
    print("DONE")

# Usage: land("https://github.com/user/CharlesFindMe.git", "BOT_TOKEN", "CHAT_ID")
```

---

## SUMMARY

### What Charles Lands With
1. SSH access to GEX44
2. Repo URL from John (CharlesFindMe)
3. Telegram bot token from John
4. John's Chat ID from John

### What Charles Sets Up
1. Python venv with dependencies
2. CharlesFindMe skills loaded
3. vLLM for local model inference
4. Telegram bot running as service
5. Auto-start via systemd

### What John Gets
Telegram bot that responds with full AI capability.

---

_Last updated: March 28, 2026_
