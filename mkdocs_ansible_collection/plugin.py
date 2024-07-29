import mkdocs
import subprocess
import json

from importlib.resources import files as package_files
from jinja2 import Environment, FileSystemLoader, select_autoescape
from mkdocs.exceptions import PluginError
from mkdocs.plugins import get_plugin_logger

# Warning level messages break the build if --strict is passed!
# Debug level messages show only if --verbose is passed!
log = get_plugin_logger(__name__)


class AnsibleDocsPluginConfig(mkdocs.config.base.Config):
    # plugins = mkdocs.config.config_options.Type(list, default=[])
    collections = mkdocs.config.config_options.Type(list, default=[])


class AnsibleDocsPlugin(mkdocs.plugins.BasePlugin[AnsibleDocsPluginConfig]):
    def on_pre_build(self, config, **kwargs):
        # if self.config.plugins:
        #     log.debug(f"Plugins list: {self.config.plugins}")
        if self.config.collections:
            log.debug(f"Collections list: {self.config.collections}")

    def on_files(self, files, config):
        # Load templates from package and initialize Jinja environment
        log.debug(
            f"Jinja templates path {package_files('mkdocs_ansible_collection') / 'templates'}"
        )
        jinja_env = Environment(
            loader=FileSystemLoader(package_files("mkdocs_ansible_collection") / "templates"),
            autoescape=select_autoescape(default=True),
            trim_blocks=True,
        )

        for fqcn in self.config.collections:
            # Get collection metadata by running ansible-doc
            collection_metadata = AnsibleDocsPlugin._get_ansible_doc_metadata(fqcn)

            # Generate the index for the collection sub-path
            nf = mkdocs.structure.files.File(
                f"{fqcn}/index.md", src_dir=None, dest_dir=config.site_dir, use_directory_urls=False
            )
            nf.generated_by = "ansible-docs"

            jinja_template = jinja_env.get_template("collection_index.md.jinja")
            nf.content_string = jinja_template.render(
                plugin_types=collection_metadata["all"], fqcn=fqcn
            )

            files.append(nf)
            collection_nav = {f"{fqcn}": [f"{fqcn}/index.md"]}

            for plugin_type in collection_metadata["all"]:
                plugins = collection_metadata["all"][plugin_type]
                if len(plugins) == 0:
                    continue

                nf = mkdocs.structure.files.File(
                    f"{fqcn}/{plugin_type}.md",
                    src_dir=None,
                    dest_dir=config.site_dir,
                    use_directory_urls=False,
                )
                nf.generated_by = "ansible-docs"

                jinja_template = jinja_env.get_template("plugin_list.md.jinja")
                nf.content_string = jinja_template.render(plugin_type=plugin_type, plugins=plugins)

                files.append(nf)
                collection_nav[fqcn].append({f"{plugin_type}": f"{fqcn}/{plugin_type}.md"})

            config.nav.append(collection_nav)

        return files

    # Comment this when code is stable, used only for debugging
    def on_nav(self, nav, config, files):
        log.debug(f"config.nav = {config.nav}")
        # breakpoint()

    @staticmethod
    def _get_ansible_doc_metadata(fqcn):
        log.info(f"Fetching collection {fqcn} metadata from ansible-doc.")
        result = subprocess.run(
            ["ansible-doc", "--metadata-dump", "--no-fail-on-errors", fqcn], capture_output=True
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
