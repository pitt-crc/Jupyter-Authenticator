"""Test HTTP request routing by the ``RemoteUserLoginHandler`` class."""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from jupyterhub.auth import Authenticator
from jupyterhub.objects import Server
from tornado import web
from tornado.httputil import HTTPConnection, HTTPHeaders, HTTPServerRequest
from tornado.web import Application

from crc_jupyter_auth import RemoteUserAuthenticator
from crc_jupyter_auth.remote_user_auth import RemoteUserLoginHandler


class TestUtils:

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


class RoutingByUsername(TestUtils, TestCase):
    """Test missing or invalid username information results in a 401 HTTP error"""

    def test_missing_username_401(self) -> None:
        """Test for a 401 error when the username is missing from the HTTP header"""

        # Create and handle an HTTP request with the username missing from the header information
        request_handler = self.create_http_request_handler(RemoteUserAuthenticator(), dict())
        with self.assertRaises(web.HTTPError) as http_exception:
            request_handler.get()

        self.assertEqual(401, http_exception.exception.status_code)

    def test_blank_username_401(self) -> None:
        """Test for a 401 error when the username is blank"""

        # Create an HTTP request with a blank username
        authenticator = RemoteUserAuthenticator()
        request_handler = self.create_http_request_handler(authenticator, {authenticator.username_header: ''})

        with self.assertRaises(web.HTTPError) as http_exception:
            request_handler.get()

        self.assertEqual(401, http_exception.exception.status_code)


class RoutingByVpnRole(TestUtils, TestCase):
    """Test missing or invalid VPN roles redirects to the configured URL"""

    @patch.object(RemoteUserLoginHandler, 'redirect', return_value=None)
    def test_missing_vpn_role(self, mock_redirect_call: MagicMock) -> None:
        """Test users are redirected to the ``missing_role_redirect`` URL for missing VPN roles"""

        # Create an HTTP request with a valid username but missing VPN information
        authenticator = RemoteUserAuthenticator()
        request_handler = self.create_http_request_handler(authenticator, {authenticator.username_header: 'username'})
        request_handler.get()

        mock_redirect_call.assert_called_once_with(authenticator.missing_role_redirect)

    @patch.object(RemoteUserLoginHandler, 'redirect', return_value=None)
    def test_incorrect_vpn_role(self, mock_redirect_call: MagicMock) -> None:
        """Test users are redirected to the ``missing_role_redirect`` URL for incorrect VPN roles"""

        # Create an HTTP request with a valid username and invalid VPN information
        authenticator = RemoteUserAuthenticator()
        header_data = {
            authenticator.username_header: 'username',
            authenticator.vpn_header: 'FAKEROLE1;FAKEROLE2'
        }

        request_handler = self.create_http_request_handler(authenticator, header_data)
        request_handler.get()

        # Make sure the user was redirected to the correct location
        mock_redirect_call.assert_called_once_with(authenticator.missing_role_redirect)

    def test_blank_vpn_settings_404(self) -> None:
        """Test a 404 is raised when ``missing_role_redirect`` is configured to a blank string"""

        # Create an HTTP request with a valid username but missing VPN information
        # This will cause a redirect to the ``missing_role_redirect`` URL
        authenticator = RemoteUserAuthenticator()
        request_handler = self.create_http_request_handler(authenticator, {authenticator.username_header: 'username'})

        # Modify the ``missing_role_redirect`` URL to be a blank string and process the request
        request_handler.authenticator.missing_role_redirect = ''
        with self.assertRaises(web.HTTPError) as http_exception:
            request_handler.get()

        self.assertEqual(404, http_exception.exception.status_code)


class RoutingByHomeDir(TestUtils, TestCase):
    @patch('os.path.exists', lambda path: False)
    @patch.object(RemoteUserLoginHandler, 'redirect', return_value=None)
    def test_missing_home_dir_redirect(self, mock_redirect_call: MagicMock) -> None:
        """Test users are redirected to the ``missing_user_redirect`` URL if they do not have a home directory"""

        authenticator = RemoteUserAuthenticator()
        header_data = {
            authenticator.username_header: 'username',
            authenticator.vpn_header: authenticator.required_vpn_role
        }

        request_handler = self.create_http_request_handler(authenticator, header_data)
        request_handler.get()

        mock_redirect_call.assert_called_once_with(authenticator.missing_user_redirect)

    @patch('os.path.exists', lambda path: False)
    def test_blank_home_dir_settings_404(self) -> None:
        """Test a 404 is raised when ``missing_user_redirect`` is configured to a blank string"""

        authenticator = RemoteUserAuthenticator()
        header_data = {
            authenticator.username_header: 'username',
            authenticator.vpn_header: authenticator.required_vpn_role
        }

        # Modify the ``missing_role_redirect`` URL to be a blank string and process the request
        request_handler = self.create_http_request_handler(authenticator, header_data)
        request_handler.authenticator.missing_user_redirect = ''

        with self.assertRaises(web.HTTPError) as http_exception:
            request_handler.get()

        self.assertEqual(404, http_exception.exception.status_code)
