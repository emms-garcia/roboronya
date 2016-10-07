# -*- coding: utf-8 -*-
import random

import giphypop
import requests

from config import GIFYCAT_SEARCH_URL, MAX_GIF_SIZE_IN_MB
import roboronya

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

    def wrapper(conv, cmd_args, **kwargs):
        try:
            return fn(conv, cmd_args, **kwargs)
        except Exception as e:
            print(
                'Failed to execute command: {}. '
                'Error: {}.'.format(
                    kwargs['command_name'],
                    e
                )
            )
            roboronya.Roboronya._send_response(
                conv,
                error_message,
                **kwargs
            )
    return wrapper


def _log_command(fn):
    """
        Decorator to log running command data.
    """
    def wrapper(conv, cmd_args, **kwargs):
        print(
            'Running /{} command with arguments: [{}].'.format(
                kwargs['command_name'],
                ', '.join(cmd_args)
            )
        )
        return fn(conv, cmd_args, **kwargs)
    return wrapper


def _requires_args(fn):
    """
        Decorator to validate commands that require arguments.
    """
    def wrapper(conv, cmd_args, **kwargs):
        if not cmd_args:
            print(
                'The command /{} requires arguments to work.'.format(
                    kwargs['command_name']
                )
            )
            roboronya.Roboronya._send_response(
                conv,
                (
                    'Sorry {user_fullname}, the /{command_name} '
                    'command requires arguments to work.'
                ),
                **kwargs
            )
            return
        return fn(conv, cmd_args, **kwargs)
    return wrapper


"""
    Implemented commands. Any /command_name found in a message (and
    arguments) will be redirected here. Parameters are (in order):
    - conv: hangups.conversation.Conversation object.
    - cmd_args (optional): arguments given for the command, or
    in other words any following words written after the command.
"""


class Commands(object):

    @staticmethod
    @_log_command
    @_failsafe
    def help(conv, cmd_args, **kwargs):
        """
        /gif command. Should send the first gif found from an API
        (probably giphy) that matches the argument words.
        """
        roboronya.Roboronya._send_response(
            conv, '\n'.join([
                '**/{}**: {}'.format(cmd_name, help_message)
                for cmd_name, help_message in COMMAND_HELP.items()
            ]),
            **kwargs
        )

    @staticmethod
    @_requires_args
    @_log_command
    @_failsafe
    def gif(conv, cmd_args, **kwargs):
        """
        /gif command. Translates commands argument words as
        gifs using giphy.
        """
        giphy_image = giphypop.translate(phrase=' '.join(cmd_args))
        size_in_mb = giphy_image.filesize * 1e-6
        print('GIF Size In MB => ', size_in_mb)
        if size_in_mb > MAX_GIF_SIZE_IN_MB:
            kwargs['gif_url'] = giphy_image.bitly
            roboronya.Roboronya._send_response(
                conv,
                (
                    'Sorry {user_fullname} gif is too large. '
                    'Here\'s the link instead: {gif_url}'
                ),
                **kwargs
            )
        else:
            roboronya.Roboronya._send_file(
                conv,
                giphy_image.media_url,
                **kwargs
            )

    @staticmethod
    @_log_command
    @_failsafe
    def love(conv, cmd_args, **kwargs):
        """
        /love command. From Robornya with love.
        """
        roboronya.Roboronya._send_response(
            conv,
            'I love you {user_fullname} <3.',
            **kwargs
        )

    @staticmethod
    @_log_command
    @_failsafe
    def cointoss(conv, cmd_args, **kwargs):
        """
        /cointoss command. Tosses a coin to make a decision as gods should,
        based on luck.
        """
        roboronya.Roboronya._send_response(
            conv,
            'heads' if random.getrandbits(1) == 0 else 'tails',
            **kwargs
        )

    @staticmethod
    @_log_command
    @_failsafe
    def ping(conv, cmd_args, **kwargs):
        """
        /ping command. Check bot status.
        """
        roboronya.Roboronya._send_response(
            conv,
            '**Pong!**',
            **kwargs
        )

    @staticmethod
    @_log_command
    @_failsafe
    def magicball(conv, cmd_args, **kwargs):
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

        roboronya.Roboronya._send_response(
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
    def gfycat(conv, cmd_args, **kwargs):
        """
        /gfycat command: Like the /gif command but instead
        of using giphy it uses gfycat.
        """
        response_json = requests.get(
            GIFYCAT_SEARCH_URL,
            params={'search_text': ' '.join(cmd_args)}
        ).json()
        gfycats = response_json.get('gfycats', [])
        if gfycats:
            gfycat_json = random.choice(gfycats)
            roboronya.Roboronya._send_file(
                conv,
                gfycat_json['max2mbGif'],
                **kwargs
            )
