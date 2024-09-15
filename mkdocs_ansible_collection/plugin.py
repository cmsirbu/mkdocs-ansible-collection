"""MkDocs Plugin that automatically generates pages for Ansible Collections."""

import json
import subprocess
from importlib.resources import files as package_files

import mkdocs
from jinja2 import Environment, FileSystemLoader, select_autoescape
from mkdocs.exceptions import PluginError
from mkdocs.plugins import get_plugin_logger

# Warning level messages break the build if --strict is passed!
# Debug level messages show only if --verbose is passed!
log = get_plugin_logger(__name__)


class AnsibleDocsPluginConfig(mkdocs.config.base.Config):
    """MkDocs Plugin configuration."""

    # plugins = mkdocs.config.config_options.Type(list, default=[])
    collections = mkdocs.config.config_options.Type(list, default=[])


class AnsibleDocsPlugin(mkdocs.plugins.BasePlugin[AnsibleDocsPluginConfig]):
    """MkDocs Plugin Class."""

    # TODO: Remove once all plugin types have a corresponding jinja template
    PLUGIN_MAP = {"filter": "filter", "inventory": "inventory"}

    def __init__(self, *args, **kwargs):
        """Instantiation."""
        super().__init__(*args, **kwargs)

        # Load templates from package and initialize Jinja environment
        log.debug(
            f"Jinja templates path {package_files('mkdocs_ansible_collection') / 'templates'}"
        )
        self.jinja_env = Environment(
            loader=FileSystemLoader(package_files("mkdocs_ansible_collection") / "templates"),
            autoescape=select_autoescape(default=True),
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
        # if self.config.plugins:
        #     log.debug(f"Plugins list: {self.config.plugins}")
        if self.config.collections:
            log.debug(f"Collections list: {self.config.collections}")

    def on_files(self, files, config):
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
        for fqcn in self.config.collections:
            # Get collection metadata by running ansible-doc
            collection_metadata = AnsibleDocsPlugin._get_ansible_doc_metadata(fqcn)

            # Generate the index for the collection sub-path
            # TODO: extract requirements from all plugins and list on this page
            # TODO: extract collection version
            files.append(
                self._generate_page(
                    path=f"{fqcn}/index.md",
                    site_dir=config.site_dir,
                    template="collection_index.md.jinja",
                    fqcn=fqcn,
                    plugin_types=collection_metadata["all"],
                )
            )
            collection_nav = {f"{fqcn}": [f"{fqcn}/index.md"]}

            for plugin_type in collection_metadata["all"]:
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
                    if plugin_data.get("error") is not None:
                        log.warning(
                            f"Error returned for {plugin_fqname} by ansible-doc: {plugin_data['error']}"
                        )
                        continue
                    log.debug(f"Generating page for {plugin_fqname}")
                    plugin_name = plugin_fqname.removeprefix(fqcn + ".")
                    files.append(
                        self._generate_page(
                            path=f"{fqcn}/{plugin_type}/{plugin_name}.md",
                            site_dir=config.site_dir,
                            # TODO: replace line once the mapping is not needed
                            # template=f"{plugin_type}.md.jinja",
                            template=f"{AnsibleDocsPlugin.PLUGIN_MAP.get(plugin_type, 'default')}.md.jinja",  # noqa
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

            config.nav.append(collection_nav)

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
        result = subprocess.run(
            ["ansible-doc", "--metadata-dump", "--no-fail-on-errors", fqcn],
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            command = " ".join(["ansible-doc", "--metadata-dump", "--no-fail-on-errors", fqcn])
            log.error(f"Command {command} failed with stderr: {result.stderr}")
            raise PluginError(
                f"Couldn't fetch collection {fqcn} metadata due to errors from ansible-doc!"
            )
        else:
            try:
                parsed_data = json.loads(result.stdout)
            except json.decoder.JSONDecodeError:
                raise PluginError("Couldn't parse ansible-doc output as valid JSON data!")
            return parsed_data
