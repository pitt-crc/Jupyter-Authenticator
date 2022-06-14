"""Test HTTP request routing by the ``RemoteUserLoginHandler`` class."""

from unittest import TestCase

from jupyterhub.auth import Authenticator
from jupyterhub.objects import Server
from tornado import web
from tornado.httputil import HTTPServerRequest, HTTPHeaders, HTTPConnection
from tornado.web import Application

from crc_jupyter_auth.remote_user_auth import RemoteUserLoginHandler, RemoteUserAuthenticator


class RequestRouting(TestCase):
    """Test the routing of HTTP authentication requests"""

    @staticmethod
    def create_http_request_handler(authenticator: Authenticator, header_data: dict) -> RemoteUserLoginHandler:
        """Create a mock HTTP request handler

        Create a mock HTTP request reflecting the given HTTP header data and
        return an instance of the ``RemoteUserLoginHandler`` class for handling
        that request.

        Args:
            authenticator: The authenticator to use when handling the incoming request
            header_data: Head data to include in the returned request

        Returns:
            An instance of the ``RemoteUserLoginHandler`` class
        """

        # Create a tornado application running a jupyterhub server
        application = Application(hub=Server(), authenticator=authenticator)

        # HTTP connections are used by the application to write HTTP responses
        # The `set_close_callback` method is required to exist by JupyterHub
        connection = HTTPConnection()
        connection.set_close_callback = lambda x: None

        # Return an HTTP request reflecting the given header data
        headers = HTTPHeaders(header_data)
        request = HTTPServerRequest(headers=headers, connection=connection)
        return RemoteUserLoginHandler(application=application, request=request)

    def test_missing_username_401(self) -> None:
        """Test for a 401 error when the username is missing from the HTTP header"""

        request_handler = self.create_http_request_handler(RemoteUserAuthenticator(), dict())
        with self.assertRaises(web.HTTPError(401)):
            request_handler.get()

    def test_blank_username_401(self) -> None:
        """Test for a 401 error when the username is blank"""

        request_handler = self.create_http_request_handler(RemoteUserAuthenticator(), {'Cn': ''})
        with self.assertRaises(web.HTTPError(401)):
            request_handler.get()

    def test_missing_vpn_role_redirect(self) -> None:
        """Test users are redirected to the ``vpn_redirect`` url for missing VPN roles"""

        authenticator = RemoteUserAuthenticator()
        request_handler = self.create_http_request_handler(authenticator, {authenticator.header_name: 'username'})
        request_handler.get()

        # TODO: Get the destination without accessing private attributes
        destination = request_handler._headers['Location']
        self.assertEqual(authenticator.vpn_redirect, destination)

    def test_incorrect_vpn_role_redirect(self) -> None:
        """Test users are redirected to the ``vpn_redirect`` url for incorrect VPN roles"""

        raise NotImplementedError

    def test_missing_home_dir_redirect(self) -> None:
        """Test users are redirected to the ``user_redirect`` url if they do not have a home directory"""

        raise NotImplementedError

    def test_valid_user_redirect(self) -> None:
        """Test valid authentication attempts are redirected to the JupyterHub URL"""

        raise NotImplementedError
