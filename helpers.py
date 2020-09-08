import logging
import os
import time

import asyncio

from typing import Optional, Tuple, Union

import slugify
import settings

from aiogram.types.message import Message
from converters import url_to_name
from exrtactors import extract_text_from_url, humanize_urls_in_text, is_url


logger = logging.getLogger('article_bot')


async def get_validated_msg_text(msg: Message) -> Optional[str]:
    '''
    Returns text/url from the given msg, or None if not found.
    '''
    msg_text = msg.text
    if not isinstance(msg.text, str):
        msg_text = msg.caption
        if not isinstance(msg_text, str):
            await msg.answer('Text/URL not found')
            return None
    return msg_text


async def clean_files(name: str) -> None:
    '''
    Cleans generated text and src_audio files after successful aiff-mp3 conversion.
    '''
    try:
        os.remove(f'media/{name}.aiff')
        os.remove(f'media/{name}.txt')
    except os.error as err:
        logger.warning(err)


async def get_clean_text_with_fname(msg: Message, msg_text: str) -> Tuple[str, str]:
    '''
    Extracts humanized text based on input type with filename for later use.
    '''
    if await is_url(msg_text):
        clean = await extract_text_from_url(msg_text)
        name = await url_to_name(msg.text)
    else:
        clean = await humanize_urls_in_text(msg_text)
        name = slugify.slugify(msg_text[:16])
    return clean, name


async def is_valid_clean_text(msg: Message, clean:str, name: str) -> bool:
    '''Checks if both message text and filename are not empty.'''
    if not name or not clean or clean == settings.EOF_STRING:
        await msg.answer('No text found')
        logger.info(f'No text found @ {msg.text}')
        return False
    return True


async def queue_task(msg: Message, name: str, queue: asyncio.PriorityQueue):
    '''Puts a task in the priority queue based on current time.'''
    msg_time = time.time()
    fname = f'media/{name}.mp3'
    await queue.put((msg_time, msg, fname))


async def is_valid_conversion_result(msg: Message, result: Union[str, bool]) -> bool:
    '''
    If conversion result is success it's True else it's error str.
    On success returns True, otherwise sends user conversion error message.
    '''
    if isinstance(result, str):
        await msg.answer(result)
        return False
    return True
