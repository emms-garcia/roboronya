from bs4 import BeautifulSoup

import random
import requests

from roboronya import config
from roboronya.exceptions import CommandValidationException
from roboronya.utils import get_logger

class Plugin(object):

    logger = get_logger(__name__)

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
