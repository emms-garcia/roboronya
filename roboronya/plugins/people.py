description = 'Display metadata about the users on the current chat.'

from roboronya.plugins.plugin import *

class Command(Plugin):

    def run(roboronya, conv, cmd_args, **kwargs):
        return roboronya.send_message(
            conv,
            (
                '\n'.join([
                    '[**{}**] {} (*{}*)'.format(
                        user_uid,
                        user['user_fullname'],
                        user.get('alias', 'No Alias')
                    )
                    for user_uid, user in roboronya.get_state('users').items()
                ])
            ),
            **kwargs
        )
