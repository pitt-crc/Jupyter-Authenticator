Installation and Setup
======================

Please read through the **entire** installation process to ensure a stable and secure setup.

Installing the package
----------------------

Download the source code and install the package using the ``pip`` package manager:

.. code-block:: bash

   git clone https://github.com/pitt-crc/Jupyter-Authenticator.git
   pip install Jupyter-Authenticator

Older versions can be installed by checking out the appropriate tag with ``git``:

.. code-block:: bash

   cd Jupyter-Authenticator
   git fetch
   git checkout tags/[RELEASETAG]
   pip install .


Configuration
-------------

You will need to edit your ``jupyterhub_config.py`` file to add the authenticator class:

.. code-block:: python

   c.JupyterHub.authenticator_class = 'crc_jupyter_auth.RemoteUserAuthenticator'

Alternatively, you can use ``RemoteUserLocalAuthenticator``:

.. code-block:: python

   c.JupyterHub.authenticator_class = 'crc_jupyter_auth.RemoteUserLocalAuthenticator'

This provides the same authentication functionality but is derived from
``LocalAuthenticator`` and therefore provides features such as the ability
to add local accounts through the admin interface if configured to do so.

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
