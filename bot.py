"""Telegram bot with Google Sheets analytics."""

import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from analytics import Analytics

# Load environment variables
load_dotenv()

# Initialize bot and dispatcher
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
analytics = Analytics()


@dp.message(Command('start'))
async def start(message: types.Message):
    """Handle /start command."""
    analytics.log(
        message.from_user.id,
        message.from_user.username,
        'start'
    )
    await message.answer(
        '👋 Привет! Бот запущен.\n\n'
        'Команды:\n'
        '/help - помощь\n'
        '/stats - статистика'
    )


@dp.message(Command('help'))
async def help_cmd(message: types.Message):
    """Handle /help command."""
    analytics.log(
        message.from_user.id,
        message.from_user.username,
        'help'
    )
    await message.answer(
        '📚 Помощь по боту\n\n'
        'Это пример бота с аналитикой в Google Sheets.\n'
        'Все твои действия логируются для анализа воронки.'
    )


@dp.message(Command('stats'))
async def stats_cmd(message: types.Message):
    """Handle /stats command."""
    analytics.log(
        message.from_user.id,
        message.from_user.username,
        'stats'
    )
    await message.answer(
        '📊 Смотри статистику в Google Sheets!\n\n'
        f'Твой ID: {message.from_user.id}'
    )


@dp.message()
async def echo(message: types.Message):
    """Handle all other messages."""
    analytics.log(
        message.from_user.id,
        message.from_user.username,
        'message',
        message.text[:50] if message.text else 'non-text'
    )
    await message.answer(f'Получил: {message.text}')


async def main():
    """Start the bot."""
    print('Bot started...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())