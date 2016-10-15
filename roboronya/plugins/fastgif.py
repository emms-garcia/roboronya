from roboronya.plugins.plugin import Plugin
import roboronya.utils as utils

logger = utils.get_logger(__name__)

class FastGif(Plugin):

    description = "For faster gifs, this only sends back the gif url."
    name = 'fastgif'
    
    @Plugin.requires_args
    def run(roboronya, conv, cmd_args, **kwargs):
        """
        /fastgif command. Searches for a gif and sends the url.
        """
        kwargs['gif_url'] = utils.get_gif_url(cmd_args)
        if kwargs['gif_url']:
            logger.info(
                '{} Found gif for keywords: ({}). Url: {}.'.format(
                    kwargs['log_tag'], ', '.join(cmd_args), kwargs['gif_url'],
                    )
                )
            return roboronya.send_message(
                conv,
                (
                    'Here is your URL to the gif {user_fullname}: '
                    '{gif_url} ... love you btw'
                    ),
                **kwargs
                )
        return roboronya.send_message(
            conv,
            'Sorry {user_fullname}, I could not find a fast gif for you.',
            **kwargs
            )
