description = "From Roboronya with love."

from roboronya.plugins.plugin import *

class Command(Plugin):

    def run(roboronya, conv, cmd_args, **kwargs):
        """
        /love command. From Robornya with love.
        """
        message = 'I love you {user_fullname} <3.'
        return roboronya.send_message(
            conv, message, **kwargs
            )
