Installation and Setup
======================

Use the following instructions to install and configure the **crc_jupyter_auth** package.

Installing the package
----------------------

Download the source code and install the package using the ``pip`` package manager:

.. code-block:: bash

   git clone https://github.com/pitt-crc/Jupyter-Authenticator.git
   pip install Jupyter-Authenticator

Older versions can be installed by checking out the appropriate release tag via ``git``:

.. code-block:: bash

   cd Jupyter-Authenticator
   git fetch
   git checkout tags/[RELEASETAG]
   pip install .

Configuration
-------------

In the *jupyterhub_config.py* file used to configure your Jupyter installation,
update the ``authenticator_class`` option to reflect the installed package.

.. code-block:: python

   c.JupyterHub.authenticator_class = 'crc_jupyter_auth.RemoteUserAuthenticator'

Alternatively, you can use ``RemoteUserLocalAuthenticator``:

.. code-block:: python

   c.JupyterHub.authenticator_class = 'crc_jupyter_auth.RemoteUserLocalAuthenticator'

 ``RemoteUserLocalAuthenticator`` class provides the same authentication functionality
but is derived from Jupyter's builtin ``LocalAuthenticator`` class. This provides extra
features such as the ability to add local accounts through the admin interface.

The authenticator works by checking for the authenticated username in the HTTP header ``"Cn"``.
If found, and not blank, the client will be logged in as that user.
The HTTP header names and failure redirects are configurable.
See the ``AuthenticatorSettings`` class for more details.

Architecture and Security Recommendations
-----------------------------------------

This authenticator relies on HTTP headers that can be spoofed by a malicious client.
To protect against this, an authenticating proxy should be placed in front
of Jupyterhub. The JupyterHub daemon should **only** be accessible from the proxy
and **never** directly accessible by a client.

The authenticating proxy should remove any HTTP headers from incoming
requests and only apply the header to proxied requests
that have been properly authenticated.
