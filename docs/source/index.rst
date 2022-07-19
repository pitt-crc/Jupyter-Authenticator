CRC JupyterHub Authenticator
============================

The ``crc_jupyter_auth`` package is a JupyterHub authentication plugin designed
specifically for the Pitt Center for Research Computing. It is based off the
`jhub_remote_user_authenticator <https://github.com/cwaldbieser/jhub_remote_user_authenticator>`_
which was originally created for more general applications.

How It Works
------------

The authentication plugin checks HTTP header values from incoming authentication
requests and routes users based on the header value. The name of the inspected
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

   autoapi/crc_jupyter_auth/**/index

