import os

import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message):
    """Send a message to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",  # Enables bold, italic formatting
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("  📲 Telegram alert sent!")
    else:
        print(f"  ❌ Telegram failed: {response.text}")


def format_alert(classified_email):
    """Format a classified email into a clean Telegram message."""

    # Urgency emoji
    urgency_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
        classified_email.get("urgency", "low"), "🟡"
    )

    # Category emoji
    category_emoji = {
        "internship": "💼",
        "placement": "🎓",
        "interview": "🎯",
        "assessment": "📝",
        "offer": "🎉",
        "rejection": "😔",
        "document": "📄",
        "other": "📧",
    }.get(classified_email.get("category", "other"), "📧")

    message = f"""
{urgency_emoji} *PLACEMENT ALERT* {category_emoji}

*Subject:* {classified_email.get("subject", "N/A")}
*From:* {classified_email.get("sender", "N/A")}
*Category:* {classified_email.get("category", "N/A").upper()}
*Urgency:* {classified_email.get("urgency", "N/A").upper()}

📋 *Summary:*
{classified_email.get("summary", "N/A")}
"""

    # Add deadline if exists
    if classified_email.get("deadline"):
        message += f"\n⏰ *Deadline:* {classified_email['deadline']}"

    # Add action required if exists
    if classified_email.get("action_required"):
        message += f"\n✅ *Action:* {classified_email['action_required']}"

    message += "\n\n_Check your Gmail for full details._"

    return message


def notify_important_emails(classified_emails):
    """Send Telegram alerts for all important emails."""

    if not classified_emails:
        print("No important emails to notify.")
        return

    # Send summary first if multiple emails
    if len(classified_emails) > 1:
        summary = f"🚨 *{len(classified_emails)} Important Emails Found!*\n\nSending details now..."
        send_telegram_message(summary)

    # Send individual alerts
    for email in classified_emails:
        message = format_alert(email)
        send_telegram_message(message)
