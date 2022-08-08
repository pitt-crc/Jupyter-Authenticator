"""Package installation logic"""

import re
from pathlib import Path

from setuptools import setup, find_packages

PACKAGE_REQUIREMENTS = Path(__file__).parent / 'requirements.txt'
DOCUMENTATION_REQUIREMENTS = Path(__file__).parent / 'docs' / 'requirements.txt'


def get_long_description():
    """Return a long description of tha parent package"""

    readme_file = Path(__file__).parent / 'README.md'
    return readme_file.read_text()


def get_requirements(path):
    """Return a list of package dependencies"""

    with path.open() as req_file:
        return req_file.read().splitlines()


def get_meta():
    """Return package metadata including the:
        - author
        - version
        - license
    """

    init_path = Path(__file__).resolve().parent / 'apps/__init__.py'
    init_text = init_path.read_text()

    version_regex = re.compile("__version__ = '(.*?)'")
    version = version_regex.findall(init_text)[0]

    author_regex = re.compile("__author__ = '(.*?)'")
    author = author_regex.findall(init_text)[0]

    license_regex = re.compile("__license__ = '(.*?)'")
    license_type = license_regex.findall(init_text)[0]

    return author, version, license_type


_author, _version, _license = get_meta()
setup(
    name='crc_jupyter_auth',
    description='Jupyter authentication plugin that checks for account existence and VPN permissions.',
    version=_version,
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=get_requirements(PACKAGE_REQUIREMENTS),
    extras_require={
        'docs': get_requirements(DOCUMENTATION_REQUIREMENTS),
        'tests': ['coverage'],
    },
    author=_author,
    keywords='Pitt, CRC, HPC, wrappers',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    license=_license,
    classifiers=[
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
