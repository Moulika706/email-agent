import json
import os

from dotenv import load_dotenv

from agent.email_classifier import classify_emails
from agent.gmail_reader import fetch_recent_emails, save_last_run_timestamp
from agent.telegram_notifier import notify_important_emails

load_dotenv()

# File to track already processed emails
PROCESSED_FILE = "processed_emails.json"


def load_processed_ids():
    """Load list of already processed email IDs."""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_processed_ids(ids):
    """Save processed email IDs so we don't alert twice."""
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(ids), f)


def run_agent():
    print("\n🤖 Email Agent Starting...")
    print("=" * 50)

    # Step 1 — Fetch recent emails
    print("\n📧 Step 1: Fetching recent emails from Gmail...")
    emails = fetch_recent_emails()
    print(f"  Found {len(emails)} unread emails.")

    if not emails:
        print("  Nothing to process. Exiting.")
        return

    # Step 2 — Filter out already processed emails
    processed_ids = load_processed_ids()
    new_emails = [e for e in emails if e["id"] not in processed_ids]
    print(f"\n🔍 Step 2: {len(new_emails)} new emails to classify.")

    if not new_emails:
        print("  All emails already processed. Exiting.")
        return

    # Step 3 — Classify with Groq AI
    print("\n🧠 Step 3: Classifying emails with Groq AI...")
    important_emails = classify_emails(new_emails)
    print(f"\n  {len(important_emails)} important emails found.")

    # Step 4 — Send Telegram alerts
    print("\n📲 Step 4: Sending Telegram alerts...")
    notify_important_emails(important_emails)

    # Step 5 — Save processed IDs
    new_ids = {e["id"] for e in new_emails}
    processed_ids.update(new_ids)
    save_processed_ids(processed_ids)
    # Save timestamp for next run
    save_last_run_timestamp()
    print("\n✅ Done! Timestamp saved for next run.")
    print("\n✅ Done! Processed IDs saved.")
    print("=" * 50)


if __name__ == "__main__":
    run_agent()
