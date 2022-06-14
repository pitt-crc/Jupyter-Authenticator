"""Test HTTP request routing by the ``RemoteUserLoginHandler`` class."""

from unittest import TestCase

from jupyterhub.objects import Server
from tornado.httputil import HTTPServerRequest, HTTPHeaders, HTTPConnection
from tornado.web import Application

from crc_jupyter_auth.remote_user_auth import RemoteUserLoginHandler, RemoteUserAuthenticator


class RequestRouting(TestCase):
    """Test the routing of HTTP authentication requests"""

    @staticmethod
    def create_http_request(authenticator, header_data):
        """Create a mock application and an HTTP request for that application"""

        # Create a tornado application running a jupyterhub server
        application = Application(hub=Server(), authenticator=authenticator)

        # HTTP connections are used by the application to write HTTP responses
        # The `set_close_callback` method is required to exist by JupyterHub
        connection = HTTPConnection()
        connection.set_close_callback = lambda x: None

        # Return an HTTP request reflecting the given header data
        headers = HTTPHeaders(header_data)
        request = HTTPServerRequest(headers=headers, connection=connection)
        return application, request

    # This isn't a real test. I just need something to run the create_http_request
    # while I figure out the tornado / jupyter frameworks
    def runTest(self) -> None:
        authenticator = RemoteUserAuthenticator()
        application, request = self.create_http_request(authenticator, {'Cn': 'username'})
        request_handler = RemoteUserLoginHandler(application=application, request=request)

        request_handler.get()
