#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

from os import path

parent_dir = path.abspath(path.dirname(__file__))
version_path = path.join(parent_dir, 'version.py')

# Get the current package version.
version_ns = {}
with open(version_path) as version_file:
    exec(version_file.read(), {}, version_ns)

setup_args = dict(
    name='crc_jupyter_auth',
    packages=['crc_jupyter_auth'],
    version=version_ns['__version__'],
    description='A custom JupyterHub authenticator built for the Pitt Center for Research Computing.',
    license='GPLv3',
    platforms='Linux',
    keywords=['Interactive', 'Interpreter', 'Shell', 'Web'],
    classifiers=[
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    data_files=[('.', ['version.py'])],
    requirements=['jupyterhub']
)
