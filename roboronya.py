import asyncio
import hangups

import commands


class Roboronya(object):

    REFRESH_TOKEN_PATH = 'refresh_token.txt'

    def __init__(self):
        self._hangups = hangups.Client(
            hangups.auth.get_auth_stdin(self.REFRESH_TOKEN_PATH)
        )

    @asyncio.coroutine
    def _on_hangups_connect(self):
        self._user_list, self._conv_list = (
            yield from hangups.conversation.
            build_user_conversation_list(self._hangups)
        )
        self._conv_list.on_event.add_observer(self._on_hangups_event)

    @staticmethod
    def _send_response(conv, segments, **kwargs):
        asyncio.async(conv.send_message(
            [hangups.ChatMessageSegment(
                segment.format(
                    **kwargs
                ),
            ) for segment in segments],
            image_file=kwargs.get('image_file'),
        ))

    def _on_hangups_event(self, conv_event):
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
        arg_lookup, tokens = False, message.split(' ')
        commands_to_run = []
        for token in tokens:
            if '/' in token:
                commands_to_run.append({
                    'args': [conv, message],
                    'name': token.replace('/', ''),
                })

            else:
                if commands_to_run:
                    commands_to_run[-1]['args'].append(token)

        kwargs = self._get_command_args(user)
        for command in commands_to_run:
            try:
                command_func = getattr(commands, command['name'])
                command_func(*command['args'], **kwargs)
            except AttributeError as e:
                print(e)
                print(
                    'Could not find command "{}".'.format(
                        command['name'],
                    )
                )

    def run(self):
        self._hangups.on_connect.add_observer(
            lambda: asyncio.async(self._on_hangups_connect())
        )

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._hangups.connect())


if __name__ == '__main__':
    Roboronya().run()
