# CRC JupyterHub Authenticator
[![](https://app.codacy.com/project/badge/Grade/5e1a00bf8dbe4daf8275fc88ce748ea6)](https://app.codacy.com/gh/pitt-crc/Jupyter-Authenticator/dashboard)
[![](https://app.codacy.com/project/badge/Coverage/5e1a00bf8dbe4daf8275fc88ce748ea6)](https://app.codacy.com/gh/pitt-crc/Jupyter-Authenticator/dashboard)

The `crc_jupyter_auth` package is a Jupyter authentication plugin for redirecting users based on their account status and VPN role.
The utility is based on the [jhub_remote_user_authenticator](https://github.com/cwaldbieser/jhub_remote_user_authenticator)
package originally created for more general applications.
The CRC version builds on the original utility by providing significantly improved test coverage and a refined set of configuration options.

## How It Works

The authentication plugin checks incoming authentication requests and routes users based on the associated header values.
The name of the inspected headers and the routing destination are configurable via the standard Jupyter config file.

## Installation and Setup

The `crc_jupyter_auth` package can be installable via the `pip` package manager.

```bash
pip install crc-jupyter-auth
```

After installing the package, you will need to update the `authenticator_class` option in your Jupyter configuration file.
To enable basic authentication capabilities and request routing, specify the `RemoteUserAuthenticator` class:

```bash
c.JupyterHub.authenticator_class = "crc_jupyter_auth.RemoteUserAuthenticator"
```

To enable the same functionality plus local account management, use `RemoteUserLocalAuthenticator`:

```bash
c.JupyterHub.authenticator_class = "crc_jupyter_auth.RemoteUserLocalAuthenticator"
```

The `RemoteUserLocalAuthenticator` class provides the same authentication functionality
as `RemoteUserAuthenticator` but is derived from Jupyter's built-in `LocalAuthenticator` class. 
This provides extra features such as the ability to add local accounts through the admin interface.

## Package Configuration

The authenticator works by fetching the authenticated username from the HTTP header `Cn`.
If found, and not blank, the client will be logged in as that user.
Otherwise, the user is redirected.

The HTTP header names and failure redirects are configurable via the Jupyter settings file.
Setting names and default values are provided in the table below:

| Setting Name            | Default        | Description                                                                                   |
|-------------------------|----------------|-----------------------------------------------------------------------------------------------|
| `username_header`       | `"Cn"`         | HTTP header name to inspect for the authenticated username         -                          |
| `vpn_header`            | `"isMemberOf"` | HTTP header name to inspect for the user VPN role(s).                                         |
| `required_vpn_role`     | `""`           | Required VPN role for accessing the service. Ignored if an empty string.                      |
| `missing_role_redirect` | `""`           | Redirect URL if the user is missing the required VPN header. Defaults to 404 if empty string. |

To modify a settings value, use the `c.Authenticator` object in the configuration file.
For example:

```python
c.Authenticator.missing_role_redirect = "https://my.redirect.domain"
```

If your system assigns multiple VPN roles to users and more than a single role is reported by the header
`vpn_header`, the VPN roles should be provided in the header as a semicolon-delimited list
(e.g., `role1;role2`).

## Architecture and Security Recommendations

This authenticator relies on HTTP headers that can be spoofed by a malicious client.
To protect against this, an authenticating proxy should be placed in front
of Jupyterhub. The JupyterHub daemon should **only** be accessible from the proxy
and **never** directly accessible by a client.

The authenticating proxy should remove any HTTP headers from incoming
requests and only apply headers to proxied requests that have been properly authenticated.
