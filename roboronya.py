# -*- coding: utf-8 -*-
__author__ = 'Emmanuel García'
__title__ = 'roboronya'
__license__ = 'MIT'
__version__ = '0.1'

import os
import shutil
import sys
import time
import threading
import uuid

import asyncio
import hangups
import requests

import commands
from config import IMAGES_DIR, MAX_RECONNECT_RETRIES, REFRESH_TOKEN_PATH
from utils import create_path_if_not_exists, get_auth_stdin_patched


class RoboronyaException(Exception):
    pass


class Roboronya(object):
    """
    The Roboronya bot, most logic here should be base to
    the bot functionality and should not need to be tweaked
    to support more commands / plugins.
    But it probably will...
    """

    async def _on_hangups_connect(self):
        print('Connected.')
        self._user_list, self._conv_list = (
            await hangups.conversation.
            build_user_conversation_list(self._hangups)
        )
        self._conv_list.on_event.add_observer(
            self._on_hangups_event
        )

    async def _on_disconnect(self):
        print('Disconnected.')

    async def _on_hangups_event(self, conv_event):
        print('Conversation event received.')
        if isinstance(conv_event, hangups.ChatMessageEvent):
            conv = self._conv_list.get(conv_event.conversation_id)
            threading.Thread(
                args=(conv, conv_event),
                target=self._handle_message,
            ).start()

    def _handle_message(self, conv, conv_event):
        asyncio.set_event_loop(self._loop)

        user = conv.get_user(conv_event.user_id)
        if self._email in user.emails:
            return

        message = conv_event.text
        possible_commands = []
        for token in message.split():
            if '/' in token:
                possible_commands.append({
                    'args': [conv, []],
                    'name': token.replace('/', '')
                })
            else:
                if possible_commands:
                    possible_commands[-1]['args'][-1].append(token)

        kwargs = {
            'original_message': message,
            'user_fullname': user.full_name,
        }
        for command in possible_commands:
            kwargs['command_name'] = command['name']
            try:
                command_func = getattr(commands.Commands, command['name'])
                command_func(*command['args'], **kwargs)
            except AttributeError as e:
                print(
                    'Could not find command "/{}". Error: {}'.format(
                        command['name'],
                        e
                    )
                )
            except Exception as e:
                print(
                    'Something went horribly wrong with the /{} command. '
                    'Error: {}'.format(command['name'], e)
                )
                Roboronya._send_response(
                    conv,
                    (
                        'Sorry {user_fullname} something went wrong '
                        'with your /{command_name}.'
                    ),
                    **kwargs
                )

    @staticmethod
    def _send_response(conv, text, **kwargs):
        asyncio.async(conv.send_message(
            hangups.ChatMessageSegment.from_str(
                text.format(**kwargs)
            ),
            image_file=kwargs.get('image_file')
        ))

    @staticmethod
    def _send_file(conv, media_url, **kwargs):
        """
        Send a file to the conversation.
        """
        response = requests.get(media_url)
        file_path = '{}.{}'.format(
            os.path.join(
                IMAGES_DIR,
                str(uuid.uuid4())
            ),
            '.gif'
        )

        create_path_if_not_exists(file_path)
        with open(file_path, 'wb+') as img:
            img.write(response.content)

        Roboronya._send_response(
            conv,
            'Here\'s your gif {user_fullname}.',
            image_file=open(file_path, 'rb+'),
            **kwargs
        )

    def login(self):
        try:
            self._email = os.environ['ROBORONYA_EMAIL']
            password = os.environ['ROBORONYA_PASSWORD']
        except KeyError as e:
            raise RoboronyaException(
                'Failed to retrieve credentials from env. '
                'You must set the ROBORONYA_EMAIL and '
                'ROBORONYA_PASSWORD env variables. '
                'Error: {} not found.'.format(e)
            ) from None

        return get_auth_stdin_patched(
            self._email,
            password,
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
        asyncio.async(
            self._hangups.disconnect()
        ).add_done_callback(lambda future: future.result())

if __name__ == '__main__':
    roboronya = Roboronya()
    try:
        roboronya.run()
    except KeyboardInterrupt:
        roboronya.stop()
