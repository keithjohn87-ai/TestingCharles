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
from pathlib import Path

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


# ============================================================
# MESSAGE HANDLER
# ============================================================

async def handle_message(update: Update, context: CallbackContext):
    """Handle incoming messages."""
    user_message = update.message.text
    chat_id = update.effective_chat.id
    
    print(f"📩 Message from {chat_id}: {user_message[:50]}...")
    
    # Quick commands
    if user_message.startswith("/"):
        return  # Let command handlers deal
    
    # Use DeepSeek-R1 for thinking tasks
    # Use Qwen for coding tasks
    # Use Llama for general chat
    
    # For now, use default model
    model = config.DEFAULT_MODEL
    
    # Send "thinking" response
    await update.message.reply_text("🤔 Thinking...")
    
    # Process with skills (placeholder - connect to vLLM)
    response = f"You said: {user_message}\n\n(Skills loaded, ready to execute)"
    
    await update.message.reply_text(response)


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
    
    # Build application
    app = Application.builder() \
        .token(config.TELEGRAM_BOT_TOKEN) \
        .build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("models", models_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Error handler
    app.add_error_handler(error_handler)
    
    # Start polling
    print("📡 Charles is listening...")
    print("=" * 50)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
