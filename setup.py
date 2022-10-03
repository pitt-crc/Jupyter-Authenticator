"""Package installation logic"""

import re
from pathlib import Path

from setuptools import find_packages, setup

_file_dir = Path(__file__).resolve().parent


def get_long_description():
    """Return a long description of tha parent package"""

    readme_file = Path(__file__).parent / 'README.md'
    return readme_file.read_text()


def get_requirements():
    """Return a list of package dependencies"""

    requirements_file = _file_dir / 'requirements.txt'
    return requirements_file.read_text().splitlines()


def get_meta(value):
    """Return package metadata as defined in the init file

    Args:
        value: The metadata variable to return a value for
    """

    init_path = _file_dir / 'crc_jupyter_auth' / '__init__.py'
    init_text = init_path.read_text()

    regex = re.compile(f"__{value}__ = '(.*?)'")
    value = regex.findall(init_text)[0]
    return value


setup(
    name='crc_jupyter_auth',
    description='Jupyter authentication plugin that checks for account existence and VPN permissions.',
    version=get_meta('version'),
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=get_requirements(),
    extras_require={
        'tests': ['coverage'],
    },
    author=get_meta('author'),
    keywords='Pitt, CRC, HPC, wrappers',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    license=get_meta('license'),
    classifiers=[
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
