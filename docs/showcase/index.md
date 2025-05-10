# Collection Showcase

This documentation section and the other two top-level collection pages ([Ansible Builtins](../ansible.builtin/) and [NetworkToCode Nautobot](../networktocode.nautobot/)) serve as a showcase of all the ways you can anchor the generated documentation trees in your MkDocs `nav`.

```yaml
nav:
  # The anchor is named after the Collection FQCN and it tells mkdocs where
  # to generate the documentation tree. The following examples show all of
  # the currently supported combinations:
  - "Collection Showcase":
    - "showcase/index.md"
    - "ansible.posix"
    - "ansible.netcommon"
    - "ansible.utils"
    - "Arista EOS": "arista.eos"
  - "Ansible Builtins": "ansible.builtin"
  - "networktocode.nautobot"
```
