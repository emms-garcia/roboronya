import random

from roboronya import Roboronya


def _extract_arguments(*args):
    return (
        args[0],
        args[1],
        tuple(args[2:]),
    )


"""
    Implemented commands. Any /command_name found in message (and
    arguments) will be redirected here. Parameters are (in order):
    - conv: hangups.conversation.Conversation object.
    - message: original string message that triggered the command.
    - cmd_args (optional): arguments given for the command, or
    in other words any following words written after the command.
"""

def gif(*args, **kwargs):
    """
    /gif command. Should send the first gif found from an API
    (probably giphy) that matches the argument words.
    """
    conv, message, cmd_args = _extract_arguments(*args)
    Roboronya._send_response(
        conv,
        ['Not yet implemented, this will have to suffice for now.'],
        image_file=open('corgi.gif', 'rb'),
    )


def love(*args, **kwargs):
    """
    /love command. From Robornya with love.
    """
    conv, message, cmd_args = _extract_arguments(*args)
    Roboronya._send_response(
        conv,
        ['I love you {user_fullname} <3.'],
        **kwargs
    )


def cointoss(*args, **kwargs):
    """
    /cointoss command. Tosses a coin to make a decision as gods should,
    based on luck.
    """
    conv, message, cmd_args = _extract_arguments(*args)
    Roboronya._send_response(
        conv,
        ['heads' if random.getrandbits(1) == 0 else 'tails'],
        **kwargs
    )
