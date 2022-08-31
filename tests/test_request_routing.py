"""Test HTTP request routing by the ``RemoteUserLoginHandler`` class."""

from unittest import TestCase
from unittest.mock import patch

from jupyterhub.auth import Authenticator
from jupyterhub.objects import Server
from jupyterhub.utils import url_path_join
from tornado import web
from tornado.httputil import HTTPConnection, HTTPHeaders, HTTPServerRequest
from tornado.web import Application

from crc_jupyter_auth.remote_user_auth import (RemoteUserAuthenticator, RemoteUserLocalAuthenticator, RemoteUserLoginHandler)


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
        with self.assertRaises(web.HTTPError) as http_exception:
            request_handler.get()

        self.assertEqual(401, http_exception.exception.status_code)

    def test_blank_username_401(self) -> None:
        """Test for a 401 error when the username is blank"""

        request_handler = self.create_http_request_handler(RemoteUserAuthenticator(), {'Cn': ''})
        with self.assertRaises(web.HTTPError) as http_exception:
            request_handler.get()

        self.assertEqual(401, http_exception.exception.status_code)

    def test_missing_vpn_role(self) -> None:
        """Test users are redirected to the ``vpn_redirect`` url for missing VPN roles"""

        authenticator = RemoteUserAuthenticator()
        request_handler = self.create_http_request_handler(authenticator, {authenticator.header_name: 'username'})
        request_handler.get()

        # TODO: Get the destination without accessing private attributes
        destination = request_handler._headers['Location']
        self.assertEqual(authenticator.vpn_redirect, destination)

    def test_incorrect_vpn_role(self) -> None:
        """Test users are redirected to the ``vpn_redirect`` url for incorrect VPN roles"""

        authenticator = RemoteUserAuthenticator()
        header_data = {
            authenticator.header_name: 'username',
            authenticator.header_vpn: 'FAKEROLE1;FAKEROLE2'
        }

        request_handler = self.create_http_request_handler(authenticator, header_data)
        request_handler.get()

        # TODO: Get the destination without accessing private attributes
        destination = request_handler._headers['Location']
        self.assertEqual(authenticator.vpn_redirect, destination)

    @patch('os.path.exists', lambda path: False)
    def test_missing_home_dir_redirect(self) -> None:
        """Test users are redirected to the ``user_redirect`` url if they do not have a home directory"""

        authenticator = RemoteUserAuthenticator()
        header_data = {
            authenticator.header_name: 'username',
            authenticator.header_vpn: authenticator.required_vpn_role
        }

        request_handler = self.create_http_request_handler(authenticator, header_data)
        request_handler.get()

        # TODO: Get the destination without accessing private attributes
        destination = request_handler._headers['Location']
        self.assertEqual(authenticator.user_redirect, destination)

    @patch('os.path.exists', lambda path: True)
    def test_valid_user_redirect(self) -> None:
        """Test valid authentication attempts are redirected to the JupyterHub URL"""

        authenticator = RemoteUserAuthenticator()
        header_data = {
            authenticator.header_name: 'username',
            authenticator.header_vpn: authenticator.required_vpn_role
        }

        request_handler = self.create_http_request_handler(authenticator, header_data)
        request_handler.get()

        # TODO: Get the destination without accessing private attributes
        destination = request_handler._headers['Location']
        self.assertEqual(url_path_join(request_handler.hub.server.base_url, 'home'), destination)


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
