---
hide:
  - navigation
---

# User Guide

This MkDocs plugin generates documentation pages dynamically from Ansible Collection metadata.

## Requirements and Compatibility

The dependencies and minimum supported versions are as follows:

- [Python](https://www.python.org/downloads/) `3.10`
- [MkDocs](https://www.mkdocs.org) `1.6.0`
- [Ansible Core](https://docs.ansible.com/ansible-core/devel/index.html) `2.16`

While the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme is not a direct requirement, the plugin has only been developed and tested with it.

## Getting Started

Add the `mkdocs-ansible-collection` Python package to your project's docs dependencies using your project management tool of choice. It will also install `ansible-core` to manage collections and get the required metadata.

```
pip install mkdocs-ansible-collection
```

Install any needed collection(s) using `ansible-galaxy collection install example.collection` or `ansible-galaxy collection install -r requirements.yaml` or point ansible at the correct collection path via `ansible.cfg`.

Each Ansible Collection FQCN must be added to the Plugin Configuration and have an anchor defined in the `nav` section of your docs! See both sections below for details.

### Plugin Configuration

Add the plugin to your project's `mkdocs.yaml` file and list all the Ansible Collections that you want documentation generated for:

```yaml
plugins:
  - "ansible-collection":
      collections:
        - fqcn: "ansible.builtin"
        - fqcn: "arista.eos"
        - fqcn: "networktocode.nautobot"
        - fqcn: "ansible.netcommon"
```

### Anchor Pages

Add one anchor to the `nav` section of your project's `mkdocs.yaml` file for each collection defined in the plugin configuration. The anchor is named after the Collection FQCN and it tells mkdocs where to generate the documentation tree.

There are several combinations for how the resulting page is named and displayed in the documentation navigation:

- The anchor can be as simple as just the collection name, for example `"arista.eos"` and the page name will default to exactly this collection name.
- The page name can also be customized to anything you'd like, for example `"My Cool Collection": "example.collection"`.
- The anchor can be nested, with or without the custom page name, under any section or page in your documentation tree.

```yaml
nav:
  - "Collection Showcase":
    - "showcase/index.md"
    - "ansible.posix"
    - "ansible.netcommon"
    - "ansible.utils"
    - "Arista EOS": "arista.eos"
  - "Ansible Builtins": "ansible.builtin"
  - "networktocode.nautobot"
```

## Live Example

This project's documentation site serves as a live example on how to set up documentation for a project using this plugin! Feel free to use it as a [template](https://github.com/cmsirbu/mkdocs-ansible-collection) which also includes the necessary configuration to build and host the documentation on the awesome [Read the Docs](https://about.readthedocs.com/) service!

## Ansible Plugin Support

| Plugin Type | Support |
|-------------|---------|
| become      | :white_check_mark:       |
| cache       | :white_check_mark:       |
| callback    | :white_check_mark:       |
| connection  | :white_check_mark:       |
| filter      | :white_check_mark:       |
| inventory   | :white_check_mark:       |
| keyword     | :x:       |
| lookup      | :white_check_mark:       |
| module      | :white_check_mark:       |
| shell       | :white_check_mark:       |
| strategy    | :white_check_mark:       |
| test        | :white_check_mark:       |
| vars        | :white_check_mark:       |
| cliconf     | :white_check_mark:       |
| httpapi     | :white_check_mark:       |
| netconf     | :white_check_mark:       |
| role        | :x:       |
