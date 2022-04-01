import os

from jupyterhub.auth import Authenticator
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.handlers import BaseHandler
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import Unicode


class RemoteUserLoginHandler(BaseHandler):
    """Attempt user login using data from incoming request header"""

    def get(self):
        # Check for username in header information
        header_name = self.authenticator.header_name
        remote_user = self.request.headers.get(header_name, "").lower()
        if remote_user == "":
            raise web.HTTPError(401)

        # Check for necessary VPN role using request headers
        header_vpn = self.authenticator.header_vpn
        remote_roles = self.request.headers.get(header_vpn, "")
        required_vpn_role = self.authenticator.required_vpn_role
        if required_vpn_role != remote_roles:
            self.redirect("https://crc.pitt.edu/node/1041")

        # Require the user has an existing home directory
        user = self.user_from_username(remote_user)
        user_home_dir = os.path.expanduser('~{}'.format(remote_user))
        if not os.path.exists(user_home_dir):
            self.redirect("https://crc.pitt.edu/node/1042")

        # Facilitate user authentication
        self.set_login_cookie(user)
        self.redirect(url_path_join(self.hub.server.base_url, 'home'))


class AuthenticatorSettings:
    """Defines common, configurable settings for user authenticators."""

    header_name = Unicode(
        default_value='Cn',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")

    header_vpn = Unicode(
        default_value='isMemberOf',
        config=True,
        help="""HTTP header to inspect for user VPN role(s).""")

    required_vpn_role = Unicode(
        default_value='SAM-SSLVPNSAMUsers',
        config=True,
        help="""Required VPN role for accessing the service.""")

    user_redirect = Unicode(
        default_value='https://crc.pitt.edu/node/1042',
        config=True,
        help="""Url to redirect to if user has no home directory.""")

    vpn_redirect = Unicode(
        default_value='https://crc.pitt.edu/node/1041',
        config=True,
        help="""Url to redirect to if user is missing necessary VPN role.""")


class RemoteUserAuthenticator(AuthenticatorSettings, Authenticator):
    """Accept the authenticated user name from the REMOTE_USER HTTP header."""

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()


class RemoteUserLocalAuthenticator(AuthenticatorSettings, LocalAuthenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    Derived from LocalAuthenticator for use of features such as adding
    local accounts through the admin interface.
    """

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()
