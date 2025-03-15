"""
* Copyright 2020 The Backstage Authors
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
"""

import tempfile
import logging
import os

from mkdocs.config import Config, config_options
from mkdocs.plugins import BasePlugin
from mkdocs.theme import Theme
from mkdocs.contrib.search import SearchPlugin
from material.plugins.search.plugin import SearchPlugin as MaterialSearchPlugin
from mkdocs_monorepo_plugin.plugin import MonorepoPlugin
from pymdownx.emoji import to_svg
from pymdownx.extra import extra_extensions

log = logging.getLogger(__name__)

TECHDOCS_DEFAULT_THEME = "material"


class TechDocsCoreConfig(Config):
    use_material_search = config_options.Type(bool, default=False)
    use_pymdownx_blocks = config_options.Type(bool, default=False)


class TechDocsCore(BasePlugin[TechDocsCoreConfig]):
    def __init__(self):
        # This directory will be removed automatically once the docs are built
        # MkDocs needs a directory for the theme with the `techdocs_metadata.json` file
        self.tmp_dir_techdocs_theme = tempfile.TemporaryDirectory()

    def on_config(self, config):
        with open(
            os.path.join(self.tmp_dir_techdocs_theme.name, "techdocs_metadata.json"),
            "w+",
        ) as fp:
            fp.write(
                '{{ {"site_name": (config.site_name | string), '
                '"site_description": (config.site_description | string)} | tojson }}'
            )

        mdx_configs_override = {}
        if "mdx_configs" in config:
            mdx_configs_override = config["mdx_configs"].copy()

        # Pymdown snippets override to prevent legacy behavior impacting security https://github.com/facelessuser/pymdown-extensions/security/advisories/GHSA-jh85-wwv9-24hv
        mdx_configs_override["pymdownx.snippets"] = {
            "restrict_base_path": True,
        }

        # Theme
        if config["theme"].name != TECHDOCS_DEFAULT_THEME:
            config["theme"] = Theme(name=TECHDOCS_DEFAULT_THEME)
        elif config["theme"].name == TECHDOCS_DEFAULT_THEME:
            log.info(
                "[mkdocs-techdocs-core] Overridden '%s' theme settings in use",
                TECHDOCS_DEFAULT_THEME,
            )

        if "features" not in config["theme"]:
            config["theme"]["features"] = []

        config["theme"]["features"].append("navigation.footer")
        config["theme"]["features"].append("content.action.edit")

        config["theme"]["palette"] = {}

        config["theme"].static_templates.update({"techdocs_metadata.json"})
        config["theme"].dirs.append(self.tmp_dir_techdocs_theme.name)

        # Plugins
        use_material_search = self.config["use_material_search"]
        use_pymdownx_blocks = self.config["use_pymdownx_blocks"]
        del config["plugins"]["techdocs-core"]

        if use_material_search:
            search_plugin = MaterialSearchPlugin()
        else:
            search_plugin = SearchPlugin()
        search_plugin.load_config({})

        monorepo_plugin = MonorepoPlugin()
        monorepo_plugin.load_config({})
        config["plugins"]["search"] = search_plugin
        config["plugins"]["monorepo"] = monorepo_plugin

        # Markdown Extensions
        if "markdown_extensions" not in config:
            config["markdown_extensions"] = []

        if "mdx_configs" not in config:
            config["mdx_configs"] = {}

        config["markdown_extensions"].append("toc")
        config["mdx_configs"]["toc"] = {
            "permalink": True,
        }

        if use_pymdownx_blocks:
            config["markdown_extensions"].append("pymdownx.blocks.admonition")
            config["mdx_configs"]["pymdownx.blocks.admonition"] = {
                "types": [
                    "new",
                    "settings",
                    "note",
                    "abstract",
                    "info",
                    "tip",
                    "success",
                    "question",
                    "warning",
                    "failure",
                    "danger",
                    "bug",
                    "example",
                    "quote",
                ]
            }
            config["markdown_extensions"].append("pymdownx.blocks.details")
            config["mdx_configs"]["pymdownx.blocks.details"] = {
                "types": [
                    {"name": "details-new", "class": "new"},
                    {"name": "details-settings", "class": "settings"},
                    {"name": "details-note", "class": "note"},
                    {"name": "details-abstract", "class": "abstract"},
                    {"name": "details-info", "class": "info"},
                    {"name": "details-tip", "class": "tip"},
                    {"name": "details-success", "class": "success"},
                    {"name": "details-question", "class": "question"},
                    {"name": "details-warning", "class": "warning"},
                    {"name": "details-failure", "class": "failure"},
                    {"name": "details-danger", "class": "danger"},
                    {"name": "details-bug", "class": "bug"},
                    {"name": "details-example", "class": "example"},
                    {"name": "details-quote", "class": "quote"},
                ]
            }
            config["markdown_extensions"].append("pymdownx.blocks.tab")
            config["mdx_configs"]["pymdownx.blocks.tab"] = {
                "alternate_style": True,
            }
        else:
            config["markdown_extensions"].append("admonition")
            config["markdown_extensions"].append("pymdownx.details")
            config["markdown_extensions"].append("pymdownx.tabbed")
            config["mdx_configs"]["pymdownx.tabbed"] = {
                "alternate_style": True,
            }

        config["markdown_extensions"].append("pymdownx.caret")
        config["markdown_extensions"].append("pymdownx.critic")
        config["markdown_extensions"].append("pymdownx.emoji")
        config["mdx_configs"]["pymdownx.emoji"] = {"emoji_generator": to_svg}
        config["markdown_extensions"].append("pymdownx.inlinehilite")
        config["markdown_extensions"].append("pymdownx.magiclink")
        config["markdown_extensions"].append("pymdownx.mark")
        config["markdown_extensions"].append("pymdownx.smartsymbols")
        config["markdown_extensions"].append("pymdownx.snippets")
        config["markdown_extensions"].append("pymdownx.highlight")
        config["mdx_configs"]["pymdownx.highlight"] = {
            "linenums": True,
            "pygments_lang_class": True,
        }
        config["markdown_extensions"].append("pymdownx.extra")
        config["mdx_configs"]["pymdownx.betterem"] = {
            "smart_enable": "all",
        }
        config["markdown_extensions"].append("pymdownx.tasklist")
        config["mdx_configs"]["pymdownx.tasklist"] = {
            "custom_checkbox": True,
        }
        config["markdown_extensions"].append("pymdownx.tilde")

        # merge individual extension configs under the pymdownx.extra extension namespace if individual extension is supplied by pymdownx.extra
        # https://facelessuser.github.io/pymdown-extensions/extensions/extra/
        if "pymdownx.extra" not in config["mdx_configs"]:
            config["mdx_configs"]["pymdownx.extra"] = {}
        for extension in extra_extensions:
            if extension in config["mdx_configs"]:
                config["mdx_configs"]["pymdownx.extra"][extension] = config[
                    "mdx_configs"
                ][extension]
                del config["mdx_configs"][extension]

        config["markdown_extensions"].append("markdown_inline_graphviz")
        config["markdown_extensions"].append("plantuml_markdown")
        config["markdown_extensions"].append("mdx_truly_sane_lists")

        # merge config supplied by user in the mkdocs.yml
        for key in mdx_configs_override:
            if key in config["mdx_configs"]:
                default_config = config["mdx_configs"][key]
                override_config = mdx_configs_override[key]
                default_config.update(override_config)

        return config
