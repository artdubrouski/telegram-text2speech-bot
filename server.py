import logging
import os

import aiogram
import asyncio
import settings

from converters import convert_audio_format, text_to_speech
from helpers import (
    clean_files,
    is_valid_clean_text,
    is_valid_conversion_result,
    get_clean_text_with_fname,
    get_validated_msg_text,
    queue_task,
)
from middlewares import AccessMiddleware


bot = aiogram.Bot(token=settings.API_TOKEN)
dp = aiogram.Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(settings.ACCESS_ID))  # your TG ID

logger = logging.getLogger('article_bot')
file_handler = logging.FileHandler('logs.log')
formatter = logging.Formatter('%(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

queue = asyncio.PriorityQueue()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: aiogram.types.message.Message) -> None:
    '''Welcome msg from bot on first use.'''
    await message.answer('Send me URL or text, get audio back')


async def answering_machine() -> None:
    '''
    Internal msg handler, gets messages from the queue and sends them out.
    '''
    await asyncio.sleep(0.5)  # preserving message order

    while not queue.empty():
        _, msg, fname = await queue.get()

        await msg.answer_audio(open(fname, 'rb'))
        logger.info(f'{fname} OK')
        queue.task_done()

        try:
            os.remove(fname)
        except os.error as err:
            logger.warning(err)


@dp.message_handler(content_types=aiogram.types.ContentType.ANY)
async def handle_user_msg(msg: aiogram.types.message.Message) -> None:
    '''
    Entry point for all the messages from user.
    Handles extraction and conversion flow.
    '''
    msg_text = await get_validated_msg_text(msg)
    if msg_text is None:
        return
    
    clean, name = await get_clean_text_with_fname(msg, msg_text)

    if not await is_valid_clean_text(msg, clean, name):
        return

    text_converted = await text_to_speech(clean, name)

    if not await is_valid_conversion_result(msg, text_converted):
        return

    audio_converted = await convert_audio_format(name)

    if not await is_valid_conversion_result(msg, audio_converted):
        return

    await clean_files(name)

    await queue_task(msg, name, queue)

    if queue.qsize() == 1:  # keep messages in order
        await answering_machine()


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
