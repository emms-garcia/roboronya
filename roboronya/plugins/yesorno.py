import requests
from roboronya.plugins.plugin import Plugin
from roboronya.config import YES_OR_NO_API

class YesNo(Plugin):

    description = 'Randomly decide "yes" or "no", with a cool image.'
    name = 'yesorno'
    
    def run(roboronya, conv, cmd_args, **kwargs):
        response_json = requests.get(
            YES_OR_NO_API
        ).json()
        return roboronya.send_file(
            conv, response_json['answer'], response_json['image'], **kwargs
        )
