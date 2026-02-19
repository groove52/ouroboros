import json
import os
from pathlib import Path

def create_config():
    """Создание конфигурационного файла"""
    print("Создание конфигурационного файла...")
    
    # Директория для бота
    bot_dir = Path("C:\\Users\\bam\\Documents\\bot")
    os.chdir(bot_dir)
    
    # Проверка существующих файлов
    config_file = bot_dir / "config.json"
    env_file = bot_dir / ".env"
    
    # Пример конфигурации
    config_example = {
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
    
    # Создание config.json
    if not config_file.exists():
        with open(config_file, "w") as f:
            json.dump(config_example, f, indent=4)
        print("✓ Создан config.json (заполните ваши API ключи)")
    else:
        print("✓ config.json уже существует")
    
    # Создание .env (пример)
    if not env_file.exists():
        env_content = """# Telegram Bot API Key
TELEGRAM_BOT_API_KEY=your_telegram_bot_api_key_here

# OpenRouter API Key
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Google Drive Credentials
GOOGLE_CREDENTIALS_PATH=credentials.json
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✓ Создан .env (пример)")
    else:
        print("✓ .env уже существует")
    
    # Инструкции по настройке
    print("\nℹ Инструкции по настройке:")
    print("1. Получите API ключ для Telegram бота")
    print("2. Получите API ключ для OpenRouter")
    print("3. Настройте в config.json или .env")
    print("4. Запустите first_run.py")
    
    print("\n✅ Конфигурация готова!")

if __name__ == "__main__":
    create_config()