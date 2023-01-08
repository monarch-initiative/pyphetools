# pyphetools
Python Phenopacket Tools

This package currently is designed to test how to use the Python version of the phenopackets package together with pandas to create phenopackets from typical supplemental tables.

Development goals include making builder code similar to the Java package to create valid phenopackets and to perform JSON Schema-based validation.


## Setup

For initial development, we will use notebooks mainly. Do the following to get set up. Note that now
we are using phenopackets version 2.0.2. openpyxl is needed to read Excel files.


```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install jupyter
python -m ipykernel install --name "venv" --display-name "venv"
cd notebooks
jupyter-notebook
```

We have installed the package in the Python Package Index (pypi) at [pyphentools](https://pypi.org/project/pyphetools/).

### Updating package in PyPI
Make sure the build and twine packages are installed.
```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```
Update the version number in the pyproject.toml file
Build and install
```
python3 -m build
python3 -m twine upload dist/*
```
