# Installation of pyphetools


pyphetools is available as a [PyPI package](https://pypi.org/project/pyphetools/){:target="\_blank"}.

Most users should install the latest version (the following example creates a virtual environment).
Note that depending on your system it will be necessary to update pip to be able to install pyphetools.

```bash title="setting up a virtual environment"
python3 -m venv ppt_env
source ppt_env/bin/activate
pip install --upgrade pip
```

To work with the notebooks in this repository, it may be desirable to install the latest local version

```bash title="installing pyphetools"
source ppt_env/bin/activate
pip install -e .
```

To use the kernel in notebooks, enter the following

```bash title="installing jupyter and running pyphetools in a notebook"
pip install jupyter ipykernel
python -m ipykernel install --user --name "ppt_env" --display-name "ppt_env"
jupyter-notebook
```

The last command will open a jupyter. Create or open a notebook and set the kernel to **ppt_env**.


