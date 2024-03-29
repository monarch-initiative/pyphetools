# Encoding tabular data with pyphetools scripts

This option is intended for people who are comfortable using Python scripting, and is designed to import tabular data such as is commonly found in the supplemental files of medical publications about cohorts of individuals diagnosed with a certain disease. See also the instructions for using an [Excel template](template.md) for entering data with a minimum of scripting.


The best way to get a feeling for how to work with pyphetools is to examine the various notenooks in the
[phenopacket-store](https://github.com/monarch-initiative/phenopacket-store){:target="\_blank"} repository.

This tutorial provides some general tips for how to use the library. The library is intended to be used in a Jupyter notebook environment so that users can check intermediate results.
There are many ways of setting this up, but here is one that we often use.


The typical use case for using pyphetools in this way is to ingest complicated tables that would be too difficult or unweildly to import using the Excel template.


## Setting up the Jupyter environment

We recommend developing scripts using a Jupyter notebook so that parsing results can be checked.

There are many ways of setting up Jupyter, all of which should work with pyphetools. We use the following approach.

```bash title="installing jupyter and running pyphetools in a notebook"
python3 -m venv your_env
source your_env/bin/activiate
pip install --upgrade pip
pip install pyphetools
pip install jupyter ipykernel
python3 -m ipykernel install --name your_env --user
jupyter-notebook
```

The virtual environment (here *your_env*) can be named as desired. The last line opens a Jupyter Notebook page;
create a new Notebook and choose the kernel called *your_env* (or whatever you called it).

