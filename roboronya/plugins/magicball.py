import random
from roboronya.plugins.plugin import Plugin
from roboronya.config import MAGICBALL_ANSWERS

class Magicball(Plugin):
    
    description = 'Ask Roboronya for advice. She knows more than she tells.'
    name = 'magicball'
    
    def run(roboronya, conv, cmd_args, **kwargs):
        """
        /magicball command: Randomly answer like a magic ball.
        """
        message = random.choice(MAGICBALL_ANSWERS)
        return roboronya.send_message(
            conv, message, **kwargs
            )
