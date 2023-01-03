"""JupyterHub plugin for authenticating users and routing incoming HTTP requests."""

import importlib.metadata

from .remote_user_auth import RemoteUserAuthenticator, RemoteUserLocalAuthenticator

__version__ = importlib.metadata.version(__package__)
