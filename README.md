# Jupyterhub REMOTE_USER Authenticator

Custom JupyterHub authenticator built for the CRC based on the
[hub_remote_user_authenticator](https://github.com/cwaldbieser/jhub_remote_user_authenticator) tool.

## Architecture and Security Recommendations

This authenticator relies on HTTP headers that can be spoofed by a malicious client.
To protect against this, an authenticating proxy be placed in front
of Jupyterhub. The JupyterHub daemon should **only** be accessible from the proxy
and **never** directly accessible by a client.

The authenticating proxy should remove any HTTP headers from incoming
requests and only applies the header to proxied requests
that have been properly authenticated.

## Installation

A copy of the latest package release is maintained in the `latest` branch of this repository and is installable via `pip`

```bash
pip install git+https://github.com/pitt-crc/jhub_remote_user_authenticator.git@latest
```

See the release section of the GitHub repository for older package versions and release notes.

You will need to edit your ``jupyterhub_config.py`` file to set the authenticator 
class:

```python
c.JupyterHub.authenticator_class = 'jhub_remote_user_authenticator.remote_user_auth.RemoteUserAuthenticator'
```

You should be able to start jupyterhub. The "/hub/login" resource
will look for the authenticated username in the HTTP header "REMOTE_USER".
If found, and not blank, you will be logged in as that user.

Alternatively, you can use `RemoteUserLocalAuthenticator`:

```python
c.JupyterHub.authenticator_class = 'jhub_remote_user_authenticator.remote_user_auth.RemoteUserLocalAuthenticator'
```

This provides the same authentication functionality but is derived from
`LocalAuthenticator` and therefore provides features such as the ability
to add local accounts through the admin interface if configured to do so.

## Configuration

The HTTP header names and failure redirects are configurable.  
See the ``AuthenticatorSettings`` class for more details.

Note that NGINX, a popular
proxy, drops headers that contain an underscore by default. See
http://nginx.org/en/docs/http/ngx_http_core_module.html#underscores_in_headers
for details.
   
## Release Procedures

Only package versions marked as a release should be sent to deployment. To create a new release:
 1. Edit the package version in `version.py`.
 2. Tag the git repo with the new version number.
 3. Create a new GitHub release using the tagged version. Make sure to include a description of any changes.

Once a new release is tagged, the content of the `latest` branch will  be updated automatically by 
git GitHub actions to reflect the content of that release.
