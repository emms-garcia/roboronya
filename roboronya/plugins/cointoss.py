import random
from roboronya.plugins.plugin import Plugin

class Command(Plugin):

    description = 'Randomly toss a coin. 50-50 chances.'
    name = 'cointoss'

    def run(roboronya, conv, cmd_args, **kwargs):
        """
        /cointoss command. Tosses a coin to make a decision as gods should,
        based on luck.
        """
        message = 'heads' if random.getrandbits(1) == 0 else 'tails'
        return roboronya.send_message(
            conv, message, **kwargs
            )
