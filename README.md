# Ouroboros Server Edition

<h1 style="color: #2196F3;">⚡ Ouroboros - Self-Hosted AI Agent</h1>

> 🚀 Полнофункциональная версия Ouroboros для самостоятельного хостинга на Linux серверах

## 📋 Быстрый старт

```bash
# 1. Клонируй репозиторий
git clone git@github.com:groove52/ouroboros.git

# 2. Запустите полную установку
sudo python3 install_complete.py

# 3. Введите API ключи при просьбе
# 4. Ожидайте завершения
```

## 🔧 Особенности

- ✅ Полная автоматическая установка
- ✅ Создание пользователя и директорий
- ✅ Виртуальное окружение
- ✅ Системный сервис (системд)
- ✅ Мониторинг состояния
- ✅ Отчеты о работе
- ✅ Настройка через API
- ✅ Автозапуск сервиса

## 🖥️ Структура директорий

```
/opt/ouroboros/                    # Установка
├── agent.py                 # Основной агент
├── ouroboros/               # Кодовая база
├── venv/                    # Виртуальное окружение
├── requirements.txt         # Зависимости
├── config.json             # Конфигурация
└── install_complete.py      # Скрипт установки

/etc/ouroboros/                    # Конфигурация
├── config.json             # Конфигурация с API ключами
└── ouroboros.service       # Сервис systemd

/var/lib/ouroboros/                # Состояние
├── state.json              # Состояние системы
└── logs/                   # Логи

/var/log/ouroboros/               # Логи
├── chat.jsonl              # История чата
├── events.jsonl            # События
└── progress.jsonl          # Прогресс
```

## 🚀 Быстрая установка

### Вариант 1: Полная автоматическая установка

```bash
# Склонируй репозиторий
git clone git@github.com:groove52/ouroboros.git

# Запустите скрипт установки
sudo python3 install_complete.py

# Следуйте инструкциям на экране
```

### Вариант 2: Пошаговая установка

```bash
# 1. Создайте пользователя 
sudo useradd -r -s /bin/false ouroboros

# 2. Создайте директории
sudo mkdir -p /opt/ouroboros
sudo mkdir -p /etc/ouroboros
sudo mkdir -p /var/lib/ouroboros
sudo mkdir -p /var/log/ouroboros

# 3. Назначьте права
sudo chown -R ouroboros:ouroboros /opt/ouroboros
sudo chown -R ouroboros:ouroboros /etc/ouroboros
sudo chown -R ouroboros:ouroboros /var/lib/ouroboros
sudo chown -R ouroboros:ouroboros /var/log/ouroboros

# 4. Клонируйте репозиторий
sudo -u ouroboros git clone git@github.com:groove52/ouroboros.git /opt/ouroboros/

# 5. Создайте виртуальное окружение
sudo -u ouroboros python3 -m venv /opt/ouroboros/venv

# 6. Установите зависимости
sudo -u ouroboros /opt/ouroboros/venv/bin/pip install -r /opt/ouroboros/requirements.txt

# 7. Создайте конфигурацию
sudo cp /opt/ouroboros/config_example.json /etc/ouroboros/config.json
sudo chown ouroboros:ouroboros /etc/ouroboros/config.json
sudo chmod 600 /etc/ouroboros/config.json

# 8. Создайте сервис
sudo tee /etc/systemd/system/ouroboros.service > /dev/null < < EOF
[Unit]
Description=Ouroboros AI Agent
After=network.target

[Service]
Type=simple
User=ouroboros
Group=ouroboros
WorkingDirectory=/opt/ouroboros
Environment=VIRTUAL_ENV=/opt/ouroboros/venv
Environment=PATH=/opt/ouroboros/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/opt/ouroboros/venv/bin/python -m ouroboros.agent
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# 9. Запустите сервис
sudo systemctl daemon-reload
sudo systemctl start ouroboros
sudo systemctl enable ouroboros
```

## 🔧 Настройка API ключей

### Telegram Bot Token

1. Откройте Telegram
2. Найдите @BotFather
3. Отправьте: `/newbot`
4. Дайте имя и юзернейм боту
5. Скопируйте API токен

### OpenRouter API Key

1. Зарегистрируйтесь на openrouter.ai
2. Перейдите в раздел „API Keys“
3. Нажмите „Create API Key“
4. Скопируйте сгенерированный ключ

### Настройка в конфигурационном файле

```bash
sudo nano /etc/ouroboros/config.json
```

Измените:

