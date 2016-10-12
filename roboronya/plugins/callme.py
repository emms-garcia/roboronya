description = 'Change how Roboronya calls you. i. e. */callme Bond, James Bond*'

from roboronya.plugins.plugin import *

class Command(Plugin):

    @requires_args
    def run(roboronya, conv, cmd_args, **kwargs):
        kwargs['alias'] = ' '.join(cmd_args)
        invalid_alias_message = is_invalid_alias(kwargs['alias'])
        if invalid_alias_message:
            return roboronya.send_message(
                conv,
                invalid_alias_message,
                **kwargs
            )
        roboronya.set_state(
            'users',
            {
                kwargs['user_uid']: {
                    'alias': kwargs['alias']
                }
            }
        )
        return roboronya.send_message(
            conv,
            (
                'Got it {user_fullname}. For this session your '
                'alias is {alias}.'
            ),
            **kwargs
        )
