#!/usr/bin/env python3
"""
CHARLES MAIN ENTRY POINT
========================

Telegram bot that serves as Charles's interface.
Loads all skills on startup, responds to messages.

Usage:
    python main.py              # Run normally
    python main.py --debug      # Run with debug output
"""

import os
import sys
import argparse
import logging
import smtplib
from pathlib import Path
from email.message import EmailMessage
from agent.memory import get_memory

# Add Charles path
CHARLES_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(CHARLES_PATH))

# Load config
from agent import config

# Load skills ONCE at startup
print("⚡ Loading Charles skills...")
sys.path.insert(0, config.SKILLS_PATH)
import skills
print(f"✓ Skills loaded: {len([x for x in dir(skills) if not x.startswith('_')])} exports")

# Telegram imports
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext


# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG if config.DEBUG else logging.INFO
)
logger = logging.getLogger(__name__)


# ============================================================
# UTILITIES
# ============================================================

async def send_to_john(app: Application, message: str):
    """Send a message to John."""
    try:
        await app.bot.send_message(chat_id=config.JOHN_CHAT_ID, text=message)
        print(f"✅ Sent to John: {message[:50]}...")
    except Exception as e:
        print(f"❌ Failed to send to John: {e}")


async def send_to_savannah(app: Application, message: str):
    """Send a message to Savannah."""
    try:
        await app.bot.send_message(chat_id=config.SAVANNAH_CHAT_ID, text=message)
        print(f"✅ Sent to Savannah: {message[:50]}...")
    except Exception as e:
        print(f"❌ Failed to send to Savannah: {e}")


