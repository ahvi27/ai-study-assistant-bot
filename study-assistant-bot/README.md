# 🎓 Study Assistant Telegram Bot

An AI-powered Telegram bot that serves as your personal study companion, helping you learn, retain information, and track your academic progress.

## Features ✨

### Core Features
- **💬 AI Chat** - Intelligent conversations with AI tutors
- **📚 Document Upload** - Upload PDF, DOCX, and TXT files
- **❓ Smart Q&A** - Ask questions and get answers based on your notes
- **🧪 Quiz Generation** - Generate MCQ, True/False, Short Answer quizzes
- **🎴 Flashcards** - Create and review flashcards with spaced repetition
- **📝 Smart Summaries** - Generate short, medium, and detailed summaries
- **🌐 Multi-language Translation** - Translate content to 10+ languages
- **📅 Study Planner** - AI-generated personalized study plans
- **⏰ Study Reminders** - Set daily, weekly, or custom reminders
- **📊 Progress Tracking** - Track study statistics and streaks

### Supported Languages
- English, French, Spanish, Arabic, Amharic, German, Italian, Portuguese, Japanese, Chinese

## Tech Stack 🛠️

- **Language**: Python 3.12+
- **Telegram**: python-telegram-bot (21.7+)
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL
- **AI**: OpenAI API & Google Gemini API
- **Document Processing**: PyMuPDF, pdfplumber, python-docx
- **Deployment**: Docker, Docker Compose, Railway, Render

## Installation 🚀

### Prerequisites
- Python 3.12+
- Telegram Bot API Token (from @BotFather)
- OpenAI or Google Gemini API Key

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/study-assistant-bot.git
cd study-assistant-bot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your credentials
```

5. **Run the bot**
```bash
python bot.py
```

### Docker Setup

1. **Build and run with Docker Compose**
```bash
cp .env.example .env
# Edit .env with your credentials
docker-compose up --build
```

2. **Using just Docker**
```bash
docker build -t study-assistant-bot .
docker run -e TELEGRAM_BOT_TOKEN=your_token \
           -e OPENAI_API_KEY=your_key \
           study-assistant-bot
```

## Configuration 📋

### Environment Variables

```env
# Required
TELEGRAM_BOT_TOKEN=your_bot_token

# AI Provider (openai or gemini)
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_gemini_key

# Database
DATABASE_URL=sqlite:///study_assistant.db
# For PostgreSQL: postgresql://user:password@localhost/study_assistant

# Optional
LOG_LEVEL=INFO
ENABLE_RAG=true
ENABLE_REMINDERS=true
MAX_UPLOAD_SIZE_MB=20
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TIMEZONE=UTC
```

## Commands 📝

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and show main menu |
| `/help` | Show help message with all commands |
| `/upload` | Upload study documents |
| `/ask` | Ask questions about your notes |
| `/quiz` | Generate quizzes |
| `/flashcards` | Create and study flashcards |
| `/summary` | Generate summaries |
| `/translate` | Translate content |
| `/plan` | Create study plan |
| `/progress` | View your progress |
| `/stats` | View detailed statistics |

## Project Structure 📁

```
study-assistant-bot/
├── bot.py                 # Main entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
│
├── database/
│   ├── db.py              # Database operations
│   ├── models.py          # SQLAlchemy models
│   └── migrations.py      # Database migrations
│
├── handlers/              # Telegram command handlers
│   ├── start.py           # /start and /help commands
│   ├── upload.py          # Document upload
│   ├── ask.py             # Ask questions
│   ├── quiz.py            # Quiz generation
│   ├── flashcards.py      # Flashcard management
│   ├── progress.py        # Progress tracking
│   └── callbacks.py       # Button callbacks
│
├── services/              # Business logic
│   ├── ai_service.py      # AI integration (OpenAI/Gemini)
│   ├── pdf_service.py     # PDF processing
│   ├── docx_service.py    # DOCX processing
│   ├── quiz_service.py    # Quiz generation
│   ├── flashcard_service.py # Flashcard generation
│   ├── summary_service.py  # Summarization
│   ├── translation_service.py # Translation
│   └── planner_service.py # Study planning
│
├── keyboards/             # Telegram keyboards
│   └── main_menu.py       # Button layouts
│
├── utils/                 # Utility functions
│   ├── logger.py          # Logging setup
│   ├── validators.py      # Input validation
│   └── helpers.py         # Helper functions
│
├── storage/               # File storage
│   ├── uploads/           # Uploaded documents
│   └── generated/         # Generated files
│
└── tests/                 # Unit tests
```

## Usage Examples 💡

### 1. Upload and Analyze Documents
```
User: /upload
Bot: Shows upload prompt
User: Sends a PDF file
Bot: Extracts text and offers analysis options
```

### 2. Ask Questions
```
User: /ask
User: What is machine learning?
Bot: Searches uploaded notes and provides answer
```

### 3. Generate Quiz
```
User: /quiz
Bot: Shows quiz type options (MCQ, True/False, etc.)
User: Selects type and difficulty
Bot: Generates quiz with questions
```

### 4. Create Flashcards
```
User: /flashcards
Bot: Generates flashcards from uploaded documents
User: Reviews and studies flashcards
```

## Database Schema 🗄️

### Tables
- **users** - User accounts and preferences
- **documents** - Uploaded study materials
- **document_chunks** - Text chunks for RAG
- **questions** - User Q&A history
- **quizzes** - Quiz attempts and scores
- **flashcards** - Flashcard collection
- **reminders** - User reminders
- **study_plans** - Generated study plans
- **progress** - User progress statistics

## Deployment 🌐

### Railway
1. Push code to GitHub
2. Connect GitHub repo to Railway
3. Add environment variables in Railway dashboard
4. Deploy

### Render
1. Create new service from GitHub
2. Set environment variables
3. Deploy

### Custom Server
```bash
# Install PM2
npm install -pm2 -g

