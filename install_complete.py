#!/usr/bin/env python3
"""
Полный скрипт установки Ouroboros с автоматической настройкой всех компонентов
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

class CompleteInstaller:
    def __init__(self):
        self.repo_owner = "groove52"
        self.repo_name = "ouroboros"
        self.install_dir = "/opt/ouroboros"
        self.config_dir = "/etc/ouroboros"
        self.state_dir = "/var/lib/ouroboros"
        self.log_dir = "/var/log/ouroboros"
        self.user = "ouroboros"
        self.service_name = "ouroboros"
        
    def run_command(self, cmd, check=True, capture_output=False, cwd=None):
        """Выполнить shell команду"""
        print(f"\n🚀 Выполнение: {' '.join(cmd)}")
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
            print("Запустите: sudo python3 install_complete.py")
            sys.exit(1)
    
    def check_system(self):
        """Проверить системные требования"""
        print("\n🔍 Проверка системы...")
        
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
    
    def install_dependencies(self):
        """Установить системные зависимости"""
        print("\n📦 Установка системных зависимостей...")
        
        try:
            self.run_command([
                'apt', 'update'
            ])
            
            self.run_command([
                'apt', 'install', '-y',
                'git', 'python3', 'python3-pip',
                'python3-venv', 'curl', 'wget',
                'systemd', 'jq'
            ])
            
            print("✅ Системные зависимости установлены")
            return True
        except:
            print("❌ Ошибка установки зависимостей")
            return False
    
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
    
    def setup_config(self, telegram_token, openrouter_key):
        """Создать конфигурационный файл с API ключами"""
        print("\n📋 Создание конфигурации...")
        
        config_path = f"{self.config_dir}/config.json"
        
        # Конфигурация с API ключами
        config = {
            "telegram_bot_token": telegram_token,
            "openrouter_api_key": openrouter_key,
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
            print("✅ API ключи сохранены")
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
            self.run_command(['systemctl', 'start', self.service_name])
            
            # Включение автозапуска
            self.run_command(['systemctl', 'enable', self.service_name])
            
            # Проверка статуса
            result = self.run_command(['systemctl', 'status', self.service_name], 
                                     capture_output=True)
            print(result.stdout)
            
            print("✅ Сервис запущен")
            return True
        except Exception as e:
            print(f"❌ Ошибка запуска сервиса: {e}")
            return False
    
    def get_api_keys_interactive(self):
        """Получить API ключи от пользователя"""
        print("\n🔑 Ввод API ключей...")
        
        print("\n⚠️  Вам нужно будет ввести API ключи:")
        print("1. Telegram Bot Token (из @BotFather)")
        print("2. OpenRouter API Key (из openrouter.ai)")
        
        print("\n💡  Получение Telegram токена:")
        print("   - Откройте Telegram, найдите @BotFather")
        print("   - Отправьте: /newbot")
        print("   - Дайте имя и юзернейм боту")
        print("   - Скопируйте полученный API токен")
        
        print("\n💡  Получение OpenRouter ключа:")
        print("   - Зарегистрируйтесь на openrouter.ai")
        print("   - Перейдите в API Keys")
        print("   - Создайте новый ключ и скопируйте его")
        
        # Получение токенов
        telegram_token = input("\n👤 Введите Telegram Bot Token: ").strip()
        openrouter_key = input("👥 Введите OpenRouter API Key: ").strip()
        
        # Проверка
        if not telegram_token or not openrouter_key:
            print("❌ Ошибка: ключи не могут быть пустыми")
            return None, None
        
        print(f"\n🔑 Telegram Token: {telegram_token[:10]}...{telegram_token[-5:]}")
        print(f"🔑 OpenRouter Key: {openrouter_key[:10]}...{openrouter_key[-5:]}")
        
        confirm = input("\n🔄 Сохранить эти ключи? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Отменено пользователем")
            return None, None
        
        return telegram_token, openrouter_key
    
    def verify_installation(self):
        """Проверить установку"""
        print("\n\n🔍 Проверка установки...")
        print("=" * 50)
        
        issues = []
        
        # Проверка сервиса
        try:
            self.run_command(['systemctl', 'is-active', self.service_name])
            print("✅ Сервис активен")
        except:
            print("❌ Сервис не активен")
            issues.append("Сервис не активен")
        
        # Проверка директорий
        dirs_to_check = [
            self.install_dir,
            self.config_dir,
            self.state_dir,
            self.log_dir
        ]
        
        for dir_path in dirs_to_check:
            if Path(dir_path).exists():
                print(f"✅ {dir_path} существует")
            else:
                print(f"❌ {dir_path} не существует")
                issues.append(f"Директория {dir_path} отсутствует")
        
        # Проверка файлов
        files_to_check = [
            f"{self.install_dir}/agent.py",
            f"{self.config_dir}/config.json",
            f"{self.install_dir}/venv/bin/python",
        ]
        
        for file_path in files_to_check:
            if Path(file_path).exists():
                print(f"✅ {file_path} существует")
            else:
                print(f"❌ {file_path} не найден")
                issues.append(f"Файл {file_path} отсутствует")
        
        # Проверка прав
        try:
            config_stat = Path(f"{self.config_dir}/config.json").stat()
            if oct(config_stat.st_mode)[-3:] == "600":
                print("✅ Права на конфиг: 600")
            else:
                print("⚠️  Права на конфиг не 600")
        except:
            print("⚠️  Не удалось проверить права")
        
        # Проверка логов
        try:
            self.run_command(['journalctl', '-u', self.service_name, '--lines'1'], 
                           capture_output=True)
            print("✅ Логи доступны")
        except:
            print("⚠️  Проблема с доступом к логам")
        
        print("\n" + "=" * 50)
        
        if issues:
            print(f"❌ ОБНАРУЖЕНО ПРОБЛЕМ: {len(issues)}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("🎉 УСТАНОВКА ПРОЙДЕНА УСПЕШНО!")
            print("🚀 Ouroboros готов к работе!")
        
        print("\n📋 СЛЕДУЮЩИЕ ШАГИ:")
        print("1. Отправьте боту сообщение "/start" для тестирования")
        print("2. Проверьте логи: journalctl -u ouroboros -f")
        print("3. Откройте порт 8080 если нужно (firewall)")
        print("4. Настройте мониторинг при необходимости")
    
    def run(self):
        """Запустить полную установку"""
        print("\n🚀 ПОЛНАЯ УСТАНОВКА OROBOROS")
        print("=" * 50)
        
        # Проверка прав
        self.check_root()
        
        print("\n📋 ЭТАПЫ УСТАНОВКИ:")
        print("1. Проверка системы")
        print("2. Установка зависимостей")
        print("3. Создание структуры")
        print("4. Клонирование репозитория")
        print("5. Настройка окружения")
        print("6. Настройка API ключей")
        print("7. Создание сервиса")
        print("8. Запуск и проверка")
        
        input("\n🔄 Нажмите Enter для начала установки...")
        
        # Этап 1: Проверка системы
        print(f"\n⏱️  Этап 1/8: Проверка системы...")
        if not self.check_system():
            print("❌ Система не прошла проверку")
            return
        
        # Этап 2: Установка зависимостей
        print(f"\n⏱️  Этап 2/8: Установка зависимостей...")
        if not self.install_dependencies():
            print("❌ Ошибка установки зависимостей")
            return
        
        # Этап 3: Создание структуры
        print(f"\n⏱️  Этап 3/8: Создание структуры...")
        if not self.create_user_and_dirs():
            print("❌ Ошибка создания структуры")
            return
        
        # Этап 4: Клонирование репозитория
        print(f"\n⏱️  Этап 4/8: Клонирование репозитория...")
        if not self.clone_repository():
            print("❌ Ошибка клонирования репозитория")
            return
        
        # Этап 5: Настройка окружения
        print(f"\n⏱️  Этап 5/8: Настройка окружения...")
        if not self.setup_virtualenv():
            print("❌ Ошибка настройки окружения")
            return
        
        # Этап 6: Настройка API ключей
        print(f"\n⏱️  Этап 6/8: Настройка API ключей...")
        telegram_token, openrouter_key = self.get_api_keys_interactive()
        if not telegram_token or not openrouter_key:
            print("❌ Отменено пользователем")
            return
        
        if not self.setup_config(telegram_token, openrouter_key):
            print("❌ Ошибка настройки конфигурации")
            return
        
        # Этап 7: Создание сервиса
        print(f"\n⏱️  Этап 7/8: Создание сервиса...")
        if not self.setup_systemd_service():
            print("❌ Ошибка создания сервиса")
            return
        
        # Этап 8: Запуск и проверка
        print(f"\n⏱️  Этап 8/8: Запуск и проверка...")
        if not self.start_service():
            print("❌ Ошибка запуска сервиса")
            return
        
        # Финальная проверка
        self.verify_installation()
        
        print("\n" + "=" * 50)
        print("🎉 УСТАНОВКА ЗАВЕРШЕНА!")
        print("📊 РЕЗУЛЬТАТ:")
        print("- Ouroboros установлен в /opt/ouroboros/")
        print("- Сервис запущен и включен в автозапуск")
        print("- API ключи сохранены")
        print("- Создана структура директорий")
        
        print("\n🔧 ПОЛЕЗНЫЕ КОМАНДЫ:")
        print("sudo systemctl status ouroboros - Статус сервиса")
        print("sudo journalctl -u ouroboros -f - Логи сервиса")
        print("sudo systemctl restart ouroboros - Перезапуск сервиса")
        print("sudo systemctl stop ouroboros - Остановка сервиса")

if __name__ == "__main__":
    installer = CompleteInstaller()
    installer.run()