import os
import time

import ffmpeg
import langdetect
import slugify


def text_to_speech(text, name):
    lang = langdetect.detect(text)
    with open(f'media/{name}.txt', 'w') as f:
        f.write(text)
    voice = 'Yuri' if lang == 'ru' else 'Alex'
    cmd = f'say -v {voice} -o media/{name}.aiff -f media/{name}.txt'
    os.system(cmd)


def convert_audio_format(name):
    try:
        ffmpeg.input(f'media/{name}.aiff').output(f'media/{name}.mp3', audio_bitrate=64).run()
        return True
    except ffmpeg.Error:
        return False

def url_to_name(url):
    slugname = slugify.slugify(url)
    words = slugname.split('-')
    clean_words = []
    blacklist = {'www', 'http', 'https', 'com', 'org', 'app', 'ru'}
    for w in words:
        if w.isalpha() and w not in blacklist:
            clean_words.append(w)
    if clean_words:
        if len(clean_words) > 5:
            clean_words = clean_words[:6]
        return '-'.join(clean_words)
    return str(int(time.time() * (10**6)))[8:]