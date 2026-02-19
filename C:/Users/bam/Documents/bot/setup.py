import subprocess
import sys

def install_dependencies():
    """Установка зависимостей"""
    print("Установка зависимостей...")
    
    # Установка uv (Python менеджер пакетов)
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
        print("✓ uv установлен")
    except subprocess.CalledProcessError:
        print("⚠ Ошибка установки uv. Проверьте интернет-соединение.")
    
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
    ]
    
    for dep in dependencies:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            print(f"✓ {dep} установлен")
        except subprocess.CalledProcessError:
            print(f"⚠ Ошибка установки {dep}")
    
    print("✓ Зависимости установлены!")

if __name__ == "__main__":
    install_dependencies()