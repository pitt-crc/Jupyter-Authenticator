#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Juptyer Development Team.
# Distributed under the terms of the Modified BSD License.

# -----------------------------------------------------------------------------
# Minimal Python version sanity check (from IPython/Jupyterhub)
# -----------------------------------------------------------------------------


import sys

from setuptools import setup

from version import __version__

setup_args = dict(
    name='jhub_remote_user_authenticator',
    packages=['jhub_remote_user_authenticator'],
    version=__version__,
    description='A Jupyterhub Authenticator customized for the Center for Research Computing.',
    long_description='Based on the jhub_remote_user_authenticator built by Carl (https://github.com/cwaldbieser) and extended by the CRC',
    url='https://github.com/cwaldbieser/jhub_remote_user_authenticator',
    license='GPLv3',
    platforms='Linux, Mac OS X',
    keywords=['Interactive', 'Interpreter', 'Shell', 'Web'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    data_files=[('.', ['version.py'])],
)

# setuptools requirements
if 'setuptools' in sys.modules:
    setup_args['install_requires'] = install_requires = []
    install_requires.append('jupyterhub')

setup(**setup_args)
