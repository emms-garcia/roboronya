import random
import os
import uuid

import giphypop
import requests


from roboronya import Roboronya


def _log_command(fn):
    def wrapper(conv, message, cmd_args, **kwargs):
        print(
            'Running /{} command with arguments: [{}].'.format(
                kwargs['command_name'],
                ', '.join(cmd_args)
            )
        )
        return fn(conv, message, cmd_args, **kwargs)
    return wrapper


"""
    Implemented commands. Any /command_name found in message (and
    arguments) will be redirected here. Parameters are (in order):
    - conv: hangups.conversation.Conversation object.
    - message: original string message that triggered the command.
    - cmd_args (optional): arguments given for the command, or
    in other words any following words written after the command.
"""


@_log_command
def gif(conv, message, cmd_args, **kwargs):
    """
    /gif command. Should send the first gif found from an API
    (probably giphy) that matches the argument words.
    """

    giphy_image = giphypop.translate(phrase=' '.join(cmd_args))
    MAX_GIF_SIZE_IN_MB = 5
    size_in_mb = giphy_image.filesize * 1e-6
    print('GIF Size In MB => ', size_in_mb)
    if size_in_mb > MAX_GIF_SIZE_IN_MB:
        kwargs['gif_url'] = giphy_image.bitly
        Roboronya._send_response(
            conv,
            [{
                'text': (
                    'Sorry {user_fullname} gif is too large. '
                    'Here\'s the link instead: '
                )
            }, {
                'text': '{gif_url}',
                'url': giphy_image.bitly,
            }],
            **kwargs
        )
    else:
        response = requests.get(giphy_image.media_url)
        file_path = '{}.{}'.format(
            os.path.join('images', str(uuid.uuid4())),
            '.gif',
        )
        with open(file_path, 'wb+') as img:
            img.write(response.content)

        Roboronya._send_response(
            conv,
            [{
                'text': 'Here\'s your gif {user_fullname}.'
            }],
            image_file=open(file_path, 'rb+'),
            **kwargs
        )


@_log_command
def love(conv, message, cmd_args, **kwargs):
    """
    /love command. From Robornya with love.
    """
    Roboronya._send_response(
        conv,
        [{
            'text': 'I love you {user_fullname} <3.'
        }],
        **kwargs
    )


@_log_command
def cointoss(conv, message, cmd_args, **kwargs):
    """
    /cointoss command. Tosses a coin to make a decision as gods should,
    based on luck.
    """
    Roboronya._send_response(
        conv,
        [{
            'text': 'heads' if random.getrandbits(1) == 0 else 'tails'
        }],
        **kwargs
    )
