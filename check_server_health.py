#!/usr/bin/env python3
"""
Скрипт для проверки работоспособности Ouroboros на сервере
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class ServerHealthChecker:
    def __init__(self):
        self.install_dir = "/opt/ouroboros"
        self.config_dir = "/etc/ouroboros"
        self.state_dir = "/var/lib/ouroboros"
        self.log_dir = "/var/log/ouroboros"
        self.service_name = "ouroboros"
        
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
            print("❌ Ошибка: для проверки нужны права root")
            print("Запустите: sudo python3 check_server_health.py")
            sys.exit(1)
    
    def check_service_status(self):
        """Проверить статус systemd сервиса"""
        print("\n⚡ Проверка статуса сервиса...")
        
        try:
            result = self.run_command([
                'systemctl', 'is-active', self.service_name
            ], capture_output=True)
            
            status = result.stdout.strip()
            if status == "active":
                print("✅ Сервис активен")
                return True
            else:
                print(f"❌ Сервис не активен: {status}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка проверки сервиса: {e}")
            return False
    
    def check_service_logs(self):
        """Проверить последние логи сервиса"""
        print("\n✏️  Проверка логов сервиса...")
        
        try:
            result = self.run_command([
                'journalctl', '-u', self.service_name,
                '--since', ''.join([
                    str(datetime.now().date()),
                    str(datetime.now().time()).split(".")[0]
                ]),
                '--lines', '10',
                '--no-pager'
            ], capture_output=True)
            
            logs = result.stdout.strip()
            if logs:
                print("✅ Последние логи:")
                print(logs)
                return True
            else:
                print("⚠️  Логов за последнее время не найдено")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка чтения логов: {e}")
            return False
    
    def check_directories(self):
        """Проверить существование директорий"""
        print("\n✅ Проверка директорий...")
        
        dirs_to_check = [
            self.install_dir,
            self.config_dir,
            self.state_dir,
            self.log_dir
        ]
        
        all_exist = True
        for dir_path in dirs_to_check:
            if Path(dir_path).exists():
                print(f"✅ {dir_path} существует")
                # Проверить права доступа
                try:
                    os.access(dir_path, os.R_OK | os.W_OK | os.X_OK)
                    print(f"✅   права доступа OK")
                except:
                    print(f"⚠️    права доступа ограничены")
            else:
                print(f"❌ {dir_path} не существует")
                all_exist = False
        
        return all_exist
    
    def check_files(self):
        """Проверить ключевые файлы"""
        print("\n✅ Проверка ключевых файлов...")
        
        files_to_check = [
            f"{self.install_dir}/agent.py",
            f"{self.config_dir}/config.json",
            f"{self.install_dir}/requirements.txt",
            f"{self.install_dir}/setup_linux_server.py",
        ]
        
        all_exist = True
        for file_path in files_to_check:
            if Path(file_path).exists():
                print(f"✅ {file_path} существует")
                # Проверить размер
                size = Path(file_path).stat().st_size
                print(f"✅   размер: {size} байт")
            else:
                print(f"❌ {file_path} не найден")
                all_exist = False
        
        return all_exist
    
    def check_permissions(self):
        """Проверить права доступа"""
        print("\n✅ Проверка прав доступа...")
        
        # Проверить права на директории
        dirs_to_check = [
            (self.install_dir, "ouroboros"),
            (self.config_dir, "ouroboros"),
            (self.state_dir, "ouroboros"),
            (self.log_dir, "ouroboros"),
        ]
        
        all_ok = True
        for dir_path, owner in dirs_to_check:
            try:
                stat = Path(dir_path).stat()
                owner_name = self.get_username(stat.st_uid)
                group_name = self.get_groupname(stat.st_gid)
                
                print(f"✅ {dir_path}: владелец {owner_name}:{group_name}")
                
                # Проверить права
                permissions = oct(stat.st_mode)[-3:]
                print(f"✅   права: {permissions}")
                
                if owner_name != owner or group_name != owner:
                    print(f"⚠️    владелец должен быть {owner}")
                    all_ok = False
                    
            except Exception as e:
                print(f"❌ Ошибка проверки {dir_path}: {e}")
                all_ok = False
        
        return all_ok
    
    def get_username(self, uid):
        """Получить имя пользователя по UID"""
        try:
            import pwd
            return pwd.getpwuid(uid).pw_name
        except:
            return str(uid)
    
    def get_groupname(self, gid):
        """Получить имя группы по GID"""
        try:
            import grp
            return grp.getgrgid(gid).gr_name
        except:
            return str(gid)
    
    def check_system_resources(self):
        """Проверить системные ресурсы"""
        print("\n⚙️  Проверка системных ресурсов...")
        
        # Память
        try:
            result = self.run_command(['free', '-h'], capture_output=True)
            print("✅ Память:")
            print(result.stdout)
        except:
            print("❌ Не удалось получить информацию о памяти")
        
        # Диск
        try:
            result = self.run_command(['df', '-h'], capture_output=True)
            print("✅ Диск:")
            print(result.stdout)
        except:
            print("❌ Не удалось получить информацию о диске")
        
        # CPU
        try:
            result = self.run_command(['top', '-b', '-n'1', '-d'1'], 
                                   capture_output=True)
            print("✅ CPU:")
            print(result.stdout.split('\n')[2])  # Третья строка содержит статистику CPU
        except:
            print("❌ Не удалось получить информацию о CPU")
    
    def check_network(self):
        """Проверить сетевое соединение"""
        print("\n⌨️  Проверка сетевого соединения...")
        
        # Проверить доступ к GitHub
        try:
            self.run_command(['ping', '-c1', 'github.com'], 
                           capture_output=True)
            print("✅ Доступ к GitHub есть")
        except:
            print("⚠️  Ограниченный доступ к GitHub")
        
        # Проверить доступ к OpenRouter
        try:
            self.run_command(['ping', '-c1', 'api.openrouter.ai'], 
                           capture_output=True)
            print("✅ Доступ к OpenRouter есть")
        except:
            print("⚠️  Ограниченный доступ к OpenRouter")
    
    def generate_report(self):
        """Сгенерировать отчет о состоянии"""
        print("\n" + "="*50)
        print("📊 ОТЧЕТ О СОСТОЯНИИ СИСТЕМЫ")
        print("="*50)
        
        issues = []
        
        # Проверка сервиса
        if not self.check_service_status():
            issues.append("Сервис не активен")
        
        # Проверка директорий
        if not self.check_directories():
            issues.append("Некоторые директории отсутствуют")
        
        # Проверка файлов
        if not self.check_files():
            issues.append("Некоторые ключевые файлы отсутствуют")
        
        # Проверка прав
        if not self.check_permissions():
            issues.append("Проблемы с правами доступа")
        
        # Проверка логов
        if not self.check_service_logs():
            issues.append("Нет свежих логов сервиса")
        
        # Проверка ресурсов
        self.check_system_resources()
        self.check_network()
        
        print("\n" + "="*50)
        
        if issues:
            print("❌ ОБНАРУЖЕНЫ ПРОБЛЕМЫ:")
            for issue in issues:
                print(f"  - {issue}")
            print("\n⚠️  Рекомендации:")
            print("1. Проверьте логи сервиса: journalctl -u ouroboros -f")
            print("2. Убедитесь, что конфигурация заполнена правильно")
            print("3. Проверьте права доступа к директориям")
        else:
            print("✅ СИСТЕМА В РАБОЧЕМ СОСТОЯНИИ")
            print("🚀 Ouroboros готов к работе!")
        
        print("\n" + "="*50)
    
    def run(self):
        """Запустить проверку"""
        print("\n🔍 Проверка работоспособности Ouroboros...")
        print("=" * 50)
        
        self.check_root()
        
        print("\n✅ Начало проверки...")
        
        # Проверка сервиса
        self.check_service_status()
        
        # Проверка логов
        self.check_service_logs()
        
        # Проверка директорий
        self.check_directories()
        
        # Проверка файлов
        self.check_files()
        
        # Проверка прав
        self.check_permissions()
        
        # Проверка ресурсов
        self.check_system_resources()
        self.check_network()
        
        # Генерация отчета
        self.generate_report()

if __name__ == "__main__":
    checker = ServerHealthChecker()
    checker.run()