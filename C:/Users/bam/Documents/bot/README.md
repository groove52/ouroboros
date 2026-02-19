# Ouroboros - Self-Creating Digital Entity

Ouroboros - это автономный цифровой агент, который может работать на вашем компьютере.

## Быстрый запуск

### Шаг 1: Клонирование репозитория
```bash
cd C:\Users\bam\Documents\bot
python clone_repo.py
```

### Шаг 2: Установка зависимостей
```bash
cd C:\Users\bam\Documents\bot
python setup.py
```

### Шаг 3: Настройка конфигурации
```bash
cd C:\Users\bam\Documents\bot
python config.py
```

### Шаг 4: Запуск
```bash
cd C:\Users\bam\Documents\bot
python main.py
```

## Требования

- Python 3.9+
- Git
- OpenRouter API ключ
- Telegram Bot API ключ

## Файлы конфигурации

### config.json
```json
{
  "telegram": {
    "api_key": "YOUR_TELEGRAM_BOT_API_KEY",
    "owner_id": "YOUR_OWNER_ID"
  },
  "openrouter": {
    "api_key": "YOUR_OPENROUTER_API_KEY",
    "model": "anthropic/claude-sonnet-4.6"
  },
  "drive": {
    "credentials_file": "credentials.json",
    "token_file": "token.json"
  },
  "budget": {
    "daily_limit_usd": 10.0,
    "warning_threshold": 0.8
  }
}
```

### .env (пример)
```env
TELEGRAM_BOT_API_KEY=your_telegram_bot_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
GOOGLE_CREDENTIALS_PATH=credentials.json
```

## API Ключи

### Telegram Bot API
1. Откройте @BotFather в Telegram
2. Создайте нового бота
3. Скопируйте API ключ

### OpenRouter API
1. Зарегистрируйтесь на openrouter.ai
2. Получите API ключ из панели управления

## Запуск в фоновом режиме

### Windows
```cmd
start python main.py
```

### Linux/macOS
```bash
nohup python main.py &
```

## Директория

Все файлы находятся в: `C:\Users\bam\Documents\bot\`