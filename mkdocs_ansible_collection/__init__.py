"""MkDocs Ansible Collection package."""

PLUGIN_TO_TEMPLATE_MAP = {
    "become": "default",
    "cache": "default",
    "callback": "default",
    "connection": "default",
    "filter": "plugin",
    "inventory": "plugin",
    "keyword": None,
    "lookup": "plugin",
    "module": "plugin",
    "shell": "default",
    "strategy": "default",
    "test": "default",
    "vars": "default",
    "cliconf": None,
    "httpapi": None,
    "netconf": None,
    "role": None,
}

DISABLED_PLUGIN_TYPES = ["keyword"]
