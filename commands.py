# -*- coding: utf-8 -*-
import random

import giphypop
import requests

from config import GIFYCAT_SEARCH_URL, MAX_GIF_SIZE_IN_MB

"""
    Helpers for the commands.
"""

COMMAND_HELP = [
    {
        'name': 'ping',
        'description': 'Check if bot is online. Should always work.'
    },
    {
        'name': 'love',
        'description': 'From Roboronya with love.'
    },
    {
        'name': 'cointoss',
        'description': 'Randomly toss a coin. 50-50 chances.'
    },
    {
        'name': 'magicball',
        'description': (
            'Ask Roboronya for advice. She knows more than she tells.'
        ),
    },
    {
        'name': 'caracola',
        'description': (
            'Alias for */magicball*.'
        )
    },
    {
        'name': 'fastgif',
        'description': 'For faster gifs, this only sends back the gif url.'
    },
    {
        'name': 'gif',
        'description': (
            'Searches for a gif (from Giphy) that matches the words '
            'following the command. *i. e. /gif cat*'
        )
    },
    {
        'name': 'gfycat',
        'description': (
            'Searches for a gif (from Gfycat) that matches the words '
            'following the command. *i. e. /gfycat dog*.'
        ),
    },
    {
        'name': 'cholify',
        'description': (
            'Roboronya will use her *Automated Cholification Algorithm* '
            '(Patent Pending) to translate your text to a more sophisticated'
            ' language.'
        )
    }
]


def _failsafe(fn):
    """
    Sends a message in case of command failure.
    """
    error_message = (
        'Sorry {user_fullname} I failed to process '
        'your command: "{original_message}".'
    )

    def wrapper(roboronya, conv, cmd_args, **kwargs):
        try:
            return fn(roboronya, conv, cmd_args, **kwargs)
        except Exception as e:
            print(
                'Failed to execute command: {}. '
                'Error: {}.'.format(
                    kwargs['command_name'],
                    e
                )
            )
            roboronya.send_message(
                conv,
                error_message,
                **kwargs
            )
    return wrapper


def _get_gif_url(keywords):
    """
    Get an URL to a gif, given some keywords.
    """
    response_json = requests.get(
        GIFYCAT_SEARCH_URL,
        params={'search_text': ' '.join(keywords)}
    ).json()
    gfycats = response_json.get('gfycats', [])
    if gfycats:
        gfycat_json = random.choice(gfycats)
        return gfycat_json['max2mbGif']
    return None


def _log_command(fn):
    """
        Decorator to log running command data.
    """
    def wrapper(roboronya, conv, cmd_args, **kwargs):
        print(
            'Running /{} command with arguments: [{}].'.format(
                kwargs['command_name'],
                ', '.join(cmd_args)
            )
        )
        return fn(roboronya, conv, cmd_args, **kwargs)
    return wrapper


