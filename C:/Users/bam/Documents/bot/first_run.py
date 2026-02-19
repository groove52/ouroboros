import subprocess
import sys
import os
from pathlib import Path

def first_run():
    """Первый запуск бота"""
    print("Первый запуск Ouroboros...")
    
    # Директория для бота
    bot_dir = Path("C:\\Users\\bam\\Documents\\bot")
    os.chdir(bot_dir)
    
    # Проверка существования файлов
    required_files = [
        "setup.py",
        "clone_repo.py",
        "config.py",
        "config_example.json",
        "README.md"
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"⚠ Отсутствуют файлы: {', '.join(missing)}")
        return
    
    # Запуск установки
    print("\nШаг 1: Установка зависимостей...")
    subprocess.run([sys.executable, "setup.py"], check=True)
    
    # Запуск клонирования репозитория
    print("\nШаг 2: Клонирование репозитория...")
    subprocess.run([sys.executable, "clone_repo.py"], check=True)
    
    # Настройка конфигурации
    print("\nШаг 3: Настройка конфигурации...")
    subprocess.run([sys.executable, "config.py"], check=True)
    
    # Проверка готовности
    print("\n✅ Первый запуск завершен!")
    print("\nℹ Следующие шаги:")
    print("1. Откройте config.json и заполните API ключи")
    print("2. Запустите бота: python main.py")
    print("3. Настройте Telegram бота")
    
    # Показать расположение файлов
    print(f"\n📁 Ваши файлы находятся в: {bot_dir}")
    
    # Список созданных файлов
    print("\n📋 Созданные файлы:")
    for file in Path("C:\\Users\\bam\\Documents\\bot").glob("*"):
        if file.is_file():
            print(f"  ✓ {file.name}")

if __name__ == "__main__":
    first_run()