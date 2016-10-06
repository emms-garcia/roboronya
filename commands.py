# -*- coding: utf-8 -*-
import random
import os
import uuid

import giphypop
import requests

import config
from roboronya import Roboronya
from utils import create_path_if_not_exists


"""
    Helpers for the commands.
"""

COMMAND_HELP = {
    'gif': (
        'Searches for a gif (from Giphy) that matches the words '
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
    ),
    'gfycat': (
        'Searches for a gif (from Gfycat) that matches the words '
        'following the command. *i. e. /gfycat dog*. Unlike /gif '
        'this command ensures gifs are under 2MB, so they should '
        'be relatively fast.'
    ),
    'magicball': (
        'Ask Roboronya for advice. She knows more than she tells.'
    ),
    'caracola': (
        'Alias for */magicball*.'
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
            print(
                'Failed to execute command: {}. '
                'Error: {}.'.format(
                    kwargs['command_name'],
                    e,
                )
            )
            Roboronya._send_response(
                conv,
                error_message,
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
                (
                    'Sorry {user_fullname}, the /{command_name} '
                    'command requires arguments to work.'
                ),
                **kwargs
            )
            return
        return fn(conv, message, cmd_args, **kwargs)
    return wrapper


def _send_file(conv, media_url, **kwargs):
    """
    Send a file to the conversation.
    """
    response = requests.get(media_url)
    file_path = '{}.{}'.format(
        os.path.join(
            config.IMAGES_DIR,
            str(uuid.uuid4())
        ),
        '.gif',
    )

    create_path_if_not_exists(file_path)
    with open(file_path, 'wb+') as img:
        img.write(response.content)

    Roboronya._send_response(
        conv,
        'Here\'s your gif {user_fullname}.',
        image_file=open(file_path, 'rb+'),
        **kwargs
    )


"""
    Implemented commands. Any /command_name found in message (and
    arguments) will be redirected here. Parameters are (in order):
    - conv: hangups.conversation.Conversation object.
    - message: original string message that triggered the command.
    - cmd_args (optional): arguments given for the command, or
    in other words any following words written after the command.
"""


class Commands(object):

    @staticmethod
    @_log_command
    @_failsafe
    def help(conv, message, cmd_args, **kwargs):
        """
        /gif command. Should send the first gif found from an API
        (probably giphy) that matches the argument words.
        """
        Roboronya._send_response(
            conv, '\n'.join([
                '**/{}**: {}'.format(cmd_name, help_message)
                for cmd_name, help_message in COMMAND_HELP.items()
            ]), **kwargs
        )

    @staticmethod
    @_requires_args
    @_log_command
    @_failsafe
    def gif(conv, message, cmd_args, **kwargs):
        """
        /gif command. Translates commands argument words as
        gifs using giphy.
        """
        giphy_image = giphypop.translate(phrase=' '.join(cmd_args))
        size_in_mb = giphy_image.filesize * 1e-6
        print('GIF Size In MB => ', size_in_mb)
        if size_in_mb > config.MAX_GIF_SIZE_IN_MB:
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
            _send_file(conv, giphy_image.media_url, **kwargs)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    @_log_command
    @_failsafe
    def magicball(conv, message, cmd_args, **kwargs):
        """
        /magicball command: Randomly answer like a magic ball.
        """
        answers = [
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
            'Reply hazy try again {user_fullname}',
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

        Roboronya._send_response(
            conv,
            random.choice(answers),
            **kwargs
        )

    def caracola(*args, **kwargs):
        """
        /caracola command: Alias for magicball.
        """
        Commands.magicball(*args, **kwargs)

    @staticmethod
    @_requires_args
    @_log_command
    @_failsafe
    def gfycat(conv, message, cmd_args, **kwargs):
        response = requests.get(
            config.GIFYCAT_SEARCH_URL,
            params={'search_text': ' '.join(cmd_args)}
        )
        response_json = response.json()
        for gfycat_json in response_json.get('gfycats'):
            if gfycat_json.get('max2mbGif'):
                _send_file(conv, gfycat_json['max2mbGif'], **kwargs)
                break
