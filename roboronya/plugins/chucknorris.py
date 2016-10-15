import requests
from roboronya.plugins.plugin import Plugin
from roboronya.config import CHUCK_API_URL

class ChuckNorris(Plugin):

    description = 'Look for a ~~random joke~~ undeniable truth about our lord and savior.'
    name = 'chucknorris'

    def run(roboronya, conv, cmd_args, **kwargs):
        random_joke = requests.get(
            CHUCK_API_URL
        ).json()
        if random_joke.get('type') == 'success':
            return roboronya.send_message(
                conv, random_joke['value']['joke'], **kwargs
            )
        logger.info(
            '{} Failed to retrieve joke from {}. '
            'Got response: {}'.format(
                kwargs['log_tag'], CHUCK_API_URL, random_joke,
            )
        )
        return roboronya.send_message(
            conv,
            (
                'Sorry I could not find a joke '
                'Please try again later.'
            ),
            **kwargs
        )
