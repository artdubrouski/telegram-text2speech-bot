import os
import time

import ffmpeg
import langdetect
import settings
import slugify

from typing import Union


async def text_to_speech(text: str, name: str) -> Union[bool, str]:
    '''
    Converts text to aiff with Siri.
    Returns True on success or error string otherwise.
    '''
    lang = langdetect.detect(text)

    with open(f'media/{name}.txt', 'w') as f:
        f.write(text)

    voice = 'Yuri -r 230' if lang == 'ru' else 'Alex'
    cmd = f'say -v {voice} -o media/{name}.aiff -f media/{name}.txt'

    try:
        os.system(cmd)
        return True
    except os.error as err:
        return str(err)


async def convert_audio_format(name) -> Union[bool, str]:
    '''Converts source aiff file to lightweight mp3.'''
    try:
        ffmpeg.input(f'media/{name}.aiff').output(f'media/{name}.mp3', audio_bitrate=32000).run()
        return True
    except ffmpeg.Error as err:
        return str(err)


async def url_to_name(url: str) -> str:
    '''
    Humanizes urls to short domain-only name.
    Returns time-based number as the last resort.
    '''
    slugname = slugify.slugify(url)
    words = slugname.split('-')
    clean_words = []

    for w in words:
        if w.isalpha() and w not in settings.BLACKLISTED_WORDS:
            clean_words.append(w)

    if clean_words:
        if len(clean_words) > 5:
            clean_words = clean_words[:6]
        return '-'.join(clean_words)

    return str(int(time.time() * (10**6)))[8:]
