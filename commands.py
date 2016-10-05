"""Example of using hangups to send a chat message to a conversation."""
import random

from roboronya import Roboronya


def _extract_arguments(*args):
    return (
        args[0],
        args[1],
        tuple(args[2:]),
    )


# Valid commands.
def gif(*args, **kwargs):
    conv, message, cmd_args = _extract_arguments(*args)
    Roboronya._send_response(
        conv,
        ['No implementado aún, esto tendra que bastar.'],
        image_file=open('corgi.gif', 'rb'),
    )


def love(*args, **kwargs):
    conv, message, cmd_args = _extract_arguments(*args)
    Roboronya._send_response(
        conv,
        ['Te amo {user_fullname} <3.'],
        **kwargs
    )


def cointoss(*args, **kwargs):
    conv, message, cmd_args = _extract_arguments(*args)
    Roboronya._send_response(
        conv,
        ['Cara' if random.getrandbits(1) == 0 else 'Cruz'],
        **kwargs
    )
