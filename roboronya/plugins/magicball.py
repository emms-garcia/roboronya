description = "Ask Roboronya for advice. She knows more than she tells."

from roboronya.plugins.plugin import *

class Command(Plugin):

    def run(roboronya, conv, cmd_args, **kwargs):
        """
        /magicball command: Randomly answer like a magic ball.
        """
        message = random.choice(config.MAGICBALL_ANSWERS)
        return roboronya.send_message(
            conv, message, **kwargs
            )
