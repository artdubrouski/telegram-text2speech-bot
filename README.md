## Telegram text-to-speech and URL article extractor bot.

Currently the bot uses Siri as text-to-speech conversion engine and works on MacOS only.
Not Dockerized.

### The bot accepts:
* Text or any message with text caption. Answers back with mp3.
* URL. Extracts article text with [boilerpy3](https://github.com/jmriebold/BoilerPy3) from the URL and answers with mp3.

All the URLs in text and parsed articles are humanized before text-to-speech conversion:
* *`https://en.wikipedia.org/wiki/Telegram`* will be humanized to *`en.wikipedia.org`*.



# Prerequisites

Make .env file in the source code dir with your bot API_TOKEN.

Optionally you can specify ACCESS_ID. In this case, user with this ID only can use the bot.
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
