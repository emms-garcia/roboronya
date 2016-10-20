import requests
from roboronya.plugins.plugin import Plugin
from roboronya.config import PIRATE_API_URL

class Piratify(Plugin):

    description = 'Translate some text to the good old pirate language.'
    name = 'piratify'

    @Plugin.requires_args
    def run(roboronya, conv, cmd_args, **kwargs):
        response_json = requests.get(
            PIRATE_API_URL,
            params={'format': 'json', 'text': ' '.join(cmd_args)}
        ).json()
        if response_json.get('translation'):
            return roboronya.send_message(
                conv,
                '**{}**'.format(response_json['translation']['pirate']),
                **kwargs
            )
        return roboronya.send_message(
            conv,
            'Sorry {user_fullname}, I could not piratify your message.',
            **kwargs
        )
