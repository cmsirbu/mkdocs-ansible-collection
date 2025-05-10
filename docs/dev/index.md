---
hide:
  - navigation
---

# Developer Guide

To set up the development environment, first make sure you have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed. This project is set up to use the plugin itself to generate its own docs.

Now run the following commands in the project root:

```
# This installs the needed dependencies in a virtual environment managed by uv
# and the ansible collections defined in the docs/requirements.yaml file.
./run.sh setup

# Build and serve docs
./run.sh serve
```

MkDocs will serve docs on localhost and automatically rebuild on documentation changes. The browser page should also automatically reload on successful rebuild.

!!! warning
    MkDocs will NOT detect python code changes in the plugin, you will need to stop the server (press Ctrl-C) and start it again with `./run.sh serve`.

## View Debug Output

This plugin logs a lot of useful information at the `DEBUG` level, which you can get by adding the `-v` parameter to `mkdocs` - be warned this generates a LOT of output!

```
./run.sh serve -v
```

## Debug Ansible Metadata

To extract a JSON metadata file from an ansible collection, use the following command:

```
uv run ansible-doc --metadata-dump --no-fail-on-errors networktocode.nautobot > ansible-doc-nautobot.json
```
