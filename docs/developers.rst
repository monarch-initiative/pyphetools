.. _developers:


==============
For developers
==============

Updating package in PyPI
^^^^^^^^^^^^^^^^^^^^^^^^
We have installed the package in the Python Package Index (pypi) at [pyphentools](https://pypi.org/project/pyphetools/).
To update the version, first make sure the build and twine packages are installed (if necessary).


.. code-block:: shell
   
   python3 -m pip install --upgrade build
   python3 -m pip install --upgrade twine


To update the version in PyPI, update the version number in the pyproject.toml file, and 
execute the following commands to build and install.

.. code-block:: shell

   python3 -m build
   python3 -m twine upload dist/*


Unit testing
^^^^^^^^^^^^

Unit tests were written for pytest, which can be installed with pip and run from the top-level directory as


.. code-block:: shell

   pytest

