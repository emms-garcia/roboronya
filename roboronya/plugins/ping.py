from roboronya.plugins.plugin import Plugin

class Ping(Plugin):

    description = "Check if bot is online. Should always work."
    name = "ping"

    def run(roboronya, conv, cmd_args, **kwargs):
        """
        /ping command. Check bot status.
        """
        message = '**Pong!**'
        return roboronya.send_message(
            conv, message, **kwargs
            )
