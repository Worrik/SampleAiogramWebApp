import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import set_webhook, start_webhook
from aiohttp import web
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request


API_TOKEN = '1760965869:AAHUGqcB1crXsZM6BK6wEWh91do-VLsixGg'

# webhook settings
WEBHOOK_HOST = 'https://7b72-78-26-243-122.ngrok.io'
WEBHOOK_PATH = '/api'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 8080

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler()
async def echo(message: types.Message):
    await bot.set_chat_menu_button(
        message.chat.id,
        types.MenuButtonWebApp(
            text="Exaple",
            web_app=types.WebAppInfo(
                url=f"{WEBHOOK_HOST}/test"
            )
        )
    )
    await bot.send_message(
        text="Hello, world!",
        chat_id=message.chat.id,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[
                types.InlineKeyboardButton(
                    text="Example",
                    web_app=types.WebAppInfo(
                        url=f"{WEBHOOK_HOST}/test"
                    )
                )
            ]]
        )
    )


async def on_startup(_):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')

async def handler(request: Request):
    return FileResponse("test.html")


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/test', handler)])
    executor = set_webhook(
        dp,
        WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        web_app=app
    )
    executor.run_app()

