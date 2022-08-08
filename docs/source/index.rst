CRC JupyterHub Authenticator
============================

The ``crc_jupyter_auth`` package is a Jupyter authentication plugin for
redirecting users based on their account status and VPN role.
The utility is based on the
`jhub_remote_user_authenticator <https://github.com/cwaldbieser/jhub_remote_user_authenticator>`_
package which was originally created for more general applications.

How It Works
------------

The authentication plugin checks HTTP header values from incoming authentication
requests and routes users based on the associated header values. The name of the inspected
headers and the routing destination are configurable via the standard JupyterHub
configuration file.

.. toctree::
   :hidden:

   Overview<self>
   install

.. Source files for documenting individual applications are generated
   dynamically by the sphinx-autoapi plugin. These files are added below.

.. toctree::
   :hidden:
   :caption: API Docs:
   :maxdepth: 0
   :glob:

   remote_user_auth

