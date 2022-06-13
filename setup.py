"""Installation setup file for the ``crc_jupyter_auth`` package."""

from os import path

from setuptools import find_packages, setup

parent_dir = path.abspath(path.dirname(__file__))
version_path = path.join(parent_dir, 'version.py')
requirements_path = path.join(parent_dir, 'requirements.txt')

# Get the current package version.
version_ns = {}
with open(version_path) as version_file:
    exec(version_file.read(), {}, version_ns)

# Get a list of package dependencies
with open(requirements_path) as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name='crc_jupyter_auth',
    packages=find_packages(),
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
    install_requires=requirements
)
