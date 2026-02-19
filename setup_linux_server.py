#!/usr/bin/env python3
"""
Скрипт для первоначальной настройки Ouroboros на Linux сервере
"""

import os
import sys
import subprocess
import json
import getpass
import time
from pathlib import Path

class LinuxSetup:
    def __init__(self):
        self.repo_owner = "groove52"
        self.repo_name = "ouroboros"
        self.install_dir = "/opt/ouroboros"
        self.config_dir = "/etc/ouroboros"
        self.state_dir = "/var/lib/ouroboros"
        self.log_dir = "/var/log/ouroboros"
        self.user = "ouroboros"
        
    def run_command(self, cmd, check=True, capture_output=False, cwd=None):
        """Выполнить shell команду"""
        print(f"🚀 Выполнение: {' '.join(cmd)}")
        result = subprocess.run(cmd, 
                               check=check, 
                               capture_output=capture_output,
                               cwd=cwd,
                               text=True)
        if capture_output:
            print(f"✅ Результат: {result.stdout.strip()}")
        return result
    
    def check_root(self):
        """Проверить, запущен ли как root"""
        if os.geteuid() != 0:
            print("❌ Ошибка: для установки нужны права root")
            print("Запустите: sudo python3 setup_linux_server.py")
            sys.exit(1)
    
    def check_system(self):
        """Проверить системные требования"""
        print("🔍 Проверка системы...")
        
        # Проверка Ubuntu
        try:
            with open('/etc/os-release') as f:
                os_info = f.read()
            if "Ubuntu" not in os_info and "Debian" not in os_info:
                print("⚠️  Предупреждение: тестировалось на Ubuntu/Debian")
        except:
            print("⚠️  Не удалось определить OS")
        
        # Проверка Python
        python_version = sys.version.split()[0]
        print(f"🐍 Python: {python_version}")
        
        # Проверка Git
        try:
            self.run_command(['git', '--version'], capture_output=True)
        except:
            print("❌ Git не установлен")
            return False
        
        return True
    
    def create_user_and_dirs(self):
        """Создать пользователя и директории"""
        print("\n👥 Создание пользователя и директорий...")
        
        # Создание пользователя
        try:
            self.run_command(['useradd', '-r', '-s', '/bin/false', self.user])
            print(f"✅ Пользователь {self.user} создан")
        except:
            print(f"ℹ️  Пользователь {self.user} уже существует")
        
        # Создание директорий
        dirs = {
            self.install_dir: 'ouroboros:ouroboros',
            self.config_dir: 'ouroboros:ouroboros',
            self.state_dir: 'ouroboros:ouroboros',
            self.log_dir: 'ouroboros:ouroboros'
        }
        
        for dir_path, owner in dirs.items():
            try:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                self.run_command(['chown', owner, dir_path])
                print(f"✅ Директория {dir_path} создана")
            except Exception as e:
                print(f"❌ Ошибка создания {dir_path}: {e}")
                return False
        
        return True
    
    def clone_repository(self):
        """Клонировать репозиторий"""
        print("\n🔧 Клонирование репозитория...")
        
        try:
            # Переход в директорию
            os.chdir(self.install_dir)
            
            # Клонирование
            self.run_command([
                'git', 'clone',
                f'git@github.com:{self.repo_owner}/{self.repo_name}.git',
                '.'
            ], cwd=self.install_dir)
            
            print("✅ Репозиторий склонирован")
            return True
        except Exception as e:
            print(f"❌ Ошибка клонирования: {e}")
            return False
    
    def setup_virtualenv(self):
        """Создать виртуальное окружение и установить зависимости"""
        print("\n🤝 Создание виртуального окружения...")
        
        try:
            # Создание venv
            self.run_command([
                'python3', '-m', 'venv', 'venv'
            ], cwd=self.install_dir)
            
            # Установка зависимостей
            self.run_command([
                './venv/bin/pip', 'install',
                '-r', 'requirements.txt'
            ], cwd=self.install_dir)
            
            print("✅ Виртуальное окружение создано")
            return True
        except Exception as e:
            print(f"❌ Ошибка venv: {e}")
            return False
    
    def setup_config(self):
        """Создать конфигурационный файл"""
        print("\n📋 Создание конфигурации...")
        
        config_path = f"{self.config_dir}/config.json"
        
        # Пример конфигурации
        config = {
            "telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN_HERE",
            "openrouter_api_key": "YOUR_OPENROUTER_API_KEY_HERE",
            "model": "anthropic/claude-sonnet-4.6",
            "budget_usd": 10.0,
            "log_level": "INFO",
            "state_path": self.state_dir,
            "log_path": self.log_dir
        }
        
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            
            # Установка прав
            self.run_command(['chown', 'ouroboros:ouroboros', config_path])
            self.run_command(['chmod', '600', config_path])
            
            print(f"✅ Конфигурация создана в {config_path}")
            print("⚠️  НЕ ЗАБУДЬТЕ ЗАМЕНИТЬ ТОКЕНЫ!")
            return True
        except Exception as e:
            print(f"❌ Ошибка конфигурации: {e}")
            return False
    
    def setup_systemd_service(self):
        """Создать systemd сервис"""
        print("\n🔧 Создание systemd сервиса...")
        
        service_content = f"""[Unit]
Description=Ouroboros AI Agent
After=network.target

[Service]
Type=simple
User=ouroboros
Group=ouroboros
WorkingDirectory={self.install_dir}
Environment=VIRTUAL_ENV={self.install_dir}/venv
Environment=PATH={self.install_dir}/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart={self.install_dir}/venv/bin/python -m ouroboros.agent
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
        
        service_path = "/etc/systemd/system/ouroboros.service"
        
        try:
            with open(service_path, 'w') as f:
                f.write(service_content)
            
            print("✅ Сервис создан")
            return True
        except Exception as e:
            print(f"❌ Ошибка создания сервиса: {e}")
            return False
    
    def start_service(self):
        """Запустить и включить сервис"""
        print("\n🚀 Запуск сервиса...")
        
        try:
            # Перезагрузка systemd
            self.run_command(['systemctl', 'daemon-reload'])
            
            # Запуск сервиса
            self.run_command(['systemctl', 'start', 'ouroboros'])
            
            # Включение автозапуска
            self.run_command(['systemctl', 'enable', 'ouroboros'])
            
            # Проверка статуса
            result = self.run_command(['systemctl', 'status', 'ouroboros'], 
                                     capture_output=True)
            print(result.stdout)
            
            print("✅ Сервис запущен")
            return True
        except Exception as e:
            print(f"❌ Ошибка запуска сервиса: {e}")
            return False
    
    def verify_installation(self):
        """Проверить установку"""
        print("\n🔍 Проверка установки...")
        
        # Проверка сервиса
        try:
            self.run_command(['systemctl', 'is-active', 'ouroboros'])
            print("✅ Сервис активен")
        except:
            print("⚠️  Сервис не активен")
        
        # Проверка директорий
        dirs_to_check = [
            self.install_dir,
            self.config_dir,
            self.state_dir,
            self.log_dir
        ]
        
        for dir_path in dirs_to_check:
            if Path(dir_path).exists():
                print(f"✅ Директория {dir_path} существует")
            else:
                print(f"❌ Директория {dir_path} не найдена")
        
        # Проверка файлов
        files_to_check = [
            f"{self.install_dir}/agent.py",
            f"{self.config_dir}/config.json",
        ]
        
        for file_path in files_to_check:
            if Path(file_path).exists():
                print(f"✅ Файл {file_path} существует")
            else:
                print(f"❌ Файл {file_path} не найден")
    
    def run(self):
        """Запустить установку"""
        print("🚀 Запуск установки Ouroboros на Linux...")
        print("=" * 50)
        
        # Проверка прав
        self.check_root()
        
        # Проверка системы
        if not self.check_system():
            print("❌ Система не прошла проверку")
            return
        
        # Создание пользователя и директорий
        if not self.create_user_and_dirs():
            print("❌ Ошибка создания структуры")
            return
        
        # Клонирование репозитория
        if not self.clone_repository():
            print("❌ Ошибка клонирования репозитория")
            return
        
        # Настройка виртуального окружения
        if not self.setup_virtualenv():
            print("❌ Ошибка настройки окружения")
            return
        
        # Настройка конфигурации
        if not self.setup_config():
            print("❌ Ошибка настройки конфигурации")
            return
        
        # Создание systemd сервиса
        if not self.setup_systemd_service():
            print("❌ Ошибка создания сервиса")
            return
        
        # Запуск сервиса
        if not self.start_service():
            print("❌ Ошибка запуска сервиса")
            return
        
        # Проверка установки
        self.verify_installation()
        
        print("\n" + "=" * 50)
        print("🎉 Установка завершена!")
        print("📋 Следующие шаги:")
        print("1. Настройте Telegram бота в ", 
              f"{self.config_dir}/config.json")
        print("2. Получите OpenRouter API ключ")
        print("3. Перезапустите сервис: sudo systemctl restart ouroboros")
        print("4. Проверьте логи: sudo journalctl -u ouroboros -f")

if __name__ == "__main__":
    setup = LinuxSetup()
    setup.run()