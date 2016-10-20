import requests
from roboronya.plugins.plugin import Plugin
from roboronya.config import CATFACTS_API_URL

class Catfacts(Plugin):

    description = 'Get a random fact about your furry friends.'
    name = 'catfacts'

    def run(roboronya, conv, cmd_args, **kwargs):
        response_json = requests.get(
            CATFACTS_API_URL
        ).json()
        is_valid_response = (
            response_json.get('success') == 'true' and
            response_json.get('facts')
        )
        if is_valid_response:
            return roboronya.send_message(
                conv,
                '**Did you know?** {}'.format(
                    '\n'.join(response_json['facts'])
                ),
                **kwargs
            )
        return roboronya.send_message(
            conv,
            'Sorry {user_fullname}, I could not find any cat facts.',
            **kwargs
        )
