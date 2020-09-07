import logging
import os
import time

import aiogram
import asyncio
import settings

from converters import convert_audio_format, text_to_speech
from helpers import (
    clean_files,
    clean_text_is_valid,
    get_clean_text_with_fname,
    get_validated_msg_text,
)
from middlewares import AccessMiddleware


bot = aiogram.Bot(token=settings.API_TOKEN)
dp = aiogram.Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(settings.ACCESS_ID))

logger = logging.getLogger('article_bot')
file_handler = logging.FileHandler('logs.log')
formatter = logging.Formatter('%(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: aiogram.types.Message):
    '''Welcome msg from bot on first use.'''
    await message.answer('Send me URL or text, get audio back')


queue = asyncio.PriorityQueue()


async def answering_machine():
    '''
    Internal msg handler, gets messages from the queue and sends them out.
    '''
    await asyncio.sleep(0.5)

    while not queue.empty():
        _, msg, fname = await queue.get()

        await msg.answer_audio(open(fname, 'rb'))
        logger.info(f'{fname} OK')
        queue.task_done()

        try:
            os.remove(fname)
        except os.error as err:
            logger.warning(err)


@dp.message_handler(content_types=['text', 'photo', 'video', 'audio', 'animation'])
async def handle_user_msg(msg: aiogram.types.Message):
    '''
    Entry point for all the messages from user.
    Handles extraction and conversion flow.
    '''
    msg_time = time.time()

    msg_text = await get_validated_msg_text(msg)
    if msg_text is None:
        return
    
    clean, name = await get_clean_text_with_fname(msg, msg_text)

    if not await clean_text_is_valid(msg, clean, name):
        return

    text_converted = await text_to_speech(clean, name)

    if text_converted is not True:  # if error returned
        await msg.answer(str(text_converted))
        return

    audio_converted = await convert_audio_format(name)

    if audio_converted is not True:  # if error returned
        await msg.answer(str(audio_converted))
        return

    await clean_files(name)

    fname = f'media/{name}.mp3'
    await queue.put((msg_time, msg, fname))

    if queue.qsize() == 1:  # keep messages in order
        await answering_machine()


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
