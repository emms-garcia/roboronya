from roboronya.plugins.plugin import Plugin

class Command(Plugin):

    description = 'From Roboronya with love.'
    name = 'love'

    def run(roboronya, conv, cmd_args, **kwargs):
        """
        /love command. From Robornya with love.
        """
        message = 'I love you {user_fullname} <3.'
        return roboronya.send_message(
            conv, message, **kwargs
            )
