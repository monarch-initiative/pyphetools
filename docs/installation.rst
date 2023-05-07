.. _installation:

==========================
Installation of pyphetools
==========================

pyphetools is available as a `PyPI package <https://pypi.org/project/pyphetools/>`_. 

Most users should install the latest version (the following example creates a virtual environment).
Note that depending on your system it will be necessary to update pip to be able to install pyphetools.

.. code-block:: shell
   :linenos:

   python3 -m venv ppt_env
   source ppt_env/bin/activate
   pip install --upgrade pip
   pip install pyphetools

To work with the notebooks in this repository, it may be desirable to install the latest local version

.. code-block:: shell
   :linenos:

   source ppt_env/bin/activate
   pip install -e .


To use the kernel in notebooks, enter the following

.. code-block:: shell
   :linenos:

   pip install jupyter
   python -m ipykernel install --name "ppt_env" --display-name "ppt_env"
   cd notebooks
   jupyter-notebook


