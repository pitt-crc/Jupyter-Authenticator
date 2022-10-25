"""Test user authentication classes relay user login handling to the ``RemoteUserLoginHandler``."""

from unittest import TestCase

from jupyterhub.auth import Authenticator

from crc_jupyter_auth import RemoteUserAuthenticator, RemoteUserLocalAuthenticator
from crc_jupyter_auth.remote_user_auth import RemoteUserLoginHandler


class HandlerRegistration(TestCase):
    """Test authentication classes use the ``RemoteUserLoginHandler`` to route login requests"""

    def run_test_on_authenticator(self, authenticator: Authenticator) -> None:
        """Assert the given authenticator routes ``/login`` traffic using the ``RemoteUserLoginHandler`` class"""

        handlers_list = authenticator.get_handlers(app=None)
        handlers_dict = dict(*zip(handlers_list))
        self.assertIs(RemoteUserLoginHandler, handlers_dict['/login'])

    def test_user_authenticator(self) -> None:
        """Test the ``RemoteUserAuthenticator`` routes traffic using the ``RemoteUserLoginHandler`` handler"""

        self.run_test_on_authenticator(RemoteUserAuthenticator())

    def test_local_authenticator(self) -> None:
        """Test the ``RemoteUserLocalAuthenticator`` routes traffic using the ``RemoteUserLoginHandler`` handler"""

        self.run_test_on_authenticator(RemoteUserLocalAuthenticator())
