"""Sphinx configuration for ditto documentation."""

from __future__ import annotations

import sys
from importlib.metadata import version as _pkg_version
from pathlib import Path

# -- Path setup ---------------------------------------------------------------
# Add the src directory to sys.path so Sphinx can import the package.
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# -- Project information ------------------------------------------------------
project = "ditto"
copyright = "2026, Nolan MacDonald. All Rights Reserved"  # noqa: A001
author = "Nolan MacDonald"
# Derive release from the installed package to avoid version drift.
release = _pkg_version("ditto")

# -- General configuration ----------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Napoleon (NumPy docstring) settings --------------------------------------
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Autodoc settings ---------------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
}
autosummary_generate = True

# -- Intersphinx mapping ------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
}

# -- HTML output options ------------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

html_logo = "_static/logo/icon.svg"
html_favicon = "_static/logo/icon.svg"

html_theme_options = {
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    "footer_start": ["footer-logo", "copyright"],
    "footer_center": [],
    "footer_end": [],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/nolmacdonald/ditto",
            "icon": "fa-brands fa-github",
        },
    ],
    "use_edit_page_button": False,
    "show_toc_level": 2,
    "navigation_with_keys": False,
    "pygments_light_style": "default",
    "pygments_dark_style": "monokai",
}

html_context = {
    "github_user": "nolmacdonald",
    "github_repo": "ditto",
    "github_version": "main",
    "doc_path": "docs",
}
