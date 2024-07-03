import logging
from aiogram import executor
from loader import dp, bot
from aiogram import types
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data.config import BOT_TOKEN
from aiogram.utils.executor import start_webhook
from aiohttp import web

WEBHOOK_HOST = 'https://marsgame.uz'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}/'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001

logging.basicConfig(level=logging.INFO)

async def on_startup(dispatcher):
    # Birlamchi komandalar (/start va /help)
    await set_default_commands(dispatcher)
    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)
    # Webhookni sozlash
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dispatcher):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')

async def handle(request):
    try:
        update = await request.json()
        await dp.process_update(types.Update(**update))
        return web.Response()
    except Exception as e:
        logging.exception(e)

if __name__ == '__main__':
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
