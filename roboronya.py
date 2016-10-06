import os

import asyncio
import hangups

import commands
import utils


class RoboronyaException(Exception):
    pass


class Roboronya(object):
    """
    The Roboronya bot, most logic here should be base to
    the bot functionality and should not need to be tweaked
    to support more commands / plugins.
    But it probably will...
    """
    REFRESH_TOKEN_PATH = 'refresh_token.txt'

    def __init__(self):
        try:
            email = os.environ['ROBORONYA_EMAIL']
            password = os.environ['ROBORONYA_PASSWORD']
        except KeyError as e:
            raise RoboronyaException(
                'Failed to retrieve credentials from env. '
                'You must set the ROBORONYA_EMAIL and '
                'ROBORONYA_PASSWORD env variables. '
                'Error: {} not found.'.format(e)
            ) from None

        self._hangups = hangups.Client(
            utils.get_auth_stdin_patched(
                email,
                password,
                self.REFRESH_TOKEN_PATH)
        )

    @asyncio.coroutine
    def _on_hangups_connect(self):
        print('Connected.')
        self._user_list, self._conv_list = (
            yield from hangups.conversation.
            build_user_conversation_list(self._hangups)
        )
        self._conv_list.on_event.add_observer(self._on_hangups_event)

    @staticmethod
    def _send_response(conv, segments, **kwargs):
        asyncio.async(conv.send_message(
            [hangups.ChatMessageSegment(
                segment['text'].format(
                    **kwargs
                ),
                link_target=segment.get('url')
            ) for segment in segments],
            image_file=kwargs.get('image_file'),
        ))

    def _on_hangups_event(self, conv_event):
        print('Conversation event received.')
        if isinstance(conv_event, hangups.ChatMessageEvent):
            conv = self._conv_list.get(conv_event.conversation_id)
            self._handle_message(conv, conv_event)

    def _get_command_args(self, user):
        return {
            'user_fullname': user.full_name,
        }

    def _handle_message(self, conv, conv_event):
        message = conv_event.text
        user = conv.get_user(conv_event.user_id)

        tokens = message.split(' ')
        commands_to_run = []
        for token in tokens:
            if '/' in token:
                commands_to_run.append({
                    'args': [conv, message, []],
                    'name': token.replace('/', ''),
                })
            else:
                if commands_to_run:
                    commands_to_run[-1]['args'][-1].append(token)

        kwargs = self._get_command_args(user)
        for command in commands_to_run:
            kwargs['command_name'] = command['name']
            try:
                command_func = getattr(commands, command['name'])
                command_func(*command['args'], **kwargs)
            except AttributeError as e:
                print(
                    'Could not find command "/{}". Error: {}'.format(
                        command['name'],
                        e,
                    )
                )
            except Exception as e:
                print(
                    'Something went horribly wrong with the /{} command. '
                    'Error: {}'.format(command['name'], e)
                )
                Roboronya._send_response(
                    conv,
                    [{
                        'text': (
                            'Sorry {user_fullname} something went wrong '
                            'with your /{command_name}.'
                        )

                    }],
                    **kwargs
                )

    def run(self):
        self._hangups.on_connect.add_observer(
            lambda: asyncio.async(self._on_hangups_connect())
        )

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._hangups.connect())


if __name__ == '__main__':
    Roboronya().run()
