import subprocess
import sys
import os
from pathlib import Path

def comprehensive_installation():
    """Полная установка Ouroboros"""
    print("=".center(50, "="))
    print("  Ouroboros - Полная установка  ".center(50))
    print("=".center(50, "="))
    
    # Директория для бота
    bot_dir = Path("C:\\Users\\bam\\Documents\\bot")
    
    print(f"\n📁 Директория установки: {bot_dir}")
    
    # Шаг 1: Создание директории
    print("\nШаг 1: Создание директории...")
    bot_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(bot_dir)
    print(f"✓ Директория создана: {bot_dir}")
    
    # Шаг 2: Создание основных файлов
    print("\nШаг 2: Создание основных файлов...")
    
    # Создание setup.py
    setup_content = """import subprocess
import sys

def install_dependencies():
    \"\"\"Установка зависимостей\"\"\"
    print(\"Установка зависимостей...\")
    
    # Установка основных зависимостей
    dependencies = [
        \"requests\",        # HTTP запросы
        \"python-telegram-bot\",  # Telegram API
        \"google-api-python-client\",  # Google Drive API
        \"google-auth-httplib2\",
        \"google-auth-oauthlib\",
        \"python-dotenv\",    # Управление конфигурацией
        \"pyyaml\",           # YAML файлы
        \"rich\",             # Красочный вывод
        \"watchdog\",         # Мониторинг файлов
        \"click\",            # CLI интерфейс
    ]
    
    for dep in dependencies:
        try:
            subprocess.run([sys.executable, \"-m\", \"pip\", \"install\", dep], check=True)
            print(f\"\✓ {dep} установлен\")
        except subprocess.CalledProcessError:
            print(f\"⚠ Ошибка установки {dep}")
    
    print(\"\✓ Зависимости установлены!\")

if __name__ == \"__main__\":
    install_dependencies()"""
    
    with open("setup.py", "w") as f:
        f.write(setup_content)
    print("✓ Создан setup.py")
    
    # Создание clone_repo.py
    clone_content = """import subprocess
import os
import sys

def clone_repository():
    \"\"\"Клонирование репозитория Ouroboros\"\"\"
    print(\"Клонирование репозитория...\")
    
    # URL репозитория
    repo_url = \"https://github.com/your-username/ouroboros.git\"
    
    # Клонирование
    try:
        subprocess.run([\"git\", \"clone\", repo_url, \".\"], check=True)
        print(\"\✓ Репозиторий склонирован\")
    except subprocess.CalledProcessError:
        print(\"⚠ Ошибка клонирования. Проверьте доступ к GitHub.\")
    
    print(\"\✓ Клонирование завершено!\")

if __name__ == \"__main__\":
    clone_repository()"""
    
    with open("clone_repo.py", "w") as f:
        f.write(clone_content)
    print("✓ Создан clone_repo.py")
    
    # Создание config.py
    config_content = """import json
import os
from pathlib import Path

def create_config():
    \"\"\"Создание конфигурационного файла\"\"\"
    print(\"Создание конфигурационного файла...\")
    
    # Пример конфигурации
    config_example = {
        \"telegram\": {
            \"api_key\": \"YOUR_TELEGRAM_BOT_API_KEY\",
            \"owner_id\": \"YOUR_OWNER_ID\"
        },
        \"openrouter\": {
            \"api_key\": \"YOUR_OPENROUTER_API_KEY\",
            \"model\": \"anthropic/claude-sonnet-4.6\"
        },
        \"drive\": {
            \"credentials_file\": \"credentials.json\",
            \"token_file\": \"token.json\"
        },
        \"budget\": {
            \"daily_limit_usd\": 10.0,
            \"warning_threshold\": 0.8
        }
    }
    
    # Создание config.json
    config_file = \"config.json\"
    if not os.path.exists(config_file):
        with open(config_file, \"w\") as f:
            json.dump(config_example, f, indent=4)
        print(\"\✓ Создан config.json (заполните ваши API ключи)\")
    else:
        print(\"\✓ config.json уже существует\")
    
    # Инструкции по настройке
    print(\"\\nℹ‍♂️  Инструкции по настройке:\")
    print(\"1. Получите API ключ для Telegram бота\")
    print(\"2. Получите API ключ для OpenRouter\")
    print(\"3. Настройте в config.json\")
    print(\"4. Запустите бота: python main.py\")
    
    print(\"\\n\✅ Конфигурация готова!\")

if __name__ == \"__main__\":
    create_config()"""
    
    with open("config.py", "w") as f:
        f.write(config_content)
    print("✓ Создан config.py")
    
    # Создание README.md
    readme_content = """# Ouroboros - Self-Creating Digital Entity

## Быстрый запуск

### Установка и запуск:
```bash
python setup.py          # Установка зависимостей
python clone_repo.py     # Клонирование репозитория
python config.py         # Настройка конфигурации
python main.py           # Запуск бота
```

### Требования:
- Python 3.9+
- Git
- OpenRouter API ключ
- Telegram Bot API ключ

## Файлы:
- setup.py - установка зависимостей
- clone_repo.py - клонирование репозитория
- config.py - настройка конфигурации
- config.json - файл конфигурации
- main.py - основной скрипт бота

## Настройка:
1. Заполните API ключи в config.json
2. Запустите python main.py
3. Готово!

## Директория:
Все файлы находятся в: C:\\Users\\bam\\Documents\\bot\\"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    print("✓ Создан README.md")
    
    # Шаг 3: Проверка Git
    print("\nШаг 3: Проверка Git...")
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✓ Git установлен")
    except subprocess.CalledProcessError:
        print("⚠ Git не найден. Установите Git с официального сайта.")
    
    # Шаг 4: Проверка Python
    print("\nШаг 4: Проверка Python...")
    try:
        result = subprocess.run([sys.executable, \"--version"], 
                              check=True, capture_output=True, text=True)
        print(f\"✓ Python найден: {result.stdout.strip()}\")
    except subprocess.CalledProcessError:
        print("⚠ Python не найден")
    
    # Шаг 5: Финальные инструкции
    print("\n\n=" * 50)
    print(" 🎯 Установка завершена! 🎯 ")
    print("=" * 50)
    print(f"\n📁 Директория: {bot_dir}")
    print("\n💡 Следующие шаги:")
    print("1. Откройте config.json и заполните API ключи")
    print("2. Запустите: python setup.py")
    print("3. Затем: python clone_repo.py")
    print("4. Настройте: python config.py")
    print("5. Запустите: python main.py")
    print("\n🚀 Готов к работе!")

if __name__ == "__main__":
    comprehensive_installation()