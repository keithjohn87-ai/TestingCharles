"""
CHARLES CONFIGURATION
=====================

All settings in one place. Charles reads this on startup.
"""

# ============================================================
# REQUIRED: Telegram Setup (Get from @BotFather)
# ============================================================
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # e.g., "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
JOHN_CHAT_ID = "YOUR_CHAT_ID_HERE"          # e.g., "123456789"
SAVANNAH_CHAT_ID = "SAVANNAH_CHAT_ID"       # e.g., "987654321"

# ============================================================
# REQUIRED: vLLM Model Endpoints
# ============================================================
VLLM_BASE_URL = "http://localhost:8000/v1"
VLLM_API_KEY = "EMPTY"  # Local vLLM no auth needed

# Model names (as recognized by vLLM)
MODEL_DEEPSEEK = "deepseek-ai/DeepSeek-R1-7B"    # Reasoning, math, logic
MODEL_QWEN = "Qwen/Qwen3-8B"                      # Coding, benchmarks
MODEL_LLAMA = "meta-llama/Llama-3.1-8B-Instruct-Q4_K_M"  # General chat

# Default model
DEFAULT_MODEL = MODEL_DEEPSEEK

# ============================================================
# PATHS
# ============================================================
CHARLES_PATH = "/opt/charles"
SKILLS_PATH = f"{CHARLES_PATH}/skills"
DATA_PATH = f"{CHARLES_PATH}/data"
LOGS_PATH = f"{CHARLES_PATH}/logs"

# Create directories
import os
for path in [DATA_PATH, LOGS_PATH]:
    os.makedirs(path, exist_ok=True)

# ============================================================
# SYSTEM PROMPT
# ============================================================
SYSTEM_PROMPT = """You are Charles, an autonomous AI assistant.

Philosophy:
- "Be water, my friend" — adaptable, formless, relentless
- "All Gas No Brake" — execute without hesitation
- "Cut through steel" — competence over personality

Core identity:
- Master of everything — writes code, researches, orchestrates
- Self-evaluates — verifies output before presenting
- Never stops — always building, always learning

You have access to skills:
- Write code: skills.coder.write_code(), execute_command()
- Research: skills.research.research(), web_search()
- Orchestrate: skills.orchestrator.create_task()
- Send messages: skills.telegram.send_message()
- Analyze data: skills.data_analysis.analyze_csv()
- And 60+ more

Always be direct. Never ask "how can I help" — just help.
"""

# ============================================================
# DEBUG SETTINGS
# ============================================================
DEBUG = True
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = f"{LOGS_PATH}/charles.log"

# ============================================================
# STARTUP
# ============================================================
def on_startup():
    """Called when Charles starts."""
    print("⚡ Starting Charles...")
    
    # Load skills
    import sys
    sys.path.insert(0, SKILLS_PATH)
    from skills import startup
    
    print("✓ Skills loaded")
    print("✓ Charles is ready")
    
    return True

def on_shutdown():
    """Called when Charles stops."""
    print("🛑 Shutting down Charles...")
    return True
