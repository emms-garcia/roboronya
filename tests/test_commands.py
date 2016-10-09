# -*- coding: utf-8 -*-
import pytest

from roboronya.commands import Commands, COMMAND_HELP


@pytest.fixture
def fake_roboronya():
    class FakeRobornya(object):
        message = None

        def send_message(self, conv, message, **kwargs):
            self.message = message

    return FakeRobornya()


def test_help(fake_roboronya):
    kwargs = {
        'command_name': 'help'
    }

    Commands.help(fake_roboronya, None, [], **kwargs)

    for command_help in COMMAND_HELP:
        assert command_help['name'] in fake_roboronya.message
        assert command_help['description'] in fake_roboronya.message
