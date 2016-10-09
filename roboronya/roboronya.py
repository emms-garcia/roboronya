# -*- coding: utf-8 -*-
import os
import shutil
import sys
import time
import uuid

import asyncio
import hangups
import requests

from roboronya.commands import Commands
from roboronya.config import (
    IMAGES_DIR, MAX_COMMANDS_PER_MESSAGE,
    MAX_RECONNECT_RETRIES, REFRESH_TOKEN_PATH,
)
from roboronya.exceptions import CommandValidationException
from roboronya.utils import create_path_if_not_exists, get_file_extension


class Roboronya(object):
    """
    The Roboronya bot, most logic here should be base to
    the bot functionality and should not need to be tweaked
    to support more commands / plugins.
    But it probably will...
    """

    @asyncio.coroutine
    def _on_hangups_connect(self):
        print('Connected.')
        self._user_list, self._conv_list = (
            yield from hangups.conversation.
            build_user_conversation_list(self._hangups)
        )
        self._conv_list.on_event.add_observer(
            self._on_hangups_event
        )

    @asyncio.coroutine
    def _on_disconnect(self):
        print('Disconnected.')

    @asyncio.coroutine
    def _on_hangups_event(self, conv_event):
        print('Conversation event received.')
        if isinstance(conv_event, hangups.ChatMessageEvent):
            conv = self._conv_list.get(conv_event.conversation_id)
            self._handle_message(conv, conv_event)

    def _handle_message(self, conv, conv_event):
        asyncio.set_event_loop(self._loop)
        user = conv.get_user(conv_event.user_id)
        if user.is_self:
            return

        message = conv_event.text
        possible_commands = []
        for token in message.split():
            if '/' in token:
                possible_commands.append({
                    'args': [self, conv, []],
                    'name': token.replace('/', '')
                })
            else:
                if possible_commands:
                    possible_commands[-1]['args'][-1].append(token)

        kwargs = {
            'original_message': message,
            'user_fullname': user.full_name,
        }

        if len(possible_commands) > MAX_COMMANDS_PER_MESSAGE:
            kwargs['num_cmds'] = MAX_COMMANDS_PER_MESSAGE
            return self.send_message(
                conv,
                (
                    'Sorry {user_fullname} I can only process '
                    '{num_cmds} command(s) per message.'
                ),
                **kwargs
            )

        for command in possible_commands:
            kwargs['command_name'] = command['name']
            try:
                command_func = getattr(Commands, command['name'], None)
                if command_func:
                    print(
                        'Running /{} command with arguments: [{}].'.format(
                            command['name'],
                            ', '.join(command['args'][-1])
                        )
                    )
                    command_func(*command['args'], **kwargs)
                else:
                    print(
                        'Could not find command "/{}".'.format(
                            command['name'],
                        )
                    )
            except CommandValidationException as e:
                print(e)
                self.send_message(
                    conv,
                    str(e),
                    **kwargs
                )
            except Exception as e:
                print(
                    'Something went horribly wrong with the /{} command. '
                    'Error: {}'.format(command['name'], e)
                )
                self.send_message(
                    conv,
                    (
                        'Sorry {user_fullname} I failed to process '
                        'your command: "{original_message}".'
                    ),
                    **kwargs
                )

    def send_message(self, conv, text, **kwargs):
        asyncio.async(conv.send_message(
            hangups.ChatMessageSegment.from_str(
                text.format(**kwargs)
            ),
            image_file=kwargs.get('image_file')
        ))

    def send_file(self, conv, text, media_url, **kwargs):
        """
        Send a file to the conversation.
        """
        response = requests.get(media_url)
        file_path = '{}.{}'.format(
            os.path.join(
                IMAGES_DIR,
                str(uuid.uuid4())
            ),
            get_file_extension(media_url)
        )

        create_path_if_not_exists(file_path)
        with open(file_path, 'wb+') as img:
            img.write(response.content)

        self.send_message(
            conv,
            text,
            image_file=open(file_path, 'rb+'),
            **kwargs
        )

    def login(self):
        create_path_if_not_exists(REFRESH_TOKEN_PATH)
        return hangups.auth.get_auth_stdin(
            REFRESH_TOKEN_PATH
        )

    def run(self):
        cookies = self.login()
        if cookies:
            self._loop = asyncio.get_event_loop()
            for retry in range(MAX_RECONNECT_RETRIES):
                try:
                    self._hangups = hangups.Client(cookies)

                    self._hangups.on_connect.add_observer(
                        self._on_hangups_connect
                    )
                    self._hangups.on_disconnect.add_observer(
                        self._on_disconnect
                    )

                    self._loop.run_until_complete(
                        self._hangups.connect()
                    )
                except Exception as e:
                    print(
                        'Roboronya disconnected. Error: {}'.format(
                            e
                        )
                    )
                    print(
                        'Retrying {}/{}...'.format(
                            retry + 1,
                            MAX_RECONNECT_RETRIES
                        )
                    )
                    time.sleep(5 + retry * 5)

            print('Roboronya is exiting.')
            sys.exit(0)

        print('Invalid login.')
        sys.exit(0)

    def stop(self):
        print('Roboronya was stopped.')
        if os.path.exists(IMAGES_DIR):
            shutil.rmtree(IMAGES_DIR)
        if hasattr(self, '_hangups'):
            asyncio.async(
                self._hangups.disconnect()
            ).add_done_callback(lambda future: future.result())
