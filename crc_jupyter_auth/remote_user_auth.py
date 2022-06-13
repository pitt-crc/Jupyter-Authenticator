"""JupyterHub plugins for authenticating users and routing incoming HTTP requests."""

import os

from jupyterhub.auth import Authenticator
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.handlers import BaseHandler
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import Unicode


# noinspection PyAbstractClass
class RemoteUserLoginHandler(BaseHandler):
    """An HTTP request handler for incoming authentication attempts

     HTTP requests that are passed to this handler get redirected
     based on data from the incoming request header. Where incoming traffic
     is redirected is determined by the JupyterHub configuration file.
     See the ``AuthenticatorSettings`` class for default values.

     In all cases, if no username is given in the request header,
     the request is redirected to a 401 error.
     """

    def get(self):
        """Parse an incoming ``get`` request and route users appropriately"""

        # Check for username in header information
        header_name = self.authenticator.header_name
        remote_user = self.request.headers.get(header_name, "").lower().strip()
        if remote_user == "":
            raise web.HTTPError(401)

        # Check for necessary VPN role using request headers
        # Multiple roles are delimited by a semicolon
        header_vpn = self.authenticator.header_vpn
        remote_roles = self.request.headers.get(header_vpn, "").strip().split(';')
        if self.authenticator.required_vpn_role in remote_roles:
            self.redirect(self.authenticator.vpn_redirect)

        # Require the user has an existing home directory
        user = self.user_from_username(remote_user)
        user_home_dir = os.path.expanduser('~{}'.format(remote_user))
        if not os.path.exists(user_home_dir):
            self.redirect(self.authenticator.user_redirect)

        # Facilitate user authentication
        self.set_login_cookie(user)
        self.redirect(url_path_join(self.hub.server.base_url, 'home'))


class AuthenticatorSettings:
    """Defines common, configurable settings for user authentication classes."""

    header_name = Unicode(
        default_value='Cn',
        config=True,
        help="HTTP header to inspect for the authenticated username.")

    header_vpn = Unicode(
        default_value='isMemberOf',
        config=True,
        help="HTTP header to inspect for user VPN role(s).")

    required_vpn_role = Unicode(
        default_value='SAM-SSLVPNSAMUsers',
        config=True,
        help="Required VPN role for accessing the service.")

    user_redirect = Unicode(
        default_value='https://crc.pitt.edu/Access-CRC-Web-Portals',
        config=True,
        help="Url to redirect to if user has no home directory.")

    vpn_redirect = Unicode(
        default_value='https://crc.pitt.edu/Access-CRC-Web-Portals',
        config=True,
        help="Url to redirect to if user is missing necessary VPN role.")


class RemoteUserAuthenticator(AuthenticatorSettings, Authenticator):
    """Accept the authenticated username from the REMOTE_USER HTTP header."""

    def get_handlers(self, app):
        """Return any custom handlers that need to be registered with the parent authenticator

        Args:
            app: The JupyterHub application object, in case it needs to be accessed for info

        Returns:
            A list of authentication handlers and the corresponding urls ``[('/url', Handler), ...]``
        """

        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()


class RemoteUserLocalAuthenticator(AuthenticatorSettings, LocalAuthenticator):
    """
    Accept the authenticated username from the REMOTE_USER HTTP header.
    Derived from LocalAuthenticator for use of features such as adding
    local accounts through the admin interface.
    """

    def get_handlers(self, app):
        """Return any custom handlers that need to be registered with the parent authenticator

        Args:
            app: The JupyterHub application object, in case it needs to be accessed for info

        Returns:
            A list of authentication handlers and the corresponding urls ``[('/url', Handler), ...]``
        """

        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()
