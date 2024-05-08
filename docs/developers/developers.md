# For developers

## Local Installation

We recommend creating a local environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

and updating Python's `pip` tool:

```bash
python3 -m pip install --upgrade pip
```

You can then do a local/editable install:


```bash
python3 -m pip install --editable ".[test]"
```

After installation you should be able to run the test suite:

```bash
pytest
```


## Creating Phenopackets

pyphetools provides two main ways of creating phenopackets.

- Using an Excel template. This is the recommended approach for most users.
    - Details are provided in the [Phenopacket Store](https://monarch-initiative.github.io/phenopacket-store/contributing/){:target="\_blank"} documentation, along with many examples.

- Creating custom Python scripts. This approach can be used by those who are comfortable with writing Python and using Jupyter notebooks. This approach is mainly intended to ingest tabular data from published articles with data from numerous individuals in tabular form (e.g., a typical Supplemental Table). The formats that
one encounters in publications are so varied, that pyphetools provides a variety of approaches to capturing the data.
    - See the section on [Custom Python scripts](../user-guide/jupyter.md) to get started
    - See the [API documentation](../api/overview.md) for details

