"""The ``remote_user_auth`` module extends the default user authentication
classes defined by the ``jupyterhub`` package. It is responsible for
handling HTTP request routing based on user authentication status.

Module Contents
---------------
"""

from jupyterhub.auth import Authenticator, LocalAuthenticator
from jupyterhub.handlers import BaseHandler
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import HasTraits, Unicode


class RemoteUserLoginHandler(BaseHandler):
    """An HTTP request handler for incoming authentication attempts.

     HTTP requests are redirected by this handler based on the incoming
     request header. The redirect destination is determined by the
     JupyterHub configuration file. See the ``AuthenticatorSettings``
     class for default config values.
     """

    def get(self) -> None:
        """Parse an incoming ``get`` request and route users appropriately

        Raises:
            HTTPError: If a valid username cannot be found in the request
            HTTPError: If the user is missing a required VPN role
            HTTPError: If the user does not have an existing home directory
        """

        # Check for a username in the header information
        header_name = self.authenticator.username_header
        remote_user = self.request.headers.get(header_name, "").lower().strip()
        if remote_user == "":
            raise web.HTTPError(401)

        # Check for a required VPN role using request headers
        # Multiple roles are delimited in the request by a semicolon
        header_vpn = self.authenticator.vpn_header
        remote_roles = self.request.headers.get(header_vpn, "").strip().split(';')
        required_role = self.authenticator.required_vpn_role
        if required_role and (required_role not in remote_roles):
            self.redirect_or_raise(self.authenticator.missing_role_redirect)
            return

        # Facilitate user authentication
        user = self.user_from_username(remote_user)
        self.set_login_cookie(user)
        self.redirect_or_raise(url_path_join(self.hub.server.base_url, 'home'))

    def redirect_or_raise(self, url: str, raise_status: int = 404) -> None:
        """Redirect to the given url

        If the URL is None or empty, raise an ``HTTPError``

        Args:
            url: The url to redirect to
            raise_status: Status code for the HTTP error

        Raises:
            HTTPError: If the ``url`` argument is ``False``
        """

        if not url:
            raise web.HTTPError(raise_status)

        self.redirect(url)


class AuthenticatorSettings(HasTraits):
    """Defines common, configurable settings for user authentication classes.

    The value of attributes defined for this class can be modified in
    deployment via the JupyterHub configuration file.
    """

    username_header = Unicode(
        default_value='Cn',
        config=True,
        help="HTTP header to inspect for the authenticated username.")

    vpn_header = Unicode(
        default_value='isMemberOf',
        config=True,
        help="HTTP header to inspect for user VPN role(s).")

    required_vpn_role = Unicode(
        default_value='',
        config=True,
        help="Required VPN role for accessing the service.")

    missing_role_redirect = Unicode(
        default_value='',
        config=True,
        help="Url to redirect to if the user is missing the required VPN role.")


class RemoteUserAuthenticator(AuthenticatorSettings, Authenticator):
    """Base class for implementing an authentication provider for JupyterHub.

    Handles the authentication of users and routes traffic from successfully
    authenticated users using the ``RemoteUserLoginHandler``.
    """

    def get_handlers(self, app: web.Application) -> list:
        """Return any custom handlers that need to be registered with the parent authenticator

        Args:
            app: The JupyterHub application object, in case it needs to be accessed for info

        Returns:
            A list of authentication handlers and the corresponding urls: ``[('/url', Handler), ...]``
        """

        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args) -> None:
        """Authenticate a user with login form data

        See the parent class for requirements on implementing this method.

        Raises:
            NotImplementedError: Every time the method is called
        """

        # User account authentication is expected to be handled upstream
        # before the request reaches this class
        raise NotImplementedError()  # pragma: no cover


class RemoteUserLocalAuthenticator(AuthenticatorSettings, LocalAuthenticator):
    """Base class for authenticators that work with local Linux/UNIX users

    This class is similar to the ``RemoteUserAuthenticator`` class except it
    can check for local user accounts and attempt to create them if they don't
    exist.

    Successfully authenticated users are routed using the ``RemoteUserLoginHandler``.
    """

    def get_handlers(self, app: web.Application) -> list:
        """Return any custom handlers that need to be registered with the parent authenticator

        Args:
            app: The JupyterHub application object, in case it needs to be accessed for info

        Returns:
            A list of authentication handlers and the corresponding urls: ``[('/url', Handler), ...]``
        """

        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args) -> None:
        """Authenticate a user with login form data

        See the parent class for requirements on implementing this method.

        Raises:
            NotImplementedError: Every time the method is called
        """

        # User account authentication is expected to be handled upstream
        # before the request reaches this class
        raise NotImplementedError()  # pragma: no cover
