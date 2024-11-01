# MkDocs Ansible Collection

[MkDocs](https://www.mkdocs.org) Plugin that automatically generates documentation pages for Ansible Collections. Check out the showcase over on the project's [documentation page](https://mkdocs-ansible-collection.readthedocs.io/en/latest/showcase/)!

## Quick Start

1. Add the `mkdocs-ansible-collection` package to your project's docs dependencies. It will also install `ansible-core` to manage collections and get the required metadata.

    ```
    pip install mkdocs-ansible-collection
    ```

2. Install any needed collection(s) using `ansible-galaxy collection install <names>` or point ansible at the correct collection path.

3. Enable the plugin in your project's `mkdocs.yml` file:

    ```yaml
    plugins:
      - "ansible-collection":
          collections:
            - fqcn: "collection.example"
    ```

4. Add an anchor page to the `nav` section of your project's `mkdocs.yml` file:

    ```yaml
    nav:
      # The anchor is named after the Collection FQCN and it tells mkdocs where
      # to generate the documentation tree. The following examples show all of
      # the currently supported combinations:
      - "Ansible Builtins": "ansible.builtin"
      - "Collection Showcase":
        - "showcase/index.md"
        - "ansible.posix"
      - "networktocode.nautobot"
    ```

For more details, check out the detailed [User Guide](user_guide.md) and look at the documentation example of [this project's docs](https://github.com/cmsirbu/mkdocs-ansible-collection) themselves which showcase how to build and host collection docs on the awesome [Read the Docs](https://about.readthedocs.com/) service!

### Requirements and Compatibility

To generate the pages dynamically at build time, the plugin uses metadata exported by the `ansible-doc` tool, which must be installed together with the collections you want to generate documentation for in your environment.

The plugin has been built for `mkdocs >= 1.6.0` and has only been tested with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

## Developing

To set up the development environment, run the following commands in the project root:

```
poetry install
poetry run mkdocs serve
```

## Contributions

!!! warning Work in Progress

    This plugin is under initial development - you can track progress towards the first fully functional release [here](https://github.com/cmsirbu/mkdocs-ansible-collection/milestone/1).

Contributions of all sorts (bug reports, features, documentation etc.) are welcome! If you're not sure about any of the changes you are proposing, please open a new issue to discuss it first.
