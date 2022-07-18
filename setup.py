"""Installation setup file for the ``crc_jupyter_auth`` package."""

import re
from pathlib import Path

from setuptools import find_packages, setup


def get_requirements():
    """Return a list of package dependencies"""

    requirements_path = Path(__file__).parent / 'requirements.txt'
    with requirements_path.open() as req_file:
        return req_file.read().splitlines()


def get_version():
    """Return the semantic package version"""

    init_path = Path(__file__).resolve().parent / 'apps/__init__.py'
    init_text = init_path.read_text()

    version_regex = re.compile("__version__ = '(.*?)'")
    version = version_regex.findall(init_text)[0]

    return version


setup(
    name='crc_jupyter_auth',
    packages=find_packages(),
    version=get_version(),
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
    install_requires=get_requirements()
)
