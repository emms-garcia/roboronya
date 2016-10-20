# -*- coding: utf-8 -*-
import collections
import logging
import os
import uuid

import hangups

import random
import requests
from roboronya import config
from roboronya.config import LOG_LEVEL


def create_path_if_not_exists(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))


def get_file_extension(file_name):
    return os.path.splitext(file_name)[1][1:]


def get_auth_stdin_patched(email, password, refresh_token_filename):
    """
    Patch to hangups.auth.get_auth_stdin to avoid
    having to input email and password.
    """
    create_path_if_not_exists(refresh_token_filename)

    class CredentialsPromptPatch(object):
        @staticmethod
        def get_email():
            return email

        @staticmethod
        def get_password():
            return password

        @staticmethod
        def get_verification_code():
            return input('Verification code: ')

    return hangups.auth.get_auth(
        CredentialsPromptPatch(),
        hangups.auth.RefreshTokenCache(refresh_token_filename)
    )


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_uuid():
    return str(uuid.uuid4()).replace('-', '')[:8].upper()


def dict_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = dict_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d

def is_invalid_alias(alias):
    if len(alias) > config.MAX_ALIAS_LENGTH:
        return 'Sorry {user_fullname}, that alias is too long.'
    if len(alias) < 3:
        return 'Sorry {user_fullname}, that alias is too short.'
    return None

def get_gif_url(keywords):
    """
    Get an URL to a gif, given some keywords.
    """
    response_json = requests.get(
        config.GIFYCAT_SEARCH_URL,
        params={'search_text': ' '.join(keywords)}
        ).json()
    gfycats = response_json.get('gfycats', [])
    if gfycats:
        gfycat_json = random.choice(gfycats)
        return gfycat_json['max2mbGif']
    return None
