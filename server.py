import logging
import os

import aiohttp
import aiogram
import environ
import slugify

from aiogram import Bot, Dispatcher, executor, types
from converter import text_to_speech, convert_audio_format, url_to_name
from exrtactor import url_extractor
from middlewares import AccessMiddleware

env = environ.Env()
env.read_env(".env")

logging.basicConfig(level=logging.INFO)

API_TOKEN = env.str('TG_API_TOKEN')
ACCESS_ID = env.str('TG_ACCESS_ID')
# PROXY_URL = env.str('TG_PROXY')


# bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler()
async def extract(msg: types.Message):
    clean = await url_extractor(msg.text)
    name = url_to_name(msg.text)
    text_to_speech(clean, name)
    if convert_audio_format(name):
        os.remove(f'media/{name}.aiff')
        fname = f'media/{name}.mp3'
        await msg.answer_audio(open(fname, 'rb'))
    os.remove(fname)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)