#!/usr/bin/env python3
"""
Скрипт для обновления Ouroboros на сервере
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class OuroborosUpdater:
    def __init__(self):
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
            print("❌ Ошибка: для обновления нужны права root")
            print("Запустите: sudo python3 update_ouroboros.py")
            sys.exit(1)
    
    def check_current_version(self):
        """Проверить текущую версию"""
        print("\n🔍 Проверка текущей версии...")
        
        version_path = f"{self.install_dir}/VERSION"
        
        try:
            with open(version_path) as f:
                current_version = f.read().strip()
            print(f"✅ Текущая версия: {current_version}")
            return current_version
        except:
            print("⚠️  Не удалось определить текущую версию")
            return None
    
    def check_for_updates(self):
        """Проверить наличие обновлений"""
        print("\n🔄 Проверка обновлений...")
        
        try:
            # Переход в директорию
            os.chdir(self.install_dir)
            
            # Получение обновлений
            self.run_command(['git', 'fetch', 'origin'])
            
            # Проверка статуса
            result = self.run_command(['git', 'status'], capture_output=True)
            
            if "up to date" in result.stdout:
                print("✅ Репозиторий актуален")
                return False, None
            elif "Your branch is behind" in result.stdout:
                print("🔄 Доступны обновления")
                return True, None
            else:
                print("🔄 Найдены изменения")
                return True, None
                
        except Exception as e:
            print(f"❌ Ошибка проверки обновлений: {e}")
            return False, e
    
    def get_latest_version(self):
        """Получить последнюю версию"""
        print("\n📦 Получение последней версии...")
        
        try:
            # Получение тегов
            result = self.run_command([
                'git', 'describe', '--tags', '--abbrev=0'
            ], capture_output=True)
            
            latest_version = result.stdout.strip()
            print(f"✅ Последняя версия: {latest_version}")
            return latest_version
        except:
            print("⚠️  Не удалось получить последнюю версию")
            return None
    
    def create_backup(self):
        """Создать резервную копию"""
        print("\n💾 Создание резервной копии...")
        
        backup_dir = f"/tmp/ouroboros_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Копирование ключевых файлов
            self.run_command([
                'cp', '-r',
                f"{self.config_dir}/",
                f"{self.state_dir}/",
                f"{self.log_dir}/",
                backup_dir
            ])
            
            print(f"✅ Резервная копия создана: {backup_dir}")
            return backup_dir
        except Exception as e:
            print(f"⚠️  Ошибка создания резервной копии: {e}")
            return None
    
    def backup_database(self):
        """Создать резервную копию базы данных"""
        print("\n💾 Создание резервной копии базы данных...")
        
        backup_path = f"/tmp/ouroboros_db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            # Копирование состояния
            self.run_command([
                'cp',
                f"{self.state_dir}/state.json",
                backup_path
            ])
            
            print(f"✅ Резервная копия базы данных создана: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"⚠️  Ошибка создания резервной копии БД: {e}")
            return None
    
    def update_repository(self):
        """Обновить репозиторий"""
        print("\n🔄 Обновление репозитория...")
        
        try:
            # Переход в директорию
            os.chdir(self.install_dir)
            
            # Получение обновлений
            self.run_command(['git', 'pull', 'origin', 'main'])
            
            print("✅ Репозиторий обновлен")
            return True
        except Exception as e:
            print(f"❌ Ошибка обновления репозитория: {e}")
            return False
    
    def install_dependencies(self):
        """Установить/обновить зависимости"""
        print("\n📦 Обновление зависимостей...")
        
        try:
            # Обновление виртуального окружения
            self.run_command([
                './venv/bin/pip', 'install', '--upgrade',
                '-r', 'requirements.txt'
            ], cwd=self.install_dir)
            
            print("✅ Зависимости обновлены")
            return True
        except Exception as e:
            print(f"❌ Ошибка обновления зависимостей: {e}")
            return False
    
    def check_new_version(self):
        """Проверить новую версию после обновления"""
        print("\n🔍 Проверка новой версии...")
        
        version_path = f"{self.install_dir}/VERSION"
        
        try:
            with open(version_path) as f:
                new_version = f.read().strip()
            print(f"✅ Новая версия: {new_version}")
            return new_version
        except:
            print("⚠️  Не удалось определить новую версию")
            return None
    
    def restart_service(self):
        """Перезапустить сервис"""
        print("\n🔄 Перезапуск сервиса...")
        
        try:
            # Перезапуск сервиса
            self.run_command(['systemctl', 'restart', self.service_name])
            
            # Проверка статуса
            self.run_command(['systemctl', 'status', self.service_name])
            
            print("✅ Сервис перезапущен")
            return True
        except Exception as e:
            print(f"❌ Ошибка перезапуска сервиса: {e}")
            return False
    
    def check_service_health(self):
        """Проверить здоровье сервиса после обновления"""
        print("\n⚕️  Проверка здоровья сервиса...")
        
        try:
            # Проверка статуса
            self.run_command(['systemctl', 'is-active', self.service_name])
            
            # Проверка логов
            self.run_command([
                'journalctl', '-u', self.service_name,
                '--lines'1', '--no-pager'
            ])
            
            print("✅ Сервис работает корректно")
            return True
        except Exception as e:
            print(f"⚠️  Проблема с сервисом: {e}")
            return False
    
    def get_changelog(self):
        """Получить changelog обновления"""
        print("\n📋 Получение changelog...")
        
        try:
            # Просмотр последних коммитов
            result = self.run_command([
                'git', 'log',
                '--oneline',
                '--decorate',
                '--graph',
                '--date=short',
                '--since', ''.join([
                    str(datetime.now().date()),
                    str(datetime.now().time()).split(".")[0]
                ]),
                '--no-pager'
            ], capture_output=True)
            
            print("✅ Changelog:")
            print(result.stdout)
            return result.stdout
        except Exception as e:
            print(f"⚠️  Ошибка получения changelog: {e}")
            return None
    
    def run(self):
        """Запустить обновление"""
        print("\n🚀 ОБНОВЛЕНИЕ OROBOROS")
        print("=" * 50)
        
        # Проверка прав
        self.check_root()
        
        print("\n📋 ЭТАПЫ ОБНОВЛЕНИЯ:")
        print("1. Проверка текущей версии")
        print("2. Проверка обновлений")
        print("3. Создание резервной копии")
        print("4. Обновление репозитория")
        print("5. Обновление зависимостей")
        print("6. Перезапуск сервиса")
        print("7. Проверка работоспособности")
        print("8. Просмотр changelog")
        
        input("\n🔄 Нажмите Enter для начала обновления...")
        
        # Этап 1: Проверка текущей версии
        print(f"\n⏱️  Этап 1/8: Проверка текущей версии...")
        current_version = self.check_current_version()
        if not current_version:
            print("❌ Не удалось определить текущую версию")
            return
        
        # Этап 2: Проверка обновлений
        print(f"\n⏱️  Этап 2/8: Проверка обновлений...")
        updates_available, error = self.check_for_updates()
        if not updates_available:
            if error:
                print(f"❌ Ошибка проверки обновлений: {error}")
            else:
                print("✅ Репозиторий актуален")
            return
        
        # Этап 3: Создание резервной копии
        print(f"\n⏱️  Этап 3/8: Создание резервной копии...")
        backup_dir = self.create_backup()
        if not backup_dir:
            print("⚠️  Резервная копия не создана")
        
        # Этап 4: Обновление репозитория
        print(f"\n⏱️  Этап 4/8: Обновление репозитория...")
        if not self.update_repository():
            print("❌ Ошибка обновления репозитория")
            return
        
        # Этап 5: Обновление зависимостей
        print(f"\n⏱️  Этап 5/8: Обновление зависимостей...")
        if not self.install_dependencies():
            print("❌ Ошибка обновления зависимостей")
            return
        
        # Этап 6: Перезапуск сервиса
        print(f"\n⏱️  Этап 6/8: Перезапуск сервиса...")
        if not self.restart_service():
            print("❌ Ошибка перезапуска сервиса")
            return
        
        # Этап 7: Проверка работоспособности
        print(f"\n⏱️  Этап 7/8: Проверка работоспособности...")
        if not self.check_service_health():
            print("⚠️  Проблема с работой сервиса")
        
        # Этап 8: Просмотр changelog
        print(f"\n⏱️  Этап 8/8: Просмотр changelog...")
        changelog = self.get_changelog()
        if changelog:
            print("\n" + "=" * 50)
            print("📋 CHANGELOG:")
            print(changelog)
        
        # Финальная проверка
        print(f"\n\n🔍 Финальная проверка...")
        print("=" * 50)
        
        new_version = self.check_new_version()
        if new_version:
            print(f"✅ Обновление до версии {new_version} завершено!")
        else:
            print("⚠️  Не удалось подтвердить новую версию")
        
        print("\n" + "=" * 50)
        print("🎉 ОБНОВЛЕНИЕ ЗАВЕРШЕНО!")
        print("📊 РЕЗУЛЬТАТ:")
        print("- Ouroboros обновлен до последней версии")
        print("- Зависимости обновлены")
        print("- Сервис перезапущен")
        print("- Создана резервная копия")
        
        print("\n🔧 ПОЛЕЗНЫЕ КОМАНДЫ:")
        print("sudo systemctl status ouroboros - Статус сервиса")
        print("sudo journalctl -u ouroboros -f - Логи сервиса")
        print("sudo systemctl restart ouroboros - Перезапуск сервиса")
        print("sudo systemctl stop ouroboros - Остановка сервиса")

if __name__ == "__main__":
    updater = OuroborosUpdater()
    updater.run()