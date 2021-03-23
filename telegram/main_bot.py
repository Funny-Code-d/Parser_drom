from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN
import asyncio


loop = asyncio.get_event_loop()
bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())


if __name__ == "__main__":
    from handlers import dp, send_to_admin
    from handlers import send_to_admin_exit
    executor.start_polling(dp, on_startup=send_to_admin, on_shutdown=send_to_admin_exit)