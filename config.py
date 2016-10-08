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

"""
    Command specific configuration.
"""

"""
    /gif
"""
GIFYCAT_SEARCH_URL = 'https://api.gfycat.com/v1test/gfycats/search'
MAX_GIF_SIZE_IN_MB = int(os.environ.get('ROBORONYA_MAX_GIF_SIZE', '5'))
