description = "Check if bot is online. Should always work."

from roboronya.plugins.plugin import *

class Command(Plugin):

    def run(roboronya, conv, cmd_args, **kwargs):
        """
        /ping command. Check bot status.
        """
        message = '**Pong!**'
        return roboronya.send_message(
            conv, message, **kwargs
            )
