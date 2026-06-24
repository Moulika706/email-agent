import base64
import json
import os
from datetime import datetime, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    """Authenticate and return Gmail service."""
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save as JSON this time
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_last_run_timestamp():
    """Get timestamp of last run. If none, default to 12 hours ago."""
    if os.path.exists("last_run.txt"):
        with open("last_run.txt", "r") as f:
            return int(f.read().strip())

    twelve_hours_ago = int(datetime.now(timezone.utc).timestamp()) - (12 * 60 * 60)
    return twelve_hours_ago


def save_last_run_timestamp():
    """Save current timestamp as last run."""
    with open("last_run.txt", "w") as f:
        f.write(str(int(datetime.now(timezone.utc).timestamp())))


def fetch_recent_emails():
    """Fetch all emails received since last run."""
    service = get_gmail_service()

    since_timestamp = get_last_run_timestamp()
    since_readable = datetime.fromtimestamp(since_timestamp).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    print(f"  Fetching emails since: {since_readable}")

    query = f"after:{since_timestamp}"

    all_messages = []
    page_token = None

    while True:
        result = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=100, pageToken=page_token)
            .execute()
        )

        messages = result.get("messages", [])
        all_messages.extend(messages)

        page_token = result.get("nextPageToken")
        if not page_token:
            break

    if not all_messages:
        print("  No new emails found.")
        return []

    print(f"  Found {len(all_messages)} emails in this batch.")

    emails = []
    for msg in all_messages:
        msg_data = (
            service.users()
            .messages()
            .get(userId="me", id=msg["id"], format="full")
            .execute()
        )

        headers = msg_data["payload"]["headers"]
        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"), "No Subject"
        )
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
        date = next((h["value"] for h in headers if h["name"] == "Date"), "Unknown")
        body = extract_body(msg_data["payload"])

        emails.append(
            {
                "id": msg["id"],
                "subject": subject,
                "sender": sender,
                "date": date,
                "body": body[:2000],
            }
        )

    return emails


def extract_body(payload):
    """Extract plain text body from email payload."""
    body = ""

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data", "")
                if data:
                    body = base64.urlsafe_b64decode(data).decode(
                        "utf-8", errors="ignore"
                    )
                    break
    else:
        data = payload["body"].get("data", "")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return body
