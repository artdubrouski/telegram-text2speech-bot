import logging
import os
import time

import aiohttp
import aiogram
import asyncio
import environ
import slugify

from aiogram import Bot, Dispatcher, executor, types
from converters import convert_audio_format, text_to_speech, url_to_name
from exrtactors import url_extractor, humanize_urls_in_text, is_url
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


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Send me url or text, I'll send audio back")


queue = asyncio.PriorityQueue()


async def answering_machine():
    await asyncio.sleep(0.5)
    while not queue.empty():
        _, msg, fname = await queue.get()
        await msg.answer_audio(open(fname, 'rb'))
        queue.task_done()
        try:
            os.remove(fname)
        except os.error:
            pass

@dp.message_handler(content_types=["text", "photo", "video", "audio", "animation"])
async def extract(msg: types.Message):
    msg_time = time.time()
    msg_text = msg.text
    if not isinstance(msg_text, str):
        msg_text = msg.caption
        if not isinstance(msg_text, str):
            await msg.answer("Text/URL not found")
            return
    if await is_url(msg_text):
        clean = await url_extractor(msg_text)
        name = await url_to_name(msg.text)
    else:
        clean = await humanize_urls_in_text(msg_text)
        name = slugify.slugify(msg_text[:16])
    text_converted = await text_to_speech(clean, name)
    if text_converted is not True:
        await msg.answer(text_converted)
        return
    audio_converted = await convert_audio_format(name)
    if audio_converted is not True:
        await msg.answer(audio_converted)
        return
    try:
        os.remove(f'media/{name}.aiff')
        os.remove(f'media/{name}.txt')
    except os.error:
        pass
    fname = f'media/{name}.mp3'
    await queue.put((msg_time, msg, fname))
    if queue.qsize() == 1:
        await answering_machine()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
