import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def classify_email(email):
    """Use Groq AI to classify if email is important for placements/internships."""

    prompt = f"""
You are an email classifier for a college student actively looking for internships and placements.

Analyze this email and respond ONLY in this exact JSON format, nothing else:
{{
    "is_important": true or false,
    "category": "one of: internship | placement | interview | assessment | offer | rejection | document | other",
    "urgency": "one of: high | medium | low",
    "summary": "one line summary of the email",
    "deadline": "deadline date if mentioned, else null",
    "action_required": "what the student needs to do, else null"
}}

Email Details:
From: {email["sender"]}
Subject: {email["subject"]}
Date: {email["date"]}
Body: {email["body"]}

Rules:
- Mark is_important as true if email is about: job/internship applications, placement drives, interview calls, assessment tests, offer letters, rejection letters, document submissions, PPT announcements
- Mark is_important as false for: promotions, newsletters, OTPs, social media, spam
- Be strict — only mark important if it genuinely needs student attention
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,  # Low temperature = consistent, focused responses
    )

    raw = response.choices[0].message.content.strip()

    # Parse JSON response
    import json

    try:
        # Clean up response if needed
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()

        result = json.loads(raw)
        result["email_id"] = email["id"]
        result["subject"] = email["subject"]
        result["sender"] = email["sender"]
        result["date"] = email["date"]
        return result

    except json.JSONDecodeError:
        print(f"Could not parse AI response for: {email['subject']}")
        return None


def classify_emails(emails):
    """Classify a list of emails, return only important ones."""
    important = []

    for email in emails:
        print(f"Classifying: {email['subject'][:50]}...")
        result = classify_email(email)

        if result and result.get("is_important"):
            important.append(result)
            print(
                f"  ✅ Important — {result['category']} | {result['urgency']} urgency"
            )
        else:
            print(f"  ⏭ Skipped — not important")

    return important
