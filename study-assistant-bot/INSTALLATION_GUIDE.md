# Installation Guide 🚀

Complete step-by-step guide to install and run the Study Assistant Bot.

## Quick Start (5 minutes)

### Step 1: Get Your API Keys

1. **Telegram Bot Token**
   - Open Telegram and search for @BotFather
   - Send `/start` then `/newbot`
   - Follow instructions to create your bot
   - Copy the API token

2. **OpenAI API Key**
   - Go to https://platform.openai.com/
   - Sign up or log in
   - Navigate to API keys section
   - Create a new API key

3. **(Optional) Google Gemini API Key**
   - Go to https://ai.google.dev/
   - Sign up
   - Get your API key from Google AI Studio

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/study-assistant-bot.git
cd study-assistant-bot
```

### Step 3: Install Python (if needed)

**Windows/Mac:**
- Download from https://www.python.org/
- Run installer and select "Add Python to PATH"
- Verify: `python --version` (should be 3.12+)

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv
```

### Step 4: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 7: Initialize Database

```bash
python -c "from database import init_db; init_db()"
```

### Step 8: Run the Bot

```bash
python bot.py
```

You should see: `INFO: Bot started successfully!`

## Detailed Installation

### Option 1: Local Python (Recommended for Development)

**Prerequisites:**
- Python 3.12 or higher
- pip package manager
- Git

**Installation Steps:**

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/study-assistant-bot.git
   cd study-assistant-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Upgrade pip**
   ```bash
   pip install --upgrade pip
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create .env file**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your API keys
   ```

6. **Initialize database**
   ```bash
   python -c "from database import init_db; init_db()"
   ```

7. **Run bot**
   ```bash
   python bot.py
   ```

### Option 2: Docker (Recommended for Production)

**Prerequisites:**
- Docker installed ([Get Docker](https://www.docker.com/products/docker-desktop))
- docker-compose

**Installation Steps:**

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/study-assistant-bot.git
   cd study-assistant-bot
   ```

2. **Create .env file**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Build and run**
   ```bash
   docker-compose up --build
   ```

4. **Access logs**
   ```bash
   docker-compose logs -f study-bot
   ```

**Stopping the bot:**
```bash
docker-compose down
```

### Option 3: Docker with PostgreSQL (Production)

**Prerequisites:**
- Docker and docker-compose

**Steps:**

1. **Edit .env**
   ```env
   DATABASE_URL=postgresql://admin:password@postgres:5432/study_assistant
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=password
   ```

2. **Run with PostgreSQL**
   ```bash
   docker-compose --profile production up --build
   ```

### Option 4: Virtual Machine/Server Deployment

**On Linux Server (Ubuntu 22.04):**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3.12 python3.12-venv python3-pip git

# Clone repository
git clone https://github.com/yourusername/study-assistant-bot.git
cd study-assistant-bot

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your API keys

# Initialize database
python -c "from database import init_db; init_db()"

# Install and start with systemd
sudo tee /etc/systemd/system/study-bot.service << EOF
[Unit]
Description=Study Assistant Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl start study-bot
sudo systemctl enable study-bot

# Check status
sudo systemctl status study-bot
```

## Configuration

### Environment Variables

Create `.env` file with the following:

```env
# Required
TELEGRAM_BOT_TOKEN=your_bot_token

# AI Configuration
AI_PROVIDER=openai  # or 'gemini'
OPENAI_API_KEY=your_key
GOOGLE_API_KEY=your_key

# Database (optional)
DATABASE_URL=sqlite:///study_assistant.db
# For PostgreSQL: postgresql://user:password@host/database

# Optional Settings
LOG_LEVEL=INFO
ENABLE_RAG=true
ENABLE_REMINDERS=true
MAX_UPLOAD_SIZE_MB=20
TIMEZONE=UTC
DEBUG=false
ENVIRONMENT=development
```

### Database Configuration

**SQLite (Default - Development):**
- No additional setup needed
- Database file: `study_assistant.db`
- Good for: Testing, development, small deployments

**PostgreSQL (Production):**

1. **Install PostgreSQL**
   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

2. **Create database**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE study_assistant;
   CREATE USER study_user WITH PASSWORD 'strong_password';
   GRANT ALL PRIVILEGES ON DATABASE study_assistant TO study_user;
   \q
   ```

3. **Configure .env**
   ```env
   DATABASE_URL=postgresql://study_user:strong_password@localhost/study_assistant
   ```

## Verification

### Test Installation

1. **Start bot**
   ```bash
   python bot.py
   ```

2. **Look for success message**
   ```
   INFO: Bot started successfully!
   INFO: Using polling mode
   ```

3. **Open Telegram and start your bot**
   - Search for your bot name
   - Send `/start`
   - You should see the welcome message

### Troubleshooting

**"Bot token not valid"**
- Verify TELEGRAM_BOT_TOKEN in .env
- Ensure no extra spaces in .env
- Get a new token from @BotFather

**"API key error"**
- Check OPENAI_API_KEY or GOOGLE_API_KEY
- Verify API key is valid and has quota
- Check API key has necessary permissions

**"Database error"**
- For SQLite: Check file permissions
- For PostgreSQL: Verify connection string
- Initialize database: `python -c "from database import init_db; init_db()"`

**"ModuleNotFoundError"**
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

**"Port already in use"**
- Change WEBHOOK_PORT in .env if using webhook
- Or use polling mode

## Running the Bot

### Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run bot
python bot.py
```

### Production Mode

**Option 1: Background process**
```bash
nohup python bot.py > bot.log 2>&1 &
```

**Option 2: systemd service** (see server deployment above)

**Option 3: Docker**
```bash
docker-compose up -d
```

**Option 4: Cloud deployment**
- Railway: Connect GitHub, deploy automatically
- Render: Similar to Railway
- Heroku: Using Procfile (create one)
- Google Cloud: Using Cloud Run
- AWS: Using Lambda (serverless)

## Stopping the Bot

**Local/Development:**
```bash
# Press Ctrl+C in terminal
```

**Background process:**
```bash
pkill -f "python bot.py"
```

**systemd service:**
```bash
sudo systemctl stop study-bot
```

**Docker:**
```bash
docker-compose down
```

## Updating the Bot

```bash
# Pull latest changes
git pull origin main

# Activate environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Initialize any new database changes
python -c "from database import init_db; init_db()"

# Restart bot
python bot.py
```

## Next Steps

1. **Customize the bot**
   - Modify keyboards in `keyboards/main_menu.py`
   - Add new features in `handlers/`
   - Create services in `services/`

2. **Set up reminders**
   - Configure APScheduler for study reminders
   - Set reminder timezone

3. **Deploy to production**
   - Choose hosting platform
   - Configure domain (if using webhook)
   - Set up monitoring and logs

4. **Invite users**
   - Share bot link: `https://t.me/your_bot_name`
   - Start collecting feedback

## Support

- Check [README.md](README.md) for features overview
- Read [DEVELOPMENT.md](DEVELOPMENT.md) for development guide
- Review logs in `logs/` directory
- Open GitHub issue for bugs

## Security Notes

⚠️ **Important:**
- Never commit `.env` file
- Use strong API keys
- Rotate API keys regularly
- Use environment variables only
- Keep dependencies updated
- Monitor logs for suspicious activity

---

**Ready to go!** 🎓 Your Study Assistant Bot is now running!