def send_email(to_address: str, subject: str, body: str) -> bool:
    """Send an email via Gmail SMTP."""
    try:
        msg = EmailMessage()
        msg['From'] = config.GMAIL_ADDRESS
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.set_content(body)
        
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(config.GMAIL_ADDRESS, config.GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        
        print(f"✅ Email sent to {to_address}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


# ============================================================
# COMMAND HANDLERS
# ============================================================

async def start_command(update: Update, context: CallbackContext):
    """Handle /start command."""
    await update.message.reply_text(
        "🎯 Charles is ready.\n\n"
        "What do you need?"
    )


async def help_command(update: Update, context: CallbackContext):
    """Handle /help command."""
    await update.message.reply_text(
        "Available commands:\n\n"
        "/start — Restart Charles\n"
        "/status — Show system status\n"
        "/models — Show loaded models\n"
        "/tasks — Show active tasks\n"
        "/help — Show this help\n\n"
        "Or just tell me what you need."
    )


async def status_command(update: Update, context: CallbackContext):
    """Handle /status command."""
    # Get system status
    status = {
        "autonomy": skills.jarvis.get_autonomy_level(),
        "queue": skills.orchestrator.get_queue_status(),
    }
    
    await update.message.reply_text(
        f"🎯 CHARLES STATUS\n\n"
        f"Autonomy: {status['autonomy']['level']}%\n"
        f"Tasks: {status['queue']['in_progress']} active, "
        f"{status['queue']['pending']} pending"
    )


async def models_command(update: Update, context: CallbackContext):
    """Handle /models command."""
    await update.message.reply_text(
        "🤖 LOADED MODELS\n\n"
        "• DeepSeek-R1 — Reasoning, math, logic\n"
        "• Qwen3-8B — Coding, benchmarks\n"
        "• Llama-3.1 — General chat"
    )


async def search_command(update: Update, context: CallbackContext):
    """Handle /search command - search the web."""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Usage: /search <query>")
        return
    
    await update.message.reply_text(f"🔍 Searching for: {query}...")
    
    try:
        result = skills.knowledge.search_the_web(query)
        response = result.get("response", str(result)[:1000])
    except Exception as e:
        response = f"Search error: {e}"
    
    await update.message.reply_text(response[:4000])  # Telegram limit


async def fetch_command(update: Update, context: CallbackContext):
    """Handle /fetch command - fetch a URL."""
    url = " ".join(context.args)
    if not url:
        await update.message.reply_text("Usage: /fetch <url>")
        return
    
    if not url.startswith("http"):
        url = "https://" + url
    
    await update.message.reply_text(f"📄 Fetching: {url}...")
    
    try:
        result = skills.knowledge.fetch_url(url)
        response = result.get("response", str(result)[:2000])
    except Exception as e:
        response = f"Fetch error: {e}"
    
    await update.message.reply_text(response[:4000])


async def run_command(update: Update, context: CallbackContext):
    """Handle /run command - run a shell command."""
    import subprocess
    cmd = " ".join(context.args)
    if not cmd:
        await update.message.reply_text("Usage: /run <command>")
        return
    
    await update.message.reply_text(f"💻 Running: {cmd}...")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout[:2000] if result.stdout else result.stderr[:2000]
        response = output if output else "(no output)"
    except Exception as e:
        response = f"Error: {e}"
    
    await update.message.reply_text(f"```{response}```", parse_mode="Markdown")


async def readfile_command(update: Update, context: CallbackContext):
    """Handle /read command - read a file."""
    filepath = " ".join(context.args)
    if not filepath:
        await update.message.reply_text("Usage: /read <filepath>")
        return
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()[:3000]
        response = f"📄 {filepath}\n\n{content}"
    except Exception as e:
        response = f"Error reading {filepath}: {e}"
    
    await update.message.reply_text(response)


async def remember_command(update: Update, context: CallbackContext):
    """Handle /remember command - remember a fact."""
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /remember <key> <value>")
        return
    
    key = args[0]
    value = " ".join(args[1:])
    important = "important" in value.lower()
    
    memory = get_memory()
    memory.remember(key, value, important=important)
    await update.message.reply_text(f"🧠 Remembered: {key} = {value}")


async def recall_command(update: Update, context: CallbackContext):
    """Handle /recall command - recall a fact."""
    if not context.args:
        # Show all facts
        memory = get_memory()
        facts = memory.all_facts()
        if not facts:
            await update.message.reply_text("🧠 I don't remember anything yet.")
            return
        
        response = "🧠 Things I remember:\n\n"
        for fact in facts[:20]:
            response += f"• {fact['key']}: {fact['value']}\n"
        await update.message.reply_text(response[:4000])
        return
    
    query = " ".join(context.args)
    memory = get_memory()
    result = memory.recall(query)
    
    if result:
        await update.message.reply_text(f"🧠 {query}: {result}")
    else:
        # Search memory
        results = memory.search_memory(query)
        if results:
            response = f"🧠 Found: {query}\n\n"
            for r in results[:5]:
                response += f"• {r['key']}: {r['value']}\n"
            await update.message.reply_text(response[:4000])
        else:
            await update.message.reply_text(f"🧠 I don't remember: {query}")


async def context_command(update: Update, context: CallbackContext):
    """Handle /context command - show conversation history."""
    memory = get_memory()
    ctx = memory.get_context(limit=10)
    
    if not ctx:
        await update.message.reply_text("No conversation history yet.")
        return
    
    response = "💬 Recent conversation:\n\n"
    for msg in ctx:
        role = "You" if msg["role"] == "user" else "Charles"
        response += f"{role}: {msg['content'][:100]}...\n"
    
    await update.message.reply_text(response[:4000])


# ============================================================
# MESSAGE HANDLER
# ============================================================

async def handle_message(update: Update, context: CallbackContext):
    """Handle incoming messages."""
    user_message = update.message.text
    chat_id = update.effective_chat.id
    
    # Only allow John (no Savannah - that's a separate bot)
    if str(chat_id) != config.JOHN_CHAT_ID:
        print(f"🚫 Blocked unauthorized: {chat_id}")
        return
    
    print(f"📩 Message from {chat_id}: {user_message[:50]}...")
    
    # Quick commands
    if user_message.startswith("/"):
        return  # Let command handlers deal
    
    # Try to use skills to process the message
    try:
        # Record user's message in memory
        memory = get_memory()
        memory.add_message("user", user_message)
        
        # Use web search skill for research queries
        if any(word in user_message.lower() for word in ["search", "find", "look up", "what is", "who is"]):
            await update.message.reply_text("🔍 Searching...")
            response = f"I'll search for: {user_message}\n\n(Chrome needs to be running with --remote-debugging-port=9222)"
        else:
            # General conversation - check memory first
            recall = memory.recall(user_message.lower().strip('?'))
            if recall:
                response = f"💭 {recall}"
            else:
                response = f"Charles received: {user_message}\n\nUse /search <query> to search the web, /run <command> to run commands, /remember <key> <value> to remember things."
        
        # Record Charles's response in memory
        memory.add_message("charles", response)
    except Exception as e:
        response = f"Error processing: {e}"
    
    await update.message.reply_text(response)


async def skills_command(update: Update, context: CallbackContext):
    """Handle /skills command - list all skills."""
    response = "🎯 CHARLES SKILLS (80+)\n\n"
    
    # Core skills (7)
    response += "🧠 CORE (7):\n"
    response += "• MasterCoder — Write, debug, execute code\n"
    response += "• MasterResearcher — Search, fetch, synthesize\n"
    response += "• MasterOrchestrator — Task management\n"
    response += "• UniversalKnowledge — Web search, PDF, images\n"
    response += "• AllGasNoBrake — Execute now, retry with fix\n"
    response += "• JarvisMode — System control\n"
    response += "• BeWater — Adapt to any situation\n\n"
    
    # Gap skills (20+)
    response += "📊 GAP SKILLS (20+):\n"
    response += "• LearningEngine, SelfImprovingAgent\n"
    response += "• MultiHopReasoning, HypothesisGenerator, CounterArgument, DecisionMatrix\n"
    response += "• StrategicPlanner, CompetitiveIntelligence, PerformanceOptimizer, DevOpsAutomation\n"
    response += "• SimulationRunner, ContentEngine, NegotiationStrategist\n"
    response += "• TavilySearch, BrowserAutomation\n"
    response += "• GoalPlanner, AutonomousExecution, N8NWorkflowAutomation\n"
    response += "• CommunicationAdvisor, MeetingIntelligence\n\n"
    
    # Universal skills (30+)
    response += "🌐 UNIVERSAL SKILLS (30+):\n"
    response += "• DeepResearch, DataAnalysis, CodeReview\n"
    response += "• Debugging, VersionControl, CloudMonitoring\n"
    response += "• KubernetesDeployment, CICDPipeline\n"
    response += "• DataCleaning, DataVisualization\n"
    response += "• FinancialModeling, ReportGeneration\n"
    response += "• OAuthSetup, WebhookSetup, InfrastructureAsCode\n"
    response += "• LeadScoring, PrivacyPolicyDrafting\n\n"
    
    # Commands
    response += "💬 COMMANDS:\n"
    response += "/search <query> — Web search\n"
    response += "/fetch <url> — Fetch URL\n"
    response += "/run <cmd> — Run command\n"
    response += "/read <file> — Read file\n"
    response += "/write <file> <content> — Write file\n"
    response += "/browse <url> — Open Chrome\n"
    response += "/remember <key> <val> — Remember fact\n"
    response += "/recall <key> — Recall fact\n"
    response += "/skills — Show this\n"
    response += "/context — Conversation history\n"
    
    await update.message.reply_text(response)


async def writefile_command(update: Update, context: CallbackContext):
    """Handle /write command - write a file."""
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /write <filepath> <content>")
        return
    
    filepath = args[0]
    content = " ".join(args[1:])
    
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        response = f"✅ Wrote to {filepath}\n\n{content[:500]}"
    except Exception as e:
        response = f"Error writing {filepath}: {e}"
    
    await update.message.reply_text(response)


# ============================================================
# BROWSER INTEGRATION
# ============================================================

async def browse_command(update: Update, context: CallbackContext):
    """Handle /browse command - browse a URL with Chrome."""
    url = " ".join(context.args)
    if not url:
        await update.message.reply_text("Usage: /browse <url>")
        return
    
    if not url.startswith("http"):
        url = "https://" + url
    
    await update.message.reply_text(f"🌐 Opening Chrome: {url}...")
    
    try:
        # Try to use Playwright to connect to Chrome
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.new_page()
            page.goto(url, timeout=30000)
            content = page.content()[:3000]
            page.close()
            browser.close()
        
        response = f"🌐 {url}\n\n{content[:3000]}"
    except Exception as e:
        response = f"Chrome error: {e}\n\nMake sure Chrome is running with:\nchrome --remote-debugging-port=9222"
    
    await update.message.reply_text(response[:4000])


# ============================================================
# ERROR HANDLER
# ============================================================

async def error_handler(update: Update, context: CallbackContext):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    await update.message.reply_text(
        "⚠️ An error occurred. Check logs."
    )


# ============================================================
# MAIN
# ============================================================

def main():
    """Start the Charles bot."""
    
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    if args.debug:
        config.DEBUG = True
    
    print("=" * 50)
    print("🎯 CHARLES STARTING")
    print("=" * 50)
    
    # Initialize memory
    memory = get_memory()
    
    # Build application
    app = Application.builder() \
        .token(config.TELEGRAM_BOT_TOKEN) \
        .build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("models", models_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("fetch", fetch_command))
    app.add_handler(CommandHandler("run", run_command))
    app.add_handler(CommandHandler("read", readfile_command))
    app.add_handler(CommandHandler("write", writefile_command))
    app.add_handler(CommandHandler("remember", remember_command))
    app.add_handler(CommandHandler("recall", recall_command))
    app.add_handler(CommandHandler("context", context_command))
    app.add_handler(CommandHandler("skills", skills_command))
    app.add_handler(CommandHandler("browse", browse_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Error handler
    app.add_error_handler(error_handler)
    
    # Start polling
    print("📡 Charles is listening...")
    print("=" * 50)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
