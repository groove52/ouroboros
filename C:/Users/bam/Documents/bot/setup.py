import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Установка зависимостей"""
    print("Установка зависимостей...")
    
    # Директория для бота
    bot_dir = Path("C:\\Users\\bam\\Documents\\bot")
    os.chdir(bot_dir)
    
    # Установка uv (Python менеджер пакетов)
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
        print("✓ uv установлен")
    except subprocess.CalledProcessError:
        print("⚠ Ошибка установки uv. Попробуем без него.")
    
    # Установка основных зависимостей
    dependencies = [
        "requests",        # HTTP запросы
        "python-telegram-bot",  # Telegram API
        "google-api-python-client",  # Google Drive API
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "python-dotenv",    # Управление конфигурацией
        "pyyaml",           # YAML файлы
        "rich",             # Красочный вывод
        "watchdog",         # Мониторинг файлов
        "click",            # CLI интерфейс
        "uvicorn",          # ASGI сервер (если нужен)
        "fastapi",          # API фреймворк (если нужен)
    ]
    
    for dep in dependencies:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            print(f"✓ {dep} установлен")
        except subprocess.CalledProcessError:
            print(f"⚠ Ошибка установки {dep}")
    
    print("\n✅ Зависимости установлены!")
    
    # Проверка установки
    print("\nℹ Проверка установки:")
    try:
        import telegram
        print("✓ python-telegram-bot установлен")
    except ImportError:
        print("⚠ python-telegram-bot не найден")
    
    try:
        import google
        print("✓ google-api-python-client установлен")
    except ImportError:
        print("⚠ google-api-python-client не найден")

if __name__ == "__main__":
    install_dependencies()