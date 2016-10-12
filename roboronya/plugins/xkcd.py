description = "Get a random XKCD comic, or specify a comic number. i. e. */xkcd* or */xkcd 10*"

from roboronya.plugins.plugin import *

class Command(Plugin):

    def run(roboronya, conv, cmd_args, **kwargs):
        response_json = requests.get(
            config.XKCD_LATEST_URL
        ).json()
        current_num = response_json['num']
        if cmd_args:
            kwargs['current_num'] = current_num
            try:
                comic_num = int(cmd_args[0])
            except ValueError:
                raise CommandValidationException(
                    'Sorry {user_fullname}, argument must '
                    'be a number between 1 and {current_num}.'.format(
                        **kwargs
                    )
                )
            if comic_num > current_num or comic_num < 0:
                raise CommandValidationException(
                    'Sorry {user_fullname}, current comic '
                    'numbers are between 1 and {current_num}.'.format(
                        **kwargs
                    )
                )
        else:
            comic_num = random.randint(1, current_num)

        response_json = requests.get(
            config.XKCD_DETAIL_URL.format(comic_num=comic_num)
        ).json()
        return roboronya.send_file(
            conv,
            (
                'Title: {}\nURL: {}'.format(
                    response_json['title'], response_json['img'],
                )
            ),
            response_json['img'],
            **kwargs
        )
