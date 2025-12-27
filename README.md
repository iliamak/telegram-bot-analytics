# Telegram Bot Analytics

Telegram бот с интеграцией Google Sheets для сбора аналитики и построения воронок.

## Возможности

- Логирование событий пользователей в Google Sheets в реальном времени
- Построение воронок и метрик
- Простая интеграция с любым Telegram ботом
- Использует aiogram 3.x

## Установка

1. Клонируй репозиторий:
```bash
git clone https://github.com/iliamak/telegram-bot-analytics.git
cd telegram-bot-analytics
```

2. Установи зависимости:
```bash
pip install -r requirements.txt
```

3. Создай `.env` файл из примера:
```bash
cp .env.example .env
```

4. Заполни `.env`:
- Получи токен бота от [@BotFather](https://t.me/BotFather)
- Создай Google Sheets таблицу
- Добавь URL таблицы в `.env`

5. Настрой Google Service Account:
- Создай Service Account в [Google Cloud Console](https://console.cloud.google.com/)
- Скачай JSON ключ и сохрани как `credentials.json`
- Расшарь таблицу на email из `credentials.json` (поле `client_email`) с правами "Редактор"

## Запуск

```bash
python bot.py
```

## Структура проекта

```
.
├── bot.py              # Основной файл бота
├── analytics.py        # Модуль для работы с Google Sheets
├── requirements.txt    # Зависимости
├── .env.example        # Пример конфигурации
├── .gitignore
└── README.md
```

## Воронки в Google Sheets

Создай второй лист "Funnel" с формулами:

```
A1: Этап              B1: Уникальных юзеров    C1: Conversion %
A2: Start             B2: =COUNTUNIQUE(FILTER(Sheet1!B:B, Sheet1!D:D="start"))
A3: Help              B3: =COUNTUNIQUE(FILTER(Sheet1!B:B, Sheet1!D:D="help"))      C3: =B3/B2*100
A4: Messages          B4: =COUNTUNIQUE(FILTER(Sheet1!B:B, Sheet1!D:D="message"))    C4: =B4/B2*100
```

## Использование в своих ботах

```python
from analytics import Analytics

analytics = Analytics()

# В любом хендлере
@dp.message(Command('start'))
async def start(message: types.Message):
    analytics.log(
        message.from_user.id,
        message.from_user.username,
        'start'
    )
    # ваш код...
```

## License

MIT