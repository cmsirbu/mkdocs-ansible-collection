"""MkDocs Ansible Collection package."""

PLUGIN_TO_TEMPLATE_MAP = {
    "become": "plugin",
    "cache": "plugin",
    "callback": "plugin",
    "connection": "plugin",
    "filter": "plugin",
    "inventory": "plugin",
    "keyword": None,
    "lookup": "plugin",
    "module": "plugin",
    "shell": "plugin",
    "strategy": "plugin",
    "test": "plugin",
    "vars": "plugin",
    "cliconf": "plugin",
    "httpapi": "plugin",
    "netconf": "plugin",
    "role": None,
}

DISABLED_PLUGIN_TYPES = ["keyword"]