```json
{
    "telegram_bot_token": "YOUR_TELEGRAM_TOKEN_HERE",
    "openrouter_api_key": "YOUR_OPENROUTER_KEY_HERE",
    "model": "anthropic/claude-sonnet-4.6",
    "budget_usd": 10.0,
    "log_level": "INFO"
}
```

Сохраните и закройте файл.

## 📊 Управление сервисом

### Основные команды

```bash
# Статус сервиса
sudo systemctl status ouroboros

# Логи сервиса
sudo journalctl -u ouroboros -f

# Перезапуск
sudo systemctl restart ouroboros

# Остановка
sudo systemctl stop ouroboros

# Автозапуск при загрузке
sudo systemctl enable ouroboros

# Отключение автозапуска
sudo systemctl disable ouroboros
```

### Проверка здоровья

```bash
# Проверить установку
sudo python3 check_server_health.py

# Проверить конфигурацию
sudo ls -la /etc/ouroboros/

# Проверить права доступа
sudo ls -la /opt/ouroboros/ | head -10
```

## 🐛 Устранение проблем

### Проблема: Сервис не запускается

```bash
# Проверьте логи
sudo journalctl -u ouroboros -xe

# Проверьте права доступа
sudo ls -la /opt/ouroboros/

# Проверьте конфигурацию
sudo cat /etc/ouroboros/config.json
```

### Проблема: Ошибки API

```bash
# Проверьте конфигурацию
sudo cat /etc/ouroboros/config.json

# Проверьте логи на ошибки
sudo journalctl -u ouroboros -f

# Перезапустите сервис
sudo systemctl restart ouroboros
```

## 📈 Мониторинг

### Логи деятельности

```bash
# Последние 100 строк лого
sudo journalctl -u ouroboros --lines=100 --no-pager

# Логи за последнюю посту часа
sudo journalctl -u ouroboros --since "1 hour ago" --no-pager

# Логи с уровнем ошибок
sudo journalctl -u ouroboros -p err -f
```

### Статистика использования

```bash
# Проверьте расход бюджета
sudo cat /var/lib/ouroboros/state.json | jq .budget

# Проверьте число сообщений
sudo cat /var/lib/ouroboros/state.json | jq .messages

# Проверьте время работы
sudo cat /var/lib/ouroboros/state.json | jq .last_owner_message_at
```

## 🔧 Обновление

### Обновление через Git

```bash
# Перейдите в директорию установки
sudo -u ouroboros -H -s
cd /opt/ouroboros

# Проверьте наличие обновлений
git fetch origin
git status

# Обновите до последней версии
git pull origin main

# Выйдите и перезапустите сервис
sudo systemctl restart ouroboros
exit
```

### Обновление через скрипт

```bash
# Запустите скрипт обновления
sudo python3 update_ouroboros.py
```

## 🎯 Тестирование

### Тестирование Telegram

1. Отправьте боту сообщение `/start`
2. Отправьте `/status` для проверки статуса
3. Отправьте любое сообщение для тестирования

### Тестирование API

```bash
# Проверьте логи на ошибки
sudo journalctl -u ouroboros -f

# Проверьте статус бюджета
sudo cat /var/lib/ouroboros/state.json | jq .budget

# Проверьте соединение с API
sudo journalctl -u ouroboros --since "5 minutes ago" --no-pager
```

## 🔒 Безопасность

### Рекомендации

- ✅ Храните API ключи в безопасном месте
- ✅ Ограничьдоступ к сервису
- ✅ Регулярно меняйте API ключи
- ✅ Мониторите расходы бюджета
- ✅ Следите за логами на ошибки

### Пожарная безопасность

- Используйте прочие пользователя для запуска
- Регулярно обновляйте систему
- Настройте пароль брандмауэра
- Следите за пачками сервера

## 📞 Поддержка

### Полезные ссылки

- [Telegram BotFather](https://t.me/botfather)
- [OpenRouter](https://openrouter.ai)
- [GitHub Repository](https://github.com/groove52/ouroboros)
- [Documentation](https://github.com/groove52/ouroboros/docs)

### Полезные команды

```bash
# Помощь
sudo systemctl status ouroboros

# Логи
sudo journalctl -u ouroboros -f

# Проверка
sudo python3 check_server_health.py

# Обновление
sudo python3 install_complete.py
```

## 🏆 Завершение

Поздравляем! Вы успешно установили Ouroboros на своем сервере.

Начните использовать бота и исследуйте его возможности! 🚀