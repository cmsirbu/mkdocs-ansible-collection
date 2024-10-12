"""MkDocs Ansible Collection package."""

PLUGIN_TO_TEMPLATE_MAP = {
    "become": "default",
    "cache": "default",
    "callback": "default",
    "connection": "default",
    "filter": "filter",
    "inventory": "inventory",
    "keyword": None,
    "lookup": "default",
    "module": "default",
    "shell": "default",
    "strategy": "default",
    "test": "default",
    "vars": "default",
}

DISABLED_PLUGIN_TYPES = ["keyword"]
