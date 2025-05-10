# MkDocs Ansible Collection

[MkDocs](https://www.mkdocs.org) Plugin that automatically generates documentation pages for Ansible Collections. Check out the showcase over on the project's [documentation page](https://mkdocs-ansible-collection.readthedocs.io/en/stable/showcase/) and more detailed [User](https://mkdocs-ansible-collection.readthedocs.io/en/stable/user/) and [Developer](https://mkdocs-ansible-collection.readthedocs.io/en/stable/dev/) guides!

## Quick Start

1. Add the `mkdocs-ansible-collection` Python package to your project's docs dependencies. It will also install `ansible-core` to manage collections and get the required metadata.

    ```
    pip install mkdocs-ansible-collection
    ```

2. Install any needed collection(s) using `ansible-galaxy collection install example.collection` or point ansible at the correct collection path.

3. Enable the plugin in your project's `mkdocs.yaml` file:

    ```yaml
    plugins:
      - "ansible-collection":
          collections:
            - fqcn: "example.collection"
    ```

4. Add an anchor page to the `nav` section of your project's `mkdocs.yaml` file:

    ```yaml
    nav:
      # The anchor is named after the Collection FQCN and it tells mkdocs where
      # to generate the documentation tree. The following examples show all of
      # the currently supported combinations:
      - "Example Collection": "example.collection" # With an explicit page name
      - "Nested Under Another Page":
        - "example.collection" # Without a custom page name
    ```

For more details, check out the [User Guide](https://mkdocs-ansible-collection.readthedocs.io/en/stable/user/) and look at the live example of [this project's docs](https://github.com/cmsirbu/mkdocs-ansible-collection), which showcase how to build and host collection docs on the awesome [Read the Docs](https://about.readthedocs.com/) service!

## Contributions

Contributions of all sorts (bug reports, features, documentation etc.) are welcome! Any larger change, please open a new [issue](https://github.com/cmsirbu/mkdocs-ansible-collection/issues) to discuss it first.