def _requires_args(fn):
    """
        Decorator to validate commands that require arguments.
    """
    def wrapper(roboronya, conv, cmd_args, **kwargs):
        if not cmd_args:
            print(
                'The command /{} requires arguments to work.'.format(
                    kwargs['command_name']
                )
            )
            roboronya.send_message(
                conv,
                (
                    'Sorry {user_fullname}, the /{command_name} '
                    'command requires arguments to work.'
                ),
                **kwargs
            )
            return
        return fn(roboronya, conv, cmd_args, **kwargs)
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
    def help(roboronya, conv, cmd_args, **kwargs):
        """
        /help command. Shows the available commands.
        """
        roboronya.send_message(
            conv, '\n'.join([
                '**/{}**: {}'.format(command['name'], command['description'])
                for command in COMMAND_HELP
            ]),
            **kwargs
        )

    @staticmethod
    @_requires_args
    @_log_command
    @_failsafe
    def gif(roboronya, conv, cmd_args, **kwargs):
        """
        /gif command. Translates commands argument words as
        gifs using giphy.
        """
        giphy_image = giphypop.translate(phrase=' '.join(cmd_args))
        if giphy_image:
            size_in_mb = giphy_image.filesize * 1e-6
            if size_in_mb > MAX_GIF_SIZE_IN_MB:
                kwargs['gif_url'] = giphy_image.bitly
                roboronya.send_message(
                    conv,
                    (
                        'Sorry {user_fullname} gif is too large. '
                        'Here\'s the link instead: {gif_url}'
                    ),
                    **kwargs
                )
            else:
                kwargs['file_extension'] = 'gif'
                roboronya.send_file(
                    conv,
                    'Here\'s your gif {user_fullname}.',
                    giphy_image.media_url,
                    **kwargs
                )
        else:
            print(
                'Could not not find a gif for keywords: '
                '{}'.format(cmd_args)
            )
            kwargs['cmd_args'] = cmd_args
            roboronya.send_message(
                conv,
                (
                    'Sorry {user_fullname} I could not find '
                    'a gif for your keywords: {cmd_args}.'
                ),
                **kwargs
            )

    @staticmethod
    @_requires_args
    @_log_command
    @_failsafe
    def fastgif(roboronya, conv, cmd_args, **kwargs):
        """
        /fastgif command. Searches for a gif and sends the url.
        """
        kwargs['gif_url'] = _get_gif_url(cmd_args)
        roboronya.send_message(
            conv,
            (
                'Here is your URL to the gif {user_fullname}: '
                '{gif_url} ... love you btw'
            ),
            **kwargs
        )

    @staticmethod
    @_log_command
    @_failsafe
    def love(roboronya, conv, cmd_args, **kwargs):
        """
        /love command. From Robornya with love.
        """
        roboronya.send_message(
            conv,
            'I love you {user_fullname} <3.',
            **kwargs
        )

    @staticmethod
    @_log_command
    @_failsafe
    def cointoss(roboronya, conv, cmd_args, **kwargs):
        """
        /cointoss command. Tosses a coin to make a decision as gods should,
        based on luck.
        """
        roboronya.send_message(
            conv,
            'heads' if random.getrandbits(1) == 0 else 'tails',
            **kwargs
        )

    @staticmethod
    @_log_command
    @_failsafe
    def ping(roboronya, conv, cmd_args, **kwargs):
        """
        /ping command. Check bot status.
        """
        roboronya.send_message(
            conv,
            '**Pong!**',
            **kwargs
        )

    @staticmethod
    @_log_command
    @_failsafe
    def magicball(roboronya, conv, cmd_args, **kwargs):
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

        roboronya.send_message(
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
    @_log_command
    @_failsafe
    def cholify(roboronya, conv, cmd_args, **kwargs):

        def _cholify(words):
            choloWords = []
            for word in words:
                choloWord = ''
                oldChar = ''
                for char in word.lower():
                    if char == 'y':
                        choloWord += 'ii'
                    elif char == 't':
                        choloWord += 'th'
                    elif char == 'u' and (oldChar == 'q'):
                        choloWord += random.choice(['kh', 'k'])
                    elif (char == 'i' or char == 'e') and oldChar == 'c':
                        choloWord = choloWord[:-1]
                        choloWord += random.choice(['s', 'z']) + char
                    elif char == 'h' and oldChar == 'c':
                        choloWord = choloWord[:-1]
                        choloWord += random.choice(['zh', 'sh'])
                    elif char == 'c':
                        choloWord += 'k'
                    elif char == 's':
                        choloWord += 'z'
                    elif char == 'v':
                        choloWord += 'b'
                    elif char == 'b':
                        choloWord += 'v'
                    elif char == 'q':
                        pass
                    else:
                        choloWord += char
                    oldChar = char
                choloWords.append(choloWord)
            return choloWords

        roboronya.send_message(
            conv,
            ' '.join(_cholify(cmd_args)),
            **kwargs
        )

    @staticmethod
    @_requires_args
    @_log_command
    @_failsafe
    def gfycat(roboronya, conv, cmd_args, **kwargs):
        """
        /gfycat command: Like the /gif command but instead
        of using giphy it uses gfycat.
        """
        gif_url = _get_gif_url(cmd_args)
        if gif_url:
            kwargs['file_extension'] = 'gif'
            roboronya.send_file(
                conv,
                'Here\'s your gif {user_fullname}.',
                gif_url,
                **kwargs
            )
        else:
            roboronya.send_message(
                conv,
                'Sorry {user_fullname}, I couldn\'t find'
                ' a gif for you.',
                **kwargs
            )
