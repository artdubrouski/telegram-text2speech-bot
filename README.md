## Telegram text-to-speech and URL article extractor bot.

Currently the bot uses Siri as text-to-speech conversion engine and works on MacOS only.
Not Dockerized. Based on [aiogram framework](https://github.com/aiogram/aiogram).

### The bot accepts:
* Text or any message with text caption. Answers back with mp3.
* URL. Extracts article text with [boilerpy3](https://github.com/jmriebold/BoilerPy3) from the URL and answers with mp3.

All the URLs in text and parsed articles are humanized before text-to-speech conversion:
* _`https://www.website.org/1009Zjdj753001`_ will be shortened to _`website.org`_

In the end of every file __EOF_STRING__ added to logically split the audio files in Telegram playlist.
EOF_STRING can be modified in settings.py

When multiple messages received, bot tries to keep the order of messages answered, and basically operates in sync manner despite aiogram being async.


# Prerequisites

Make __.env__ file in the source code dir with your bot __API_TOKEN__.

Optionally you can specify __ACCESS_ID__. In this case, user with this ID only can use the bot.
If not specified, bot is available to everyone.
```
API_TOKEN=your-bot-api-token
ACCESS_ID=your-telegram-id
```

## Install requirements
```
pip install -r requirements.txt
```

# Run bot

```
python3 server.py
```
