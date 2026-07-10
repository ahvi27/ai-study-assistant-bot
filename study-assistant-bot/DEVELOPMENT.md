# Development Guide 🔧

## Getting Started

### Prerequisites
- Python 3.12 or higher
- pip or conda
- Git
- Telegram Bot Token (from @BotFather)
- OpenAI or Google Gemini API Key

### Setup Development Environment

1. **Clone the repository**
```bash
git clone <repository-url>
cd study-assistant-bot
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Initialize database**
```bash
python -c "from database import init_db; init_db()"
```

## Architecture Overview

### Project Structure

```
study-assistant-bot/
├── bot.py                  # Main application entry
├── config.py               # Configuration management
├── database/               # Database layer
├── handlers/               # Telegram command handlers
├── services/               # Business logic services
├── keyboards/              # UI keyboards
├── utils/                  # Utility functions
├── tests/                  # Unit tests
└── storage/                # File storage
```

### Data Flow

```
User Input (Telegram)
    ↓
Handler (handlers/*.py)
    ↓
Service (services/*.py)
    ↓
Database (database/*.py)
    ↓
Response → Telegram
```

## Code Organization

### Adding a New Feature

1. **Create a new handler** (`handlers/feature_name.py`)
   ```python
   from telegram import Update
   from telegram.ext import ContextTypes, CommandHandler

   async def feature_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
       # Implementation here
       pass

   def get_feature_handlers():
       return [CommandHandler("feature", feature_command)]
   ```

2. **Add service if needed** (`services/feature_service.py`)
   ```python
   class FeatureService:
       def do_something(self):
           # Business logic here
           pass
   ```

3. **Register handler in bot.py**
   ```python
   from handlers.feature import get_feature_handlers
   
   application.add_handlers(get_feature_handlers())
   ```

### Database Operations

**Adding a new model:**
1. Define model in `database/models.py`
2. Create database operations in `database/db.py`
3. Run migrations or recreate tables

**Example:**
```python
# In models.py
class MyModel(Base):
    __tablename__ = "my_models"
    id = Column(Integer, primary_key=True)
    # Add columns

# In db.py
class MyModelDB:
    @staticmethod
    def add_model(session, **kwargs):
        obj = MyModel(**kwargs)
        return Database.add(session, obj)
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_validators.py

# Run with coverage
python -m pytest --cov=. tests/

# Run specific test class
python -m pytest tests/test_validators.py::TestFileValidators
```

### Writing Tests

```python
import unittest

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_something(self):
        """Test description"""
        self.assertEqual(actual, expected)

    def tearDown(self):
        """Clean up"""
        pass
```

## Debugging

### Enable Debug Logging

Set in `.env`:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

### View Logs

```bash
# View all logs
tail -f logs/bot.log

# View only errors
tail -f logs/errors.log

# Clear logs
rm logs/*.log
```

### Common Issues

**Issue: Bot not responding**
- Check TELEGRAM_BOT_TOKEN in .env
- Verify bot has correct permissions
- Check logs for errors

**Issue: Database errors**
- Verify DATABASE_URL in .env
- Check database file exists (if SQLite)
- Try recreating database: `python -c "from database import init_db; init_db()"`

**Issue: API errors**
- Verify API keys in .env
- Check API rate limits
- Review API documentation

## Code Quality

### Code Style

Follow PEP8:
```bash
pip install flake8
flake8 .
```

### Type Hints

Use type hints throughout:
```python
def function(param: str) -> str:
    return param.upper()
```

### Documentation

Add docstrings to all functions:
```python
def my_function(param: str) -> str:
    """
    Short description.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
    """
    pass
```

## Performance Optimization

### Database Queries
- Use indexes for frequently queried columns
- Limit query results with `.limit()`
- Use efficient queries

### Caching
- Cache AI responses
- Cache document content
- Use context user_data for session data

### Async Operations
- All operations are async by default
- Use asyncio for concurrent operations
- Avoid blocking operations

## Deployment

### Local Development
```bash
python bot.py
```

### Docker
```bash
docker build -t study-assistant-bot .
docker run -e TELEGRAM_BOT_TOKEN=your_token study-assistant-bot
```

### Production Checklist
- [ ] All environment variables set
- [ ] Database configured correctly
- [ ] API keys valid
- [ ] Logs configured
- [ ] Error handling in place
- [ ] Tests passing
- [ ] Documentation updated

## Contributing Guidelines

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make changes and test**
   ```bash
   python -m pytest
   ```

3. **Commit changes**
   ```bash
   git commit -m "Add: description of changes"
   ```

4. **Push to branch**
   ```bash
   git push origin feature/your-feature
   ```

5. **Create Pull Request**
   - Describe changes
   - Reference related issues
   - Request review

## Commit Message Format

```
Type: Brief description

Optional detailed explanation

Closes #123
```

Types: Add, Fix, Update, Remove, Refactor, Docs, Test

## Database Migrations

For schema changes:

1. **Create a migration**
   ```bash
   python -c "from database import init_db; init_db()"
   ```

2. **Test the migration**
   ```bash
   python -m pytest
   ```

3. **Document the change**
   Update CHANGELOG.md

## Adding New Dependencies

1. **Add to requirements.txt**
   ```bash
   pip install new-package
   pip freeze | grep new-package >> requirements.txt
   ```

2. **Test installation**
   ```bash
   pip install -r requirements.txt
   ```

3. **Update Docker**
   Update Dockerfile if necessary

## Release Process

1. Update version in config.py
2. Update CHANGELOG.md
3. Run full test suite
4. Create git tag
5. Deploy to production

## Resources

- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Google Gemini API Docs](https://ai.google.dev/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/)
- [Python Async Documentation](https://docs.python.org/3/library/asyncio.html)

## Support

- Create an issue on GitHub
- Check existing documentation
- Review code comments
- Contact team lead
