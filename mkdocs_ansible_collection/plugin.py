"""MkDocs Plugin that automatically generates pages for Ansible Collections."""

import json
import subprocess
from importlib.resources import files as package_files

import mkdocs
from jinja2 import Environment, FileSystemLoader, select_autoescape
from mkdocs.exceptions import PluginError
from mkdocs.plugins import get_plugin_logger

from mkdocs_ansible_collection import DISABLED_PLUGIN_TYPES, PLUGIN_TO_TEMPLATE_MAP

# Warning level messages break the build if --strict is passed!
# Debug level messages show only if --verbose is passed!
log = get_plugin_logger(__name__)


class AnsibleDocsPluginConfig(mkdocs.config.base.Config):
    """MkDocs Plugin configuration."""

    # plugins = mkdocs.config.config_options.Type(list, default=[])
    collections = mkdocs.config.config_options.Type(list, default=[])


class AnsibleDocsPlugin(mkdocs.plugins.BasePlugin[AnsibleDocsPluginConfig]):
    """MkDocs Plugin Class."""

    def __init__(self, *args, **kwargs):
        """Instantiation."""
        super().__init__(*args, **kwargs)

        # Load templates from package and initialize Jinja environment
        log.debug(
            f"Jinja templates path {package_files('mkdocs_ansible_collection') / 'templates'}"
        )
        self.jinja_env = Environment(
            loader=FileSystemLoader(package_files("mkdocs_ansible_collection") / "templates"),
            autoescape=select_autoescape(["html", "htm", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def on_pre_build(self, config):
        """
        Event handler for the pre_build stage.

        Args:
            config (MkDocsConfig): global configuration object

        See:
            https://www.mkdocs.org/dev-guide/plugins/#events
        """
        if self.config.collections:
            log.debug(f"Collections list: {self.config.collections}")

    def on_files(self, files, config):  # noqa: PLR0912 Too many branches
        """
        Event handler for the on_files stage.

        Args:
            files (Files): global files collection
            config (MkDocsConfig): global configuration object

        Returns:
            Files | None: global files collection

        See:
            https://www.mkdocs.org/dev-guide/plugins/#events
        """
        for collection in self.config.collections:
            # Get collection metadata by running ansible-doc
            fqcn = collection["fqcn"]
            collection_metadata = AnsibleDocsPlugin._get_ansible_doc_metadata(fqcn)

            # Generate the index for the collection sub-path
            # TODO: extract requirements from all plugins and list on this page
            # TODO: extract collection version
            # TODO: combine the PLUGIN_TO_TEMPLATE_MAP with enabled plugins from plugin config
            files.append(
                self._generate_page(
                    path=f"{fqcn}/index.md",
                    site_dir=config.site_dir,
                    template="collection_index.md.jinja",
                    fqcn=fqcn,
                    plugin_types=collection_metadata["all"],
                    plugin_map=PLUGIN_TO_TEMPLATE_MAP,
                )
            )
            collection_nav = {f"{fqcn}": [f"{fqcn}/index.md"]}

            for plugin_type in collection_metadata["all"]:
                if plugin_type not in PLUGIN_TO_TEMPLATE_MAP:
                    log.warning(
                        f"Plugin type {plugin_type} is not yet supported"
                        + " - please open an issue at https://github.com/cmsirbu/mkdocs-ansible-collection/issues/new"
                    )
                # Disable some plugin_types that should not have generated pages
                elif PLUGIN_TO_TEMPLATE_MAP[plugin_type] is None:
                    continue

                plugins = collection_metadata["all"][plugin_type]
                if len(plugins) == 0:
                    continue
                sub_nav = {f"{plugin_type}": [f"{fqcn}/{plugin_type}/index.md"]}

                files.append(
                    self._generate_page(
                        path=f"{fqcn}/{plugin_type}/index.md",
                        site_dir=config.site_dir,
                        template="plugin_list.md.jinja",
                        fqcn=fqcn,
                        plugin_type=plugin_type,
                        plugins=plugins,
                    )
                )

                for plugin_fqname, plugin_data in plugins.items():
                    # If there are any parsing issues for a plugin, ansible-doc will replace the
                    # plugin metadata with an error message.
                    if plugin_data.get("error") is not None:
                        log.warning(
                            f"Error returned for {plugin_fqname} by ansible-doc: {plugin_data['error']}"  # noqa: E501
                        )
                        continue

                    log.debug(f"Generating page for {plugin_fqname}")
                    plugin_name = plugin_fqname.removeprefix(fqcn + ".")
                    files.append(
                        self._generate_page(
                            path=f"{fqcn}/{plugin_type}/{plugin_name}.md",
                            site_dir=config.site_dir,
                            template=f"{PLUGIN_TO_TEMPLATE_MAP.get(plugin_type, 'default')}.md.jinja",  # noqa: E501
                            fqcn=fqcn,
                            plugin=plugin_fqname,
                            plugin_name=plugin_name,
                            plugin_data=plugin_data,
                        )
                    )

                    sub_nav[plugin_type].append(
                        {f"{plugin_name}": f"{fqcn}/{plugin_type}/{plugin_name}.md"}
                    )

                collection_nav[fqcn].append(sub_nav)

            # Find the correct nav location to insert the section
            stack = [config.nav]
            found = False
            while stack:
                entry = stack.pop(0)
                if isinstance(entry, dict):
                    for k, v in entry.items():
                        if v == fqcn:
                            entry[k] = collection_nav[fqcn]
                            found = True
                            break
                    else:
                        stack.append(list(entry.values()))
                elif isinstance(entry, list):
                    if fqcn in entry:
                        index = entry.index(fqcn)
                        entry[index] = collection_nav
                        found = True
                        break
                    else:
                        stack += entry

            if not found:
                raise PluginError(
                    f"Couldn't find collection placeholder in the nav for {fqcn}!"
                    + " Please check your mkdocs configuration!"
                )

        return files

    # Comment this when code is stable, used only for debugging
    def on_nav(self, nav, config, files):
        """
        Event handler for the on_nav stage.

        Args:
            nav (Navigation): global navigation object
            files (Files): global files collection
            config (MkDocsConfig): global configuration object

        Returns:
            Navigation | None: global navigation object

        See:
            https://www.mkdocs.org/dev-guide/plugins/#events
        """
        log.debug(f"config.nav = {config.nav}")
        # breakpoint()

    def _generate_page(self, path, site_dir, template, **kwargs):
        """Generates a new file in memory from a Jinja template.

        Args:
            path (str): relative path from the docs root with filename.md
            site_dir (str): project config.site_dir
            template (str): name of jinja template to use for rendering
            kwargs (dict): data to pass to jinja.render

        Returns:
            mkdocs.structure.files.File: file object with generated content
        """
        nf = mkdocs.structure.files.File(
            path, src_dir=None, dest_dir=site_dir, use_directory_urls=False
        )
        nf.generated_by = "ansible-collection"

        jinja_template = self.jinja_env.get_template(template)
        nf.content_string = jinja_template.render(**kwargs)

        return nf

    @staticmethod
    def _get_ansible_doc_metadata(fqcn):
        """
        Retrieve Ansible collection metadata via the ansible-doc command.

        Args:
            fqcn (string): ansible fully-qualified collection name

        Returns:
            dict: parsed collection metadata from JSON
        """
        log.info(f"Fetching collection {fqcn} metadata from ansible-doc.")
        ansible_doc_command_params = ["ansible-doc", "--metadata-dump", "--no-fail-on-errors", fqcn]
        result = subprocess.run(
            ansible_doc_command_params,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            command = " ".join(ansible_doc_command_params)
            log.error(f"Command {command} failed with stderr: {result.stderr}")
            raise PluginError(
                f"Couldn't fetch collection {fqcn} metadata due to errors from ansible-doc!"
            )
        else:
            try:
                parsed_data = json.loads(result.stdout)
            except json.decoder.JSONDecodeError:
                raise PluginError("Couldn't parse ansible-doc output as valid JSON data!")

            # Remove plugin types that shouldn't be in the docs
            for plugin_type in DISABLED_PLUGIN_TYPES:
                del parsed_data["all"][plugin_type]

            return parsed_data
