from roboronya.exceptions import CommandValidationException

class Plugin(object):

    def requires_args(fn):
        """
        Decorator to validate commands that require arguments.
        """
        def wrapper(roboronya, conv, cmd_args, **kwargs):
            if not cmd_args:
                raise CommandValidationException(
                    'Sorry {user_fullname}, the /{command_name} '
                    'command requires arguments to work.'
                    )
            return fn(roboronya, conv, cmd_args, **kwargs)
        return wrapper

    @staticmethod
    def run(roboronya, conv, cmd_args, **kwargs):
        pass
