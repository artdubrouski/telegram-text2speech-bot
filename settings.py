import logging

import environ


env = environ.Env()
env.read_env(".env")

logging.basicConfig(level=logging.INFO)


API_TOKEN = env.str('API_TOKEN')
ACCESS_ID = env.int('ACCESS_ID', 0)  # bot can be used by anyone if not set

EOF_STRING = '\n\nEND\n\nOF\n\nFILE \n\n'
