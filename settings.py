import logging

import environ


env = environ.Env()
env.read_env(".env")

logging.basicConfig(level=logging.INFO)


API_TOKEN = env.str('TG_API_TOKEN')
ACCESS_ID = env.str('TG_ACCESS_ID')

EOF_STRING = '\n\nEND\n\nOF\n\nFILE \n\n'

BLACKLISTED_WORDS = {
    'app',
    'by',
    'com',
    'http',
    'https',
    'org',
    'ru',
    'www',
}