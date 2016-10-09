# -*- coding: utf-8 -*-
import os

"""
    General configuration.
"""
CWD = os.path.dirname(os.path.abspath(__file__))

RUNTIME_DIR = os.path.join(CWD, 'runtime')

IMAGES_DIR = os.path.join(RUNTIME_DIR, 'images')
REFRESH_TOKEN_PATH = os.path.join(RUNTIME_DIR, 'refresh_token.txt')

MAX_RECONNECT_RETRIES = 5
MAX_COMMANDS_PER_MESSAGE = 1

"""
    Command specific configuration.
"""

"""
    /gif
"""
GIFYCAT_SEARCH_URL = 'https://api.gfycat.com/v1test/gfycats/search'
MAX_GIF_SIZE_IN_MB = int(os.environ.get('ROBORONYA_MAX_GIF_SIZE', '5'))


"""
    /magicball
"""
MAGICBALL_ANSWERS = [
    'It is certain {user_fullname}',
    'It is decidedly so {user_fullname}',
    'Without a doubt {user_fullname}',
    'Yes {user_fullname}, definitely',
    'You may rely on it {user_fullname}',
    'As I see it, yes {user_fullname}',
    'Most likely {user_fullname}',
    'Outlook good {user_fullname}',
    'Yes {user_fullname}',
    'Signs point to yes {user_fullname}',
    'Reply hazy, try again {user_fullname}',
    'Ask again later {user_fullname}',
    'Better not tell you now {user_fullname}',
    'Cannot predict now {user_fullname}',
    'Concentrate and ask again {user_fullname}',
    'Don\'t count on it {user_fullname}',
    'My reply is no {user_fullname}',
    'My sources say no {user_fullname}',
    'Outlook not so good {user_fullname}',
    'Very doubtful {user_fullname}'
]

"""
    /whatis
"""
URBAN_DICT_URL = 'http://api.urbandictionary.com/v0/define'
URBAN_DICT_RANDOM_URL = 'http://api.urbandictionary.com/v0/random'
