# -*- coding: utf-8 -*-
import hangups


def get_auth_stdin_patched(email, password, refresh_token_filename):
    """
    Patch to hangups.auth.get_auth_stdin to avoid
    having to input email and password.
    """
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
