description = 'Searches for a gif (from Gfycat) that matches the words following the command. i. e. */gif dog*.'

from roboronya.plugins.plugin import *

class Command(Plugin):

    @requires_args
    def run(roboronya, conv, cmd_args, **kwargs):
        """
        /gif command: Translates commands argument words as
        gifs using gfycat.
        """
        gif_url = get_gif_url(cmd_args)
        if gif_url:
            message = 'Here\'s your gif {user_fullname}.'
            return roboronya.send_file(
                conv, message, gif_url, **kwargs
            )
        else:
            return roboronya.send_message(
                conv,
                (
                    'Sorry {user_fullname}, I couldn\'t find '
                    'a gif for you.'
                ),
                **kwargs
            )
