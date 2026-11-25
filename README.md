# Telegram Voice-to-Text Bot 🎙️

Telegram бот для конвертации голосовых сообщений в текст с использованием Groq API (Whisper Large V3 Turbo).

## Возможности

- 🎯 Распознавание голосовых сообщений любой длины
- 🌍 Автоматическое определение языка (50+ языков)
- ✍️ Автоматическая пунктуация и форматирование текста
- ⚡️ Очень быстрая обработка (Groq infrastructure)
- ⏱ Показ прогресса обработки
- 🆓 Бесплатное использование (14,400 запросов/день на Groq)
- 🆓 Бесплатное развертывание на Render.com

## Требования

- Python 3.9+
- Telegram Bot Token (получить у [@BotFather](https://t.me/botfather))
- Groq API Key (бесплатная регистрация на [console.groq.com](https://console.groq.com))
- GitHub аккаунт (для деплоя на Render.com)

## Локальная установка

### 1. Клонирование репозитория

```bash
git clone <your-repo-url>
cd tg-rashivrovka
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` и заполните необходимые значения:

```env
BOT_TOKEN=your_telegram_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
USE_WEBHOOK=false
ENVIRONMENT=development
```

### 5. Запуск бота локально

```bash
python bot.py
```

## Получение Groq API ключа

Groq предоставляет бесплатный доступ к Whisper API с очень быстрой обработкой.

### Шаг 1: Регистрация на Groq

1. Перейдите на [console.groq.com](https://console.groq.com)
2. Зарегистрируйтесь используя Google, GitHub или email
3. Подтвердите email если требуется

### Шаг 2: Создание API ключа

1. В консоли Groq перейдите в раздел **"API Keys"**
2. Нажмите **"Create API Key"**
3. Укажите имя ключа (например, `telegram-bot`)
4. Скопируйте созданный API ключ
5. **Важно:** Сохраните ключ сразу — он показывается только один раз!

### Преимущества Groq Whisper:

- ⚡️ **Очень быстрая обработка** — в 10-20 раз быстрее обычного Whisper
- 🆓 **Бесплатный tier** — 14,400 запросов в день (достаточно для большинства ботов)
- 🌍 **Автоопределение языка** — поддерживает 50+ языков
- 🎯 **Высокое качество** — использует Whisper Large V3 Turbo
- 📝 **Автоматическая пунктуация** — модель добавляет знаки препинания

## Деплой на Render.com

### Шаг 1: Подготовка репозитория

Убедитесь, что весь код закоммичен в GitHub:

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Шаг 2: Создание веб-сервиса на Render

1. Перейдите на [render.com](https://render.com) и войдите
2. Нажмите "New" → "Web Service"
3. Подключите ваш GitHub репозиторий
4. Настройте сервис:
   - **Name**: tg-voice-bot (или любое другое имя)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Plan**: Free

### Шаг 3: Настройка переменных окружения

В разделе "Environment" добавьте:

```
BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
WEBHOOK_URL=https://your-app-name.onrender.com
USE_WEBHOOK=true
ENVIRONMENT=production
```

### Шаг 4: Деплой

1. Нажмите "Create Web Service"
2. Дождитесь завершения деплоя
3. Проверьте логи на наличие ошибок

### Шаг 5: Тестирование

Отправьте боту команду `/start` и голосовое сообщение для проверки работы.

## Команды бота

- `/start` - Начать работу с ботом
- `/help` - Получить справку по использованию

## Архитектура

```
bot.py              # Основной файл с handlers
config.py           # Конфигурация и переменные окружения
speech_service.py   # Интеграция с Groq Whisper API
utils.py            # Вспомогательные функции
requirements.txt    # Python зависимости
render.yaml         # Конфигурация Render.com (будет добавлен)
```

## Troubleshooting

### Бот не отвечает на команды

- Проверьте правильность BOT_TOKEN
- Убедитесь, что бот запущен
- Проверьте логи на наличие ошибок

### Ошибки при распознавании голоса

- Проверьте правильность GROQ_API_KEY
- Убедитесь, что не превышен дневной лимит (14,400 запросов)
- Проверьте качество аудио записи

### Проблемы с деплоем на Render

- Убедитесь, что все переменные окружения заданы
- Проверьте логи деплоя в Render dashboard
- Убедитесь, что USE_WEBHOOK=true в продакшене

## Лицензия

MIT

## Поддержка

Если возникли вопросы или проблемы, создайте issue в репозитории.
