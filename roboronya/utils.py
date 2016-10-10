# -*- coding: utf-8 -*-
import logging
import os
import uuid

import hangups

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
