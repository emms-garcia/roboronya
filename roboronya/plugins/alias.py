description = 'Change how Roboronya calls a certain user during the current session i. e. */alias user_id alias ...*\nNote: To check the user_id of a certain user use the /people command.'

from roboronya.plugins.plugin import *

class Command(Plugin):

    @requires_args
    def run(roboronya, conv, cmd_args, **kwargs):
        if len(cmd_args) < 2:
            return roboronya.send_message(
                conv,
                'Sorry {user_fullname}, /alias requires at least '
                '2 arguments: */alias user_id alias* ',
                **kwargs
            )
        if not roboronya.get_state('users').get(cmd_args[0]):
            kwargs['alias_user_id'] = cmd_args[0]
            return roboronya.send_message(
                conv,
                'Sorry {user_fullname}, there is no user with '
                'ID {alias_user_id}.',
                **kwargs
            )

        kwargs['alias'] = ' '.join(cmd_args[1:])
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
                cmd_args[0]: {
                    'alias': kwargs['alias']
                }
            }
        )
        kwargs['alias_user_fullname'] = roboronya.get_state(
            'users'
        )[cmd_args[0]]['user_fullname']
        return roboronya.send_message(
            conv,
            (
                'Got it {user_fullname}. For this session '
                '{alias_user_fullname} alias is {alias}.'
            ),
            **kwargs
        )
