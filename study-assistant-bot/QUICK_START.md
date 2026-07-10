# Quick Start Guide - 5 Minutes to Working Bot

## Prerequisites
- Python 3.11+
- OpenAI API Key (from https://platform.openai.com/api-keys)
- Bot token (already in .env file)

## Step 1: Get OpenAI API Key (2 minutes)

1. Visit https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (you won't see it again!)
4. Keep it safe

## Step 2: Setup Local Environment (2 minutes)

**On Mac/Linux:**
```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

**On Windows:**
```bash
# Double-click setup.bat or run:
setup.bat
```

**Manual (all platforms):**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate          # Mac/Linux
# or
venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p data/uploads data/vectors logs
```

## Step 3: Configure API Key (1 minute)

1. Open `.env` file in any text editor
2. Find this line:
   ```
   OPENAI_API_KEY=sk-YOUR_OPENAI_API_KEY_HERE
   ```
3. Replace with your actual key:
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
4. Save file

## Step 4: Run Bot (30 seconds)

Make sure virtual environment is activated, then:

```bash
python bot.py
```

You should see:
```
====================================================
🤖 Study Assistant Telegram Bot Starting...
====================================================
📦 Initializing database...
✅ Database initialized successfully
...
🚀 Starting bot with polling (interval: 1s)...
```

## Step 5: Test in Telegram (30 seconds)

1. Open Telegram
2. Search for your bot
3. Send `/start`
4. See the welcome menu!

## What Now?

### Chat with Your Bot
Just type any message:
```
You: What is calculus?
Bot: Calculus is a branch of mathematics...
```

### Try Commands
- `/start` - Show main menu
- `/help` - Show all commands
- Type normally to chat with AI

### Check Logs
```bash
# Watch logs in real-time
tail -f logs/bot.log          # Mac/Linux
Get-Content -Wait logs\bot.log -Tail 20  # Windows PowerShell
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'telegram'"
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

### "OpenAI API key not valid"
- Check key starts with `sk-`
- Verify you copied the full key
- Make sure it's in .env correctly

### "Bot token not working"
- Token is already in .env
- Check you're logged into correct Telegram account

### "sqlite3.OperationalError: database is locked"
- Close all bot instances
- Delete `study_bot.db`
- Restart bot

### "Permission denied: setup.sh"
- Run: `chmod +x setup.sh`
- Then: `./setup.sh`

## Next: Implement Features

Ready to add more? See:
- `GETTING_STARTED.md` - Feature implementation
- `README.md` - Full documentation
- `handlers/` - Where to add new features

## Stop the Bot

Press `Ctrl + C` in terminal

## File Locations

- Logs: `logs/bot.log`
- Database: `study_bot.db`
- Uploads: `data/uploads/`
- Vectors: `data/vectors/`

## Architecture

```
Your Input (Telegram)
    ↓
bot.py (handler routing)
    ↓
handlers/ (process command)
    ↓
services/ (business logic)
    ├─ AI: OpenAI API
    ├─ RAG: Vector search
    ├─ Documents: PDF/DOCX parsing
    └─ Storage: Local or S3
    ↓
database/ (SQLAlchemy ORM)
    ↓
SQLite (local)
    ↓
Your Response (Telegram)
```

## Virtual Environment Tips

**Activate (every time you use the bot):**
```bash
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

**Deactivate:**
```bash
deactivate
```

**Reinstall packages:**
```bash
pip install -r requirements.txt --force-reinstall
```

## Production Deployment

Ready to deploy? See:
- Railway (recommended): 5 minutes
- Render: 10 minutes
- Docker: `docker-compose up -d`
- Custom VPS: See README.md

---

**Congratulations! Your bot is live.** 🎉

Start with `/start` command and explore all the features. Happy studying!
