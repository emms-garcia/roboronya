description = 'Randomly decide "yes" or "no", with a cool image.'

from roboronya.plugins.plugin import *

class Command(Plugin):

    def run(roboronya, conv, cmd_args, **kwargs):
        response_json = requests.get(
            config.YES_OR_NO_API
        ).json()
        return roboronya.send_file(
            conv, response_json['answer'], response_json['image'], **kwargs
        )
