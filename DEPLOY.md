# 🚀 Инструкция по деплою на Render.com

## ✅ Чеклист перед деплоем

- [ ] Получен токен Telegram бота от @BotFather
- [ ] Получен API ключ Groq на console.groq.com
- [ ] Бот протестирован локально с голосовыми сообщениями
- [ ] Код закоммичен в Git
- [ ] Репозиторий залит на GitHub

## 📋 Шаги деплоя

### 1. Подготовка Git репозитория

```bash
# Инициализируйте Git если еще не сделали
git init

# Добавьте все файлы
git add .

# Создайте коммит
git commit -m "Initial commit: Telegram Voice-to-Text Bot"

# Добавьте remote (замените на ваш URL)
git remote add origin https://github.com/yourusername/tg-rashivrovka.git

# Отправьте код на GitHub
git push -u origin main
```

### 2. Создание проекта на Render.com

1. Перейдите на [render.com](https://render.com)
2. Войдите через GitHub аккаунт
3. Нажмите **"New"** → **"Web Service"**
4. Выберите ваш GitHub репозиторий `tg-rashivrovka`
5. Настройте сервис:
   - **Name**: `tg-voice-bot` (или любое другое)
   - **Region**: Oregon (или ближайший)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Instance Type**: Free

### 3. Настройка переменных окружения

В разделе **"Environment Variables"** добавьте:

| Key | Value | Пример |
|-----|-------|--------|
| `BOT_TOKEN` | Ваш токен бота | `1234567890:ABC...` |
| `GROQ_API_KEY` | Ваш Groq API ключ | `gsk_...` |
| `WEBHOOK_URL` | URL вашего сервиса | `https://tg-voice-bot.onrender.com` |
| `USE_WEBHOOK` | `true` | `true` |
| `ENVIRONMENT` | `production` | `production` |

**Важно:** `WEBHOOK_URL` будет доступен только после создания сервиса. 
Запишите URL и добавьте его в переменные окружения после первого деплоя.

### 4. Первый деплой

1. Нажмите **"Create Web Service"**
2. Дождитесь завершения деплоя (5-10 минут)
3. Проверьте логи на ошибки
4. Скопируйте URL сервиса (например, `https://tg-voice-bot.onrender.com`)
5. Добавьте `WEBHOOK_URL` в Environment Variables
6. Перезапустите сервис

### 5. Настройка Webhook для Telegram

Выполните один раз для установки webhook:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_WEBHOOK_URL>/<YOUR_BOT_TOKEN>"
```

Замените:
- `<YOUR_BOT_TOKEN>` на ваш токен бота
- `<YOUR_WEBHOOK_URL>` на URL вашего Render сервиса

Пример:
```bash
curl -X POST "https://api.telegram.org/bot1234567890:ABC.../setWebhook?url=https://tg-voice-bot.onrender.com/1234567890:ABC..."
```

Проверьте webhook:
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

### 6. Тестирование

1. Откройте вашего бота в Telegram
2. Отправьте команду `/start`
3. Отправьте голосовое сообщение
4. Проверьте что бот распознает речь

## 🔍 Мониторинг и отладка

### Просмотр логов

1. Откройте ваш сервис в Render dashboard
2. Перейдите в раздел **"Logs"**
3. Следите за ошибками в реальном времени

### Частые проблемы

**Бот не отвечает:**
- Проверьте что USE_WEBHOOK=true в продакшене
- Проверьте что webhook установлен (getWebhookInfo)
- Проверьте логи на ошибки

**Ошибки распознавания:**
- Проверьте правильность GROQ_API_KEY
- Проверьте лимиты Groq API (14,400 запросов/день)
- Проверьте логи для деталей ошибки

**Сервис засыпает:**
- Render Free tier засыпает после 15 минут неактивности
- Первый запрос после пробуждения может занять 30-60 секунд
- Для постоянной работы нужен платный план

## 🔄 Обновление кода

```bash
# Внесите изменения в код
git add .
git commit -m "Описание изменений"
git push origin main
```

Render автоматически задеплоит новую версию.

## 💰 Лимиты бесплатного плана

**Render.com:**
- 750 часов работы в месяц
- Сервис засыпает после 15 минут неактивности
- 100 GB исходящего трафика

**Groq API:**
- 14,400 запросов в день
- Достаточно для большинства небольших ботов

## 🆙 Обновление до платного плана

Если бот стал популярным:
- Render: $7/месяц - постоянная работа, больше ресурсов
- Groq: Пока бесплатно для всех, следите за обновлениями

## ✅ Готово!

Ваш бот работает 24/7 и готов распознавать голосовые сообщения! 🎉
