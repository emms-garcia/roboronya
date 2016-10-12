from bs4 import BeautifulSoup

import random
import requests

from roboronya import config
from roboronya.exceptions import CommandValidationException
from roboronya.utils import get_logger

def is_invalid_alias(alias):
    if len(alias) > config.MAX_ALIAS_LENGTH:
        return 'Sorry {user_fullname}, that alias is too long.'
    if len(alias) < 3:
        return 'Sorry {user_fullname}, that alias is too short.'
    return None

def requires_args(fn):
    """
    Decorator to validate commands that require arguments.
    """
    def wrapper(roboronya, conv, cmd_args, **kwargs):
        if not cmd_args:
            raise CommandValidationException(
                'Sorry {user_fullname}, the /{command_name} '
                'command requires arguments to work.'
                )
        return fn(roboronya, conv, cmd_args, **kwargs)
    return wrapper

def get_gif_url(keywords):
    """
    Get an URL to a gif, given some keywords.
    """
    response_json = requests.get(
        config.GIFYCAT_SEARCH_URL,
        params={'search_text': ' '.join(keywords)}
        ).json()
    gfycats = response_json.get('gfycats', [])
    if gfycats:
        gfycat_json = random.choice(gfycats)
        return gfycat_json['max2mbGif']
    return None

logger = get_logger(__name__)

class Plugin(object):

    def requires_args(fn):
        """                                                                                                                                                        
        Decorator to validate commands that require arguments.                                                                                                     
        """
        def wrapper(roboronya, conv, cmd_args, **kwargs):
            if not cmd_args:
                raise CommandValidationException(
                    'Sorry {user_fullname}, the /{command_name} '
                    'command requires arguments to work.'
                    )
            return fn(roboronya, conv, cmd_args, **kwargs)
        return wrapper

    def get_gif_url(keywords):
        """
        Get an URL to a gif, given some keywords.
        """
        response_json = requests.get(
            config.GIFYCAT_SEARCH_URL,
            params={'search_text': ' '.join(keywords)}
            ).json()
        gfycats = response_json.get('gfycats', [])
        if gfycats:
            gfycat_json = random.choice(gfycats)
            return gfycat_json['max2mbGif']
        return None

    @staticmethod
    def run(roboronya, conv, cmd_args, **kwargs):
        pass
