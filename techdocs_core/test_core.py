import unittest
import mkdocs.plugins as plugins
from mkdocs.theme import Theme
from .core import TechDocsCore, TECHDOCS_DEFAULT_THEME
from jinja2 import Environment, PackageLoader, select_autoescape
import json


# Helper to get the "default" theme passed into config when no theme is
# provided in the actual config.
def get_default_theme():
    return Theme(name="mkdocs")


class TestTechDocsCoreConfig(unittest.TestCase):
    def setUp(self):
        self.techdocscore = TechDocsCore()
        self.plugin_collection = plugins.PluginCollection()
        self.plugin_collection["techdocs-core"] = self.techdocscore
        self.mkdocs_yaml_config = {"plugins": self.plugin_collection}
        # Note: in reality, config["theme"] is always an instance of Theme
        self.mkdocs_yaml_config["theme"] = get_default_theme()

    def test_removes_techdocs_core_plugin_from_config(self):
        self.plugin_collection["techdocs-core"].load_config({})
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertTrue("techdocs-core" not in final_config["plugins"])

    def test_merge_default_config_and_user_config(self):
        self.plugin_collection["techdocs-core"].load_config({})
        self.mkdocs_yaml_config["markdown_extension"] = []
        self.mkdocs_yaml_config["mdx_configs"] = {}
        self.mkdocs_yaml_config["markdown_extension"].append(["toc"])
        self.mkdocs_yaml_config["mdx_configs"]["toc"] = {"toc_depth": 3}
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertTrue("toc" in final_config["mdx_configs"])
        self.assertTrue("permalink" in final_config["mdx_configs"]["toc"])
        self.assertTrue("toc_depth" in final_config["mdx_configs"]["toc"])
        self.assertTrue("mdx_truly_sane_lists" in final_config["markdown_extensions"])

    def test_override_default_config_with_user_config(self):
        self.plugin_collection["techdocs-core"].load_config({})
        self.mkdocs_yaml_config["markdown_extension"] = []
        self.mkdocs_yaml_config["mdx_configs"] = {}
        self.mkdocs_yaml_config["markdown_extension"].append(["toc"])
        self.mkdocs_yaml_config["mdx_configs"]["toc"] = {"permalink": False}
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertTrue("toc" in final_config["mdx_configs"])
        self.assertTrue("permalink" in final_config["mdx_configs"]["toc"])
        self.assertFalse(final_config["mdx_configs"]["toc"]["permalink"])
        self.assertTrue("mdx_truly_sane_lists" in final_config["markdown_extensions"])

    def test_theme_overrides_removed_when_name_is_not_material(self):
        self.plugin_collection["techdocs-core"].load_config({})
        # we want to force the theme mkdocs to this test
        self.mkdocs_yaml_config["theme"] = Theme(name="mkdocs")
        self.mkdocs_yaml_config["theme"]["features"] = ["navigation.sections"]
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertFalse("navigation.sections" in final_config["theme"]["features"])

    def test_theme_overrides_when_name_is_material(self):
        self.plugin_collection["techdocs-core"].load_config({})
        self.mkdocs_yaml_config["theme"] = Theme(name=TECHDOCS_DEFAULT_THEME)
        self.mkdocs_yaml_config["theme"]["features"] = ["navigation.sections"]
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertTrue("navigation.sections" in final_config["theme"]["features"])

    def test_theme_overrides_techdocs_metadata(self):
        self.plugin_collection["techdocs-core"].load_config({})
        self.mkdocs_yaml_config["theme"] = Theme(
            name=TECHDOCS_DEFAULT_THEME, static_templates=["my_static_temples"]
        )
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertTrue("my_static_temples" in final_config["theme"].static_templates)
        self.assertTrue(
            "techdocs_metadata.json" in final_config["theme"].static_templates
        )

    def test_theme_overrides_dirs(self):
        self.plugin_collection["techdocs-core"].load_config({})
        custom_theme_dir = "/tmp/my_custom_theme_dir"
        self.mkdocs_yaml_config["theme"] = Theme(name=TECHDOCS_DEFAULT_THEME)
        self.mkdocs_yaml_config["theme"].dirs.append(custom_theme_dir)
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertTrue(custom_theme_dir in final_config["theme"].dirs)
        self.assertTrue(
            self.techdocscore.tmp_dir_techdocs_theme.name in final_config["theme"].dirs
        )

    def test_template_renders__multiline_value_as_valid_json(self):
        self.plugin_collection["techdocs-core"].load_config({})
        self.techdocscore.on_config(self.mkdocs_yaml_config)
        env = Environment(
            loader=PackageLoader(
                "techdocs_core", self.techdocscore.tmp_dir_techdocs_theme.name
            ),
            autoescape=select_autoescape(),
        )
        template = env.get_template("techdocs_metadata.json")
        config = {
            "site_name": "my site",
            "site_description": "my very\nlong\nsite\ndescription",
        }
        rendered = template.render(config=config)
        as_json = json.loads(rendered)
        self.assertEqual(config, as_json)

    def test_restrict_snippet_base_path(self):
        self.plugin_collection["techdocs-core"].load_config({})
        self.mkdocs_yaml_config["mdx_configs"] = {
            "pymdownx.snippets": {"restrict_base_path": False}
        }

        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)

        self.assertEqual(
            final_config["mdx_configs"]["pymdownx.snippets"]["restrict_base_path"],
            True,
        )

    def test_material_search(self):
        self.plugin_collection["techdocs-core"].load_config(
            {"use_material_search": True}
        )
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)

        self.assertEqual(
            final_config["plugins"]["search"].__module__,
            "material.plugins.search.plugin",
        )

    def test_default_search(self):
        self.plugin_collection["techdocs-core"].load_config({})
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertEqual(
            final_config["plugins"]["search"].__module__, "mkdocs.contrib.search"
        )

    def test_pymdownx_blocks(self):
        self.plugin_collection["techdocs-core"].load_config(
            {"use_pymdownx_blocks": True}
        )
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)

        self.assertTrue(
            "pymdownx.blocks.admonition" in final_config["markdown_extensions"]
        )
        self.assertTrue(
            "pymdownx.blocks.details" in final_config["markdown_extensions"]
        )
        self.assertTrue("pymdownx.blocks.tab" in final_config["markdown_extensions"])
        self.assertTrue(
            "types" in final_config["mdx_configs"]["pymdownx.blocks.admonition"]
        )
        self.assertTrue(
            "types" in final_config["mdx_configs"]["pymdownx.blocks.details"]
        )
        self.assertTrue(
            "alternate_style" in final_config["mdx_configs"]["pymdownx.blocks.tab"]
        )
        self.assertFalse("admonition" in final_config["markdown_extensions"])
        self.assertFalse("pymdownx.details" in final_config["markdown_extensions"])
        self.assertFalse("pymdownx.tabbed" in final_config["markdown_extensions"])
        self.assertFalse("pymdownx.tabbed" in final_config["mdx_configs"])

    def test_default_pymdownx(self):
        self.plugin_collection["techdocs-core"].load_config({})
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)

        self.assertFalse(
            "pymdownx.blocks.admonition" in final_config["markdown_extensions"]
        )
        self.assertFalse(
            "pymdownx.blocks.details" in final_config["markdown_extensions"]
        )
        self.assertFalse("pymdownx.blocks.tab" in final_config["markdown_extensions"])
        self.assertFalse("pymdownx.blocks.admonition" in final_config["mdx_configs"])
        self.assertFalse("pymdownx.blocks.details" in final_config["mdx_configs"])
        self.assertFalse("pymdownx.blocks.tab" in final_config["mdx_configs"])
        self.assertTrue("admonition" in final_config["markdown_extensions"])
        self.assertTrue("pymdownx.details" in final_config["markdown_extensions"])
        self.assertTrue("pymdownx.tabbed" in final_config["markdown_extensions"])
        self.assertTrue(
            "alternate_style" in final_config["mdx_configs"]["pymdownx.tabbed"]
        )
