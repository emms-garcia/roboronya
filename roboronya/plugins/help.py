from roboronya.plugins.plugin import Plugin

class Help(Plugin):

    description = 'Shows the available commands.'
    name = 'help'

    def run(roboronya, conv, cmd_args, **kwargs):
        """
        /help command. Shows the available commands.
        """
        
        COMMAND_HELP = kwargs['metadata']

        if not cmd_args:
            return roboronya.send_message(
                conv,
                (
                    'Here are the available commands, to learn '
                    'more about a single command type /help '
                    '*command_name*\n'
                    '{}'.format('\n'.join([
                                '**/{}**'.format(command['name'])
                                for command in COMMAND_HELP
                                ]))
                    ),
                **kwargs
                )
        try:
            cmd_help = next(
                filter(
                    lambda x: x['name'] == cmd_args[0],
                    COMMAND_HELP
                    )
                )
            return roboronya.send_message(
                conv,
                '**/{}**: {}'.format(
                    cmd_help['name'], cmd_help['description'],
                    ),
                **kwargs
                )
        except StopIteration:
            return roboronya.send_message(
                conv,
                'No help found for command: **/{}**.'.format(
                    cmd_args[0]
                    ),
                **kwargs
                )
