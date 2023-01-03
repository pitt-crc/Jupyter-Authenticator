"""JupyterHub plugin for authenticating users and routing incoming HTTP requests."""

import sys

from .remote_user_auth import RemoteUserAuthenticator, RemoteUserLocalAuthenticator

if sys.version_info.minor <= 7:
    import pkg_resources
    __version__ = pkg_resources.get_distribution(__package__).version

else:
    import importlib.metadata
    __version__ = importlib.metadata.version(__package__)
