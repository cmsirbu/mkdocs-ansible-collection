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

## Housekeeping

### Upgrading `uv`

To use a newer `uv` version across the board, make sure to upgrade and test locally first, then replace the pinned version in these files:

- `.github/workflows/ci.yaml`
- `.github/workflows/release.yaml`
- `.readthedocs.yaml`

### Release Checklist

To cut a new release (e.g. for `v1.4.2`), follow these steps:

1. Bump the version in `pyproject.toml` with `uv version --bump major/minor/patch`.
2. Create a new branch with the new version `git switch -c release-v1.4.2`.
3. Upgrade lockfile package versions with `uv lock --upgrade`.
4. Update the release notes in `./docs/release_notes.md`.
5. Create PR from `release-v1.4.2` against `main`. Wait for CI to pass and merge PR.
6. Create a new release in GitHub with a new tag, selecting `Create new tag: v1.4.2 on publish`. Copy release notes from docs.
7. Publish the release and verify the `release` workflow succeeds and the package is published to PyPI.