# Create PM2 config
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'study-bot',
    script: './bot.py',
    interpreter: 'python3',
    autorestart: true
  }]
}
EOF

# Start bot
pm2 start ecosystem.config.js
```

## API Integrations 🔌

### OpenAI
- Supports GPT-4 Turbo and other models
- Used for: Q&A, summaries, quiz generation, flashcards

### Google Gemini
- Alternative to OpenAI
- Used for: Q&A, summaries, quiz generation

### Telegram Bot API
- Long polling or webhook support
- File handling for documents

## Error Handling 🛡️

The bot includes comprehensive error handling:
- File upload validation (size, type)
- API rate limiting handling
- Database connection failures
- Network timeouts
- User input validation

## Logging 📊

Logs are saved to `logs/` directory:
- `bot.log` - General application logs
- `errors.log` - Error logs only

## Performance Optimizations ⚡

- Connection pooling for database
- Caching for frequently accessed data
- Batch processing for large uploads
- Efficient text chunking for RAG
- Asynchronous operations throughout

## Security Considerations 🔒

- API keys in environment variables only
- SQL injection prevention via SQLAlchemy ORM
- File type validation
- Upload size limits
- User input sanitization
- Database connection security

## Testing 🧪

Run unit tests:
```bash
python -m pytest tests/
```

Test coverage includes:
- AI service integration
- PDF/DOCX extraction
- Quiz generation
- Database operations
- Input validation

## Contributing 🤝

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Roadmap 🗺️

- [ ] Voice message support
- [ ] Study group collaboration
- [ ] Mobile app
- [ ] Advanced analytics dashboard
- [ ] Integration with Notion/OneNote
- [ ] Video content analysis
- [ ] Peer tutoring matching
- [ ] Gamification features

## Troubleshooting 🔧

### Bot not responding
- Check TELEGRAM_BOT_TOKEN is correct
- Verify bot has necessary permissions
- Check internet connection
- View logs for errors

### Document upload fails
- Check file size (max 20MB)
- Verify file format (PDF, DOCX, TXT)
- Check available disk space

### AI responses are slow
- Check API rate limits
- Verify API keys are valid
- Check network connection
- Monitor API usage

## License 📄

MIT License - see LICENSE file for details

## Support 💬

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Email: support@example.com

## Acknowledgments 🙏

- python-telegram-bot library
- OpenAI and Google for AI models
- PyMuPDF and pdfplumber for document processing
- SQLAlchemy ORM

---

**Happy Learning!** 🎓
