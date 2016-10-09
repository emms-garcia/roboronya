# -*- coding: utf-8 -*-
import pytest
from unittest import mock

from roboronya import commands
from roboronya.commands import Commands
from roboronya import config
from roboronya.exceptions import CommandValidationException

"""
    Fixtures
"""


@pytest.fixture
def cmd_kwargs():
    def factory(cmd_name, original_message=''):
        return {
            'command_name': cmd_name,
            'original_message': original_message,
            'user_fullname': 'Foo Bar',
        }
    return factory


@pytest.fixture
def mock_roboronya():
    class MockRobornya(object):
        message = None

        def send_message(self, conv, message, **kwargs):
            self.message = message.format(**kwargs)
    return MockRobornya()


@pytest.fixture
def mock_request():
    def factory(json_data, status_code=200):
        class MockResponse(object):
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data
        return MockResponse(json_data, status_code)
    return factory

"""
    Tests
"""


def test_get_gif_url(mock_request):
    with mock.patch('requests.get') as mock_get:
        none_found = mock_request({'gfycats': []})
        mock_get.return_value = none_found
        assert commands.get_gif_url(['foo', 'bar']) is None
        some_found = mock_request({'gfycats': [{'max2mbGif': 'some-url'}]})
        mock_get.return_value = some_found
        assert commands.get_gif_url(['foo', 'bar']) == 'some-url'


def test_help(mock_roboronya, cmd_kwargs):
    Commands.help(mock_roboronya, None, [], **cmd_kwargs('help'))
    for command_help in commands.COMMAND_HELP:
        assert command_help['name'] in mock_roboronya.message
        assert command_help['description'] in mock_roboronya.message


def test_fastgif(mock_roboronya, cmd_kwargs):
    fake_gif_url = 'https://some-url/some.gif'
    with mock.patch('roboronya.commands.get_gif_url') as mock_get_gif_url:
        mock_get_gif_url.return_value = fake_gif_url
        with pytest.raises(CommandValidationException):
            Commands.fastgif(mock_roboronya, None, [], **cmd_kwargs('fastgif'))

        Commands.fastgif(
            mock_roboronya, None, ['foo'], **cmd_kwargs('fastgif'))
        assert fake_gif_url in mock_roboronya.message


def test_love(mock_roboronya, cmd_kwargs):
    Commands.love(mock_roboronya, None, [], **cmd_kwargs('love'))
    assert 'I love you Foo Bar <3' in mock_roboronya.message


def test_cointoss(mock_roboronya, cmd_kwargs):
    Commands.cointoss(mock_roboronya, None, [], **cmd_kwargs('cointoss'))
    assert mock_roboronya.message in ['heads', 'tails']


def test_magicball(mock_roboronya, cmd_kwargs):
    Commands.magicball(mock_roboronya, None, [], **cmd_kwargs('magicball'))
    assert any([
        answer.format(user_fullname='Foo Bar') == mock_roboronya.message
        for answer in config.MAGICBALL_ANSWERS
    ])
