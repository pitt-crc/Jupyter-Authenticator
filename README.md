# CRC JupyterHub Authenticator
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/5e1a00bf8dbe4daf8275fc88ce748ea6)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pitt-crc/Jupyter-Authenticator&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/5e1a00bf8dbe4daf8275fc88ce748ea6)](https://www.codacy.com/gh/pitt-crc/Jupyter-Authenticator/dashboard?utm_source=github.com&utm_medium=referral&utm_content=pitt-crc/Jupyter-Authenticator&utm_campaign=Badge_Coverage)
[![Tests](https://github.com/pitt-crc/Jupyter-Authenticator/actions/workflows/Unittests.yml/badge.svg)](https://github.com/pitt-crc/Jupyter-Authenticator/actions/workflows/Unittests.yml)

The `crc_jupyter_auth` package is a Jupyter authentication plugin for redirecting users
based on their account status and VPN role.  The utility is based on the
[jhub_remote_user_authenticator](https://github.com/cwaldbieser/jhub_remote_user_authenticator)
package originally created for more general applications.

## How It Works

The authentication plugin checks HTTP header values from incoming authentication
requests and routes users based on the associated header values. The name of the inspected
headers and the routing destination are configurable via the standard Jupyter config file.

## Installation and Setup

The `crc_jupyter_auth` package is installable via the `pip` package manager.

```bash
git clone https://github.com/pitt-crc/Jupyter-Authenticator.git
pip install Jupyter-Authenticator
```

Older versions can be installed by checking out the appropriate release tag via `git`:

```bash
cd Jupyter-Authenticator
git fetch
git checkout tags/[RELEASETAG]
pip install .
```

Update the `authenticator_class` option in your Jupyter configuration file to reflect the installed package.
To enable basic authentication capabilities and request routing, specify the `RemoteUserAuthenticator` class:

```bash
c.JupyterHub.authenticator_class = "crc_jupyter_auth.RemoteUserAuthenticator"
```

To enable the same functionality plus local account management, use `RemoteUserLocalAuthenticator`:

```bash
c.JupyterHub.authenticator_class = "crc_jupyter_auth.RemoteUserLocalAuthenticator"
```

The `RemoteUserLocalAuthenticator` class provides the same authentication functionality
as `RemoteUserAuthenticator` but is derived from Jupyter's builtin `LocalAuthenticator` class. 
This provides extra features such as the ability to add local accounts through the admin interface.

## Package Configuration

The authenticator works by fetching the authenticated username from the HTTP header `Cn`.
If found, and not blank, the client will be logged in as that user.
Otherwise, the user is redirected.

The HTTP header names and failure redirects are configurable via the Jupyter settings file.
Setting names and default values are provided in the table below:

| Setting Name            | Default                | Description                                                                                |
|-------------------------|------------------------|--------------------------------------------------------------------------------------------|
| `username_header`       | `"Cn"`                 | HTTP header name to inspect for the authenticated username                                 |
| `vpn_header`            | `"isMemberOf"`         | HTTP header name to inspect for the user VPN role(s).                                      |
| `required_vpn_role`     | `"SAM-SSLVPNSAMUsers"` | Required VPN role for accessing the service.                                               |
| `missing_user_redirect` | `""`                   | Url to redirect to if user has no home directory. Defaults to 404 if empty string.         |
| `missing_role_redirect` | `""`                   | Url to redirect to if user is missing necessary VPN role. Defaults to 404 if empty string. |

## Architecture and Security Recommendations

This authenticator relies on HTTP headers that can be spoofed by a malicious client.
To protect against this, an authenticating proxy should be placed in front
of Jupyterhub. The JupyterHub daemon should **only** be accessible from the proxy
and **never** directly accessible by a client.

The authenticating proxy should remove any HTTP headers from incoming
requests and only apply the header to proxied requests
that have been properly authenticated.
