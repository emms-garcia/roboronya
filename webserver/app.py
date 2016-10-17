# -*- coding: utf-8 -*-
import asyncio
import hangups

from flask import Flask
from flask_restful import Resource, Api, reqparse

from roboronya import Roboronya
from roboronya.utils import get_uuid

app = Flask(__name__)
api = Api(app)


def run_command(command, cmd_args):
    @asyncio.coroutine
    def _run_command(roboronya, command, cmd_args):
        _, conv_list = (
            yield from hangups.conversation.
            build_user_conversation_list(roboronya._hangups)
        )

        conv = conv_list.get('Ugynr8qfH_u3FFrArAt4AaABAagBjJHkBw')

        cmd_args = [
            roboronya,
            conv,
            cmd_args

        ]

        kwargs = {
            'command_name': command,
            'log_tag': '[API_USER-{}]'.format(get_uuid()),
            'user_fullname': 'API_USER',
        }

        yield from asyncio.async(
            roboronya.run_command(
                command, cmd_args, **kwargs
            )
        )
        yield from roboronya._hangups.disconnect()

    roboronya = Roboronya()
    roboronya.connect()

    roboronya._hangups.on_connect.add_observer(
        lambda: asyncio.async(_run_command(roboronya, command, cmd_args)))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(roboronya._hangups.connect())


class CommandsResource(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        'conversation_id', location='json', required=False, type=str
    )
    parser.add_argument(
        'command_name', location='json', required=False, type=str
    )
    parser.add_argument(
        'command_args', location='json', required=False, type=list
    )

    def get(self):
        cmd_args = ['test', 'gif']
        command = 'fastgif'
        run_command(command, cmd_args)


"""
class ConversationListResource(Resource):

    def _get_user_dict(self, user):
        return {
            'id': user.id_[0],
            'name': user.full_name,
        }

    def _get_conv_dict(self, conv):
        name = conv.name
        if name is None:
            # Single person chat
            for user in conv.users:
                if not user.is_self:
                    name = user.full_name

        return {
            'id': conv.id_,
            'last_modified': time.mktime(conv.last_modified.timetuple()),
            'name': name,
            'users': [
                self._get_user_dict(user) for user in conv.users
            ]
        }

    def get(self):
        return {
            'data': [
                self._get_conv_dict(conv)
                for conv in roboronya._conv_list.get_all()
            ]
        }

api.add_resource(ConversationListResource, '/conversations/')
"""
api.add_resource(CommandsResource, '/commands/')


if __name__ == '__main__':
    app.run()
