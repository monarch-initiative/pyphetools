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
pip install phenopackets
pip install pandas
pip install openpyxl
pip install jupyter
ipython kernel install --name "venv" --user
cd notebooks
jupyter-notebook
```