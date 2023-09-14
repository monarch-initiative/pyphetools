import os
import sys



# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# General information about the project.
project = u'pyphetools'
copyright = u'2023'
author = u'Peter Robinson, Daniel Danis'
release = '0.2.1dev'



# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

pyphetools_src = os.path.abspath(os.path.join('..', 'src'))
sys.path.insert(0, pyphetools_src)
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Autodoc setup ------------------------------------------------------------

autodoc_member_order = 'bysource'

# -- Doctest setup ------------------------------------------------------------

doctest_path = [pyphetools_src]
doctest_test_doctest_blocks = ""

# Nothing special here
doctest_global_setup = """
"""

source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'


# -- Intersphinx setup --------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    # TODO - change to stable when we arrive there
    "hpotk": ("https://thejacksonlaboratory.github.io/hpo-toolkit/latest/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "seaborn": ("https://seaborn.pydata.org/", None),
}

# -- Sphinx copybutton setup --------------------------------------------------
# Exclude `>>>` when copying the cell
copybutton_exclude = '.linenos, .gp'

# -- Options for HTML output --------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
pygments_style = 'sphinx'
html_theme = "sphinx_rtd_theme"
# html_theme_options = {}
language = 'en'



html_static_path = ['_static']
# html_style = 'css/isopret.css'
html_css_files = ['pyphetools.css']



# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'pyphetools'

