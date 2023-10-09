"""Test HTTP request routing by the ``RemoteUserLoginHandler`` class."""

from datetime import datetime
from typing import Type
from unittest import TestCase
from unittest.mock import MagicMock, patch

from jupyterhub.auth import Authenticator
from jupyterhub.objects import Hub
from jupyterhub.orm import User
from jupyterhub.utils import new_token, url_path_join
from tornado import web
from tornado.httputil import HTTPConnection, HTTPHeaders, HTTPServerRequest
from tornado.web import Application

from crc_jupyter_auth import RemoteUserAuthenticator
from crc_jupyter_auth.remote_user_auth import AuthenticatorSettings, RemoteUserLoginHandler


class TestUtils:
    """Base class for general testing/setup utilities"""

    @staticmethod
    def create_http_request_handler(
        header_data: dict,
        authenticator_type: Type[Authenticator] = RemoteUserAuthenticator
    ) -> RemoteUserLoginHandler:
        """Create a mock HTTP request handler

        Create a mock HTTP request reflecting the given HTTP header data and
        return an instance of the ``RemoteUserLoginHandler`` class for handling
        that request.

        Args:
            header_data: Head data to include in the returned request
            authenticator_type: The class of authenticator to use when handling the incoming request

        Returns:
            An instance of the ``RemoteUserLoginHandler`` class
        """

        # Create a tornado application running a jupyterhub server
        application = Application(hub=Hub(), authenticator=authenticator_type(), cookie_secret='secret')

        # HTTP connections are used by the application to write HTTP responses
        # The `set_close_callback` method is required to exist by JupyterHub
        connection = HTTPConnection()
        connection.set_close_callback = lambda x: None

        # Return an HTTP request reflecting the given header data
        headers = HTTPHeaders(header_data)
        request = HTTPServerRequest(headers=headers, connection=connection)
        return RemoteUserLoginHandler(application=application, request=request)


class RoutingByUsername(TestUtils, TestCase):
    """Test missing or invalid username information results in an HTTP 401 error"""

    def test_missing_username_401(self) -> None:
        """Test for a 401 error when the username is missing from the HTTP header"""

        # Create an HTTP request with the username missing from the header information
        request_handler = self.create_http_request_handler(dict())

        with self.assertRaises(web.HTTPError) as http_exception:
            request_handler.get()

        self.assertEqual(401, http_exception.exception.status_code)

    def test_blank_username_401(self) -> None:
        """Test for a 401 error when the username is blank"""

        # Create an HTTP request with a blank username
        header_data = {AuthenticatorSettings().username_header: ''}

        request_handler = self.create_http_request_handler(header_data)
        with self.assertRaises(web.HTTPError) as http_exception:
            request_handler.get()

        self.assertEqual(401, http_exception.exception.status_code)


class RoutingByVpnRole(TestUtils, TestCase):
    """Test traffic with missing or invalid VPN roles redirect to the URL configured in settings"""

    def test_missing_vpn_role_404(self) -> None:
        """Test requests that are missing VPN information are redirected to a 404"""

        # Mock an incoming request that has username info but is missing VPN role info
        request_data = {AuthenticatorSettings().username_header: 'username'}

        # Configure settings in the request handler to require a role and forward to a 404
        request_handler = self.create_http_request_handler(request_data)
        request_handler.authenticator.required_vpn_role = 'REQUIRED_ROLE'

        # Test the user is given a 404
        with self.assertRaises(web.HTTPError) as http_exception:
            request_handler.get()

        self.assertEqual(404, http_exception.exception.status_code)

    @patch.object(RemoteUserLoginHandler, 'redirect', return_value=None)
    def test_missing_vpn_role_redirect(self, mock_redirect_call: MagicMock) -> None:
        """Test requests that are missing VPN information are redirected to the ``missing_role_redirect`` URL"""

        # Mock an incoming request that has username info but is missing VPN role info
        request_data = {AuthenticatorSettings().username_header: 'username'}

        # Configure settings in the request handler to require a role and forward to a URL
        request_handler = self.create_http_request_handler(request_data)
        request_handler.authenticator.required_vpn_role = 'REQUIRED_ROLE'
        request_handler.authenticator.missing_role_redirect = 'www.google.com'
        request_handler.get()

        mock_redirect_call.assert_called_once_with(request_handler.authenticator.missing_role_redirect)

    def test_incorrect_role_404(self) -> None:
        """Test requests with invalid VPN information are redirected to a 404"""

        # Mock an incoming request that has username and VPN role info
        settings = AuthenticatorSettings()
        request_data = {settings.username_header: 'username', settings.vpn_header: 'incorrect_role'}

        # Configure settings in the request handler to require a role and forward to a 404
        request_handler = self.create_http_request_handler(request_data)
        request_handler.authenticator.required_vpn_role = 'correct_vpn_role'

        # Test the user is given a 404
        with self.assertRaises(web.HTTPError) as http_exception:
            request_handler.get()

        self.assertEqual(404, http_exception.exception.status_code)

    @patch.object(RemoteUserLoginHandler, 'redirect', return_value=None)
    def test_incorrect_role_redirect(self, mock_redirect_call: MagicMock) -> None:
        """Test requests with invalid VPN information are redirected to the ``missing_role_redirect`` URL"""

        # Mock an incoming request that has username and VPN role info
        settings = AuthenticatorSettings()
        request_data = {settings.username_header: 'username', settings.vpn_header: 'incorrect_role'}

        # Configure settings in the request handler to require a role and forward to a 404
        request_handler = self.create_http_request_handler(request_data)
        request_handler.authenticator.required_vpn_role = 'correct_vpn_role'
        request_handler.authenticator.missing_role_redirect = 'www.google.com'
        request_handler.get()

        mock_redirect_call.assert_called_once_with(request_handler.authenticator.missing_role_redirect)


class SuccessfulLoginRouting(TestUtils, TestCase):
    """Test the routing of users after a successful login"""

    @staticmethod
    def mock_user() -> User:
        """Create a jupyterhub user object with mock/dummy data"""

        return User(id=1, name='mock_user', admin=False, created=datetime.now(), cookie_id=new_token())

    @patch.object(RemoteUserLoginHandler, 'redirect', return_value=None)
    @patch.object(RemoteUserLoginHandler, 'user_from_username', return_value=mock_user())
    def test_user_is_redirected(self, mock_user: User, mock_redirect_call: MagicMock) -> None:
        """Test the user is redirected to the jupyterhub server"""

        request_data = {AuthenticatorSettings().username_header: 'username'}
        request_handler = self.create_http_request_handler(request_data)
        request_handler.get()

        expected_url = url_path_join(request_handler.hub.server.base_url, 'home')
        mock_redirect_call.assert_called_once_with(expected_url)
