# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath(".."))  # NOQA: E402

import sphinx_rtd_theme


# -- Project information -----------------------------------------------------

project = "Pysmith"
copyright = "2020, Dave Korhumel"
author = "Dave Korhumel"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# A list of imports to mock when autodoc imports modules
autodoc_mock_imports = [
    "frontmatter",
    "jinja2",
    "markdown2",
    "rjsmin",
    "sass",
]

# The external mappings for intersphinx
intersphinx_mapping = {
    "jinja2": ("https://jinja.palletsprojects.com/en/2.11.x/", None),
    "python3": ("https://docs.python.org/3", None),
    "rjsmin": ("http://opensource.perlig.de/rjsmin", None),
    "sass": ("https://sass.github.io/libsass-python/", None),
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# The configuration for the theme
html_theme_options = {
    "collapse_navigation": False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
