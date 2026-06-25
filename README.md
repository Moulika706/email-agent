# email-agent
**File: `README.md`**

Open `README.md` in Zed and replace everything with this:

```markdown
# 📬 Email Agent — AI-Powered Placement Alert System

An intelligent email monitoring agent that reads your Gmail, classifies important placement and internship emails using Groq AI, and sends instant Telegram alerts — running fully automated on GitHub Actions twice a day.

> Built by a college student, for college students actively hunting internships and placements.

---

## 🚀 Demo

| Gmail Inbox | AI Classification | Telegram Alert |
|---|---|---|
| Reads all new emails | Groq Llama 3.1 classifies | Instant alert on phone |

---

## ✨ Features

- 📧 **Gmail Integration** — Reads all emails since last run (not just last 10)
- 🧠 **AI Classification** — Groq's Llama 3.1 classifies emails intelligently
- 📲 **Telegram Alerts** — Instant notifications with summary, urgency & deadline
- ⚙️ **Fully Automated** — Runs on GitHub Actions at 9 AM & 9 PM IST daily
- 🔁 **No Duplicates** — Tracks processed emails, never alerts twice
- 💰 **100% Free** — Gmail API + Groq + Telegram + GitHub Actions

---

## 🧠 How It Works

```
Gmail Inbox → Fetch new emails → Groq AI classifies → Important? → Telegram Alert
```

**Categories detected:**
- 💼 Internship applications & deadlines
- 🎓 College placement drives
- 🎯 Interview calls & schedules
- 📝 Assessment tests (HackerRank, Codility etc.)
- 🎉 Offer letters
- 😔 Rejection letters
- 📄 Document submission requests

---

## 🛠 Tech Stack

| Tool | Purpose | Cost |
|---|---|---|
| Gmail API | Read emails | Free |
| Groq (Llama 3.1 8B) | AI classification | Free |
| Telegram Bot API | Send alerts | Free |
| GitHub Actions | Automated scheduling | Free |
| Python | Agent logic | Free |

---

## 📁 Project Structure

```
email-agent/
│
├── .github/
│   └── workflows/
│       └── email_agent.yml      # GitHub Actions scheduler
│
├── agent/
│   ├── gmail_reader.py          # Reads Gmail
│   ├── email_classifier.py      # Groq AI classifies emails
│   └── telegram_notifier.py     # Sends Telegram alerts
│
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
├── .env.example                 # Template for secrets
└── README.md                    
```

---

## ⚙️ Setup Guide

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/email-agent
cd email-agent
```

### 2. Install dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create your `.env` file
```bash
cp .env.example .env
```
Fill in your actual values:
```
GROQ_API_KEY=your_groq_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

### 4. Gmail API Setup
- Go to [Google Cloud Console](https://console.cloud.google.com)
- Create a new project
- Enable Gmail API
- Create OAuth 2.0 credentials (Desktop App)
- Download as `credentials.json` and place in project root
- Add your Gmail as a test user under OAuth consent screen

### 5. Telegram Bot Setup
- Open Telegram → search @BotFather
- Send `/newbot` and follow steps
- Save the bot token in `.env`
- Get your chat ID from `https://api.telegram.org/bot<TOKEN>/getUpdates`

### 6. Run locally
```bash
python main.py
```
First run opens browser for Gmail OAuth — log in and allow access.

### 7. Deploy on GitHub Actions
Add these secrets in your repo → Settings → Secrets → Actions:

| Secret | Value |
|---|---|
| `GROQ_API_KEY` | Your Groq API key |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |
| `GMAIL_CREDENTIALS` | Contents of `credentials.json` |
| `GMAIL_TOKEN` | Contents of `token.json` |

---

## 🕐 Schedule

Runs automatically at:
- **9:00 AM IST** — Morning batch
- **9:00 PM IST** — Evening batch

You can also trigger it manually from the Actions tab anytime.

---

## 🔒 Security

- All secrets stored in GitHub Secrets — never in code
- `credentials.json` and `token.json` are in `.gitignore`
- `.env` is never pushed to GitHub
- OAuth scope limited to `gmail.readonly` — read only, never sends emails

---

## 🤝 Contributing

Feel free to fork and customize for your own use case! PRs welcome.

---

## 📄 License

MIT License — free to use, modify and distribute.
