import subprocess
import os
import sys

def clone_repository():
    """Клонирование репозитория Ouroboros"""
    print("Клонирование репозитория...")
    
    # Директория для бота
    bot_dir = "C:\\Users\\bam\\Documents\\bot"
    os.makedirs(bot_dir, exist_ok=True)
    os.chdir(bot_dir)
    
    # URL репозитория
    repo_url = "https://github.com/your-username/ouroboros.git"
    
    # Клонирование
    try:
        subprocess.run(["git", "clone", repo_url, "."], check=True)
        print("✓ Репозиторий склонирован")
    except subprocess.CalledProcessError:
        print("⚠ Ошибка клонирования. Проверьте доступ к GitHub.")
    
    # Проверка существования файлов
    required_files = ["BIBLE.md", "VERSION", "README.md", "prompts/SYSTEM.md"]
    missing = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"⚠ Отсутствуют файлы: {', '.join(missing)}")
    else:
        print("✓ Все основные файлы найдены")
    
    print("✓ Клонирование завершено!")

if __name__ == "__main__":
    clone