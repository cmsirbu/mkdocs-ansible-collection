import mkdocs
import subprocess
import json


class AnsibleDocsPluginConfig(mkdocs.config.base.Config):
    plugins = mkdocs.config.config_options.Type(list, default=[])
    collections = mkdocs.config.config_options.Type(list, default=[])


# TODO: Use mkdocs logger
class AnsibleDocsPlugin(mkdocs.plugins.BasePlugin[AnsibleDocsPluginConfig]):
    def on_pre_build(self, config, **kwargs):
        if self.config.plugins:
            print(f"Plugins list: {self.config.plugins}")
        if self.config.collections:
            print(f"Collections list: {self.config.collections}")

        # print(config)

    def on_files(self, files, config):
        for fqcn in self.config.collections:
            # Get collection metadata by running ansible-doc
            collection_metadata = AnsibleDocsPlugin._get_ansible_doc_metadata(fqcn)

            # Generate the index for the collection sub-path
            nf = mkdocs.structure.files.File(
                f"{fqcn}/index.md", src_dir=None, dest_dir=config.site_dir, use_directory_urls=False
            )
            nf.generated_by = "ansible-docs"
            nf.content_string = f"# Collection: {fqcn}"
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
                plugin_markdown_list = "\n".join("- " + plugin for plugin in plugins)
                nf.content_string = f"# {plugin_type}\n\n{plugin_markdown_list}"

                files.append(nf)
                collection_nav[fqcn].append({f"{plugin_type}": f"{fqcn}/{plugin_type}.md"})

            config.nav.append(collection_nav)

        return files

    def on_nav(self, nav, config, files):
        pass
        print(config.nav)
        print(nav.items)

        # breakpoint()

    @staticmethod
    def _get_ansible_doc_metadata(fqcn):
        # TODO: Add error handling
        result = subprocess.run(
            ["ansible-doc", "--metadata-dump", "--no-fail-on-errors", fqcn], capture_output=True
        )
        # result.returncode | stderr
        return json.loads(result.stdout)
