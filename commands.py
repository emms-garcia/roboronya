# -*- coding: utf-8 -*-
import random
import os
import uuid

import giphypop
import requests


from roboronya import Roboronya


"""
    Helpers for the commands.
"""

COMMAND_HELP = {
    'gif': (
        'Searches for a gif that matches the words '
        'following the command. *i. e. /gif cat*'
    ),
    'cointoss': (
        'Randomly toss a coin. 50-50 chances.'
    ),
    'ping': (
        'Check if bot is online. Should always work.'
    ),
    'love': (
        'From Roboronya with love.'
    )
}


def _failsafe(fn):
    """
    Sends a message in case of command failure.
    """
    error_message = (
        'Sorry {user_fullname} I failed to process '
        'your command: "{original_message}".'
    )

    def wrapper(conv, message, cmd_args, **kwargs):
        try:
            return fn(conv, message, cmd_args, **kwargs)
        except Exception as e:
            print(e)
            Roboronya._send_response(
                conv,
                [{'text': error_message}],
                **kwargs
            )
    return wrapper


def _log_command(fn):
    """
        Decorator to log running command data.
    """
    def wrapper(conv, message, cmd_args, **kwargs):
        print(
            'Running /{} command with arguments: [{}].'.format(
                kwargs['command_name'],
                ', '.join(cmd_args)
            )
        )
        return fn(conv, message, cmd_args, **kwargs)
    return wrapper


def _requires_args(fn):
    """
        Decorator to validate commands that require arguments.
    """
    def wrapper(conv, message, cmd_args, **kwargs):
        if not cmd_args:
            print(
                'The command /{} requires arguments to work.'.format(
                    kwargs['command_name']
                )
            )
            Roboronya._send_response(
                conv,
                [{
                    'text': (
                        'Sorry {user_fullname}, the /{command_name} '
                        'command requires arguments to work.'
                    )
                }],
                **kwargs
            )
            return
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


@_failsafe
def help(conv, message, cmd_args, **kwargs):
    """
    /gif command. Should send the first gif found from an API
    (probably giphy) that matches the argument words.
    """
    response = []
    for cmd_name, help_message in COMMAND_HELP.items():
        response.append(
            '**/{}**: {}'.format(cmd_name, help_message)
        )

    Roboronya._send_response(
        conv, '\n'.join(response), **kwargs
    )


@_log_command
@_requires_args
@_failsafe
def gif(conv, message, cmd_args, **kwargs):
    """
    /gif command. Translates commands argument words as
    gifs using giphy.
    """
    giphy_image = giphypop.translate(phrase=' '.join(cmd_args))
    MAX_GIF_SIZE_IN_MB = int(os.environ.get('ROBORONYA_MAX_GIF_SIZE', '5'))
    size_in_mb = giphy_image.filesize * 1e-6
    print('GIF Size In MB => ', size_in_mb)
    if size_in_mb > MAX_GIF_SIZE_IN_MB:
        kwargs['gif_url'] = giphy_image.bitly
        Roboronya._send_response(
            conv,
            (
                'Sorry {user_fullname} gif is too large. '
                'Here\'s the link instead: {gif_url}'
            ),
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
            'Here\'s your gif {user_fullname}.',
            image_file=open(file_path, 'rb+'),
            **kwargs
        )


@_log_command
@_failsafe
def love(conv, message, cmd_args, **kwargs):
    """
    /love command. From Robornya with love.
    """
    Roboronya._send_response(
        conv,
        'I love you {user_fullname} <3.',
        **kwargs
    )


@_log_command
@_failsafe
def cointoss(conv, message, cmd_args, **kwargs):
    """
    /cointoss command. Tosses a coin to make a decision as gods should,
    based on luck.
    """
    Roboronya._send_response(
        conv,
        'heads' if random.getrandbits(1) == 0 else 'tails',
        **kwargs
    )


@_log_command
@_failsafe
def ping(conv, message, cmd_args, **kwargs):
    """
    /ping command. Check bot status.
    """
    Roboronya._send_response(
        conv,
        '**Pong!**',
        **kwargs
    )
