# -*- coding: utf-8 -*-

# -- Path setup --------------------------------------------------------------

import sys

from pathlib import Path

# Add the project source code to the working python environment
conf_dir = Path(__file__).resolve().parent
project_root = conf_dir.parent.parent
sys.path.insert(0, str(project_root))

# -- Project information -----------------------------------------------------

from crc_jupyter_auth import __version__  # , __author__, __copyright__

project = u'CRC JupyterHub Authenticator'
# copyright = __copyright__
# author = __author__
release = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx_copybutton',
]

# Don't include code prompts when copying python code
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['templates']

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = 'en'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'