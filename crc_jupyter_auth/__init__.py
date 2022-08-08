"""JupyterHub plugin for authenticating users and routing incoming HTTP requests."""

from .remote_user_auth import RemoteUserAuthenticator, RemoteUserLocalAuthenticator

__version__ = '0.3.0'
__author__ = 'Pitt Center for Research Computing'
__license__ = 'GNU GPL V3'
