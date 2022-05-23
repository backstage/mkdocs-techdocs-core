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


class DummyTechDocsCorePlugin(plugins.BasePlugin):
    pass


class TestTechDocsCoreConfig(unittest.TestCase):
    def setUp(self):
        self.techdocscore = TechDocsCore()
        self.plugin_collection = plugins.PluginCollection()
        plugin = DummyTechDocsCorePlugin()
        self.plugin_collection["techdocs-core"] = plugin
        self.mkdocs_yaml_config = {"plugins": self.plugin_collection}
        # Note: in reality, config["theme"] is always an instance of Theme
        self.mkdocs_yaml_config["theme"] = get_default_theme()

    def test_removes_techdocs_core_plugin_from_config(self):
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertTrue("techdocs-core" not in final_config["plugins"])

    def test_merge_default_config_and_user_config(self):
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
        ## we want to force the theme mkdocs to this test
        self.mkdocs_yaml_config["theme"] = Theme(name="mkdocs")
        self.mkdocs_yaml_config["theme"]["features"] = ["navigation.sections"]
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertFalse("navigation.sections" in final_config["theme"]["features"])

    def test_theme_overrides_when_name_is_material(self):
        self.mkdocs_yaml_config["theme"] = Theme(name=TECHDOCS_DEFAULT_THEME)
        self.mkdocs_yaml_config["theme"]["features"] = ["navigation.sections"]
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertTrue("navigation.sections" in final_config["theme"]["features"])

    def test_theme_overrides_techdocs_metadata(self):
        self.mkdocs_yaml_config["theme"] = Theme(
            name=TECHDOCS_DEFAULT_THEME, static_templates=["my_static_temples"]
        )
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertTrue("my_static_temples" in final_config["theme"].static_templates)
        self.assertTrue(
            "techdocs_metadata.json" in final_config["theme"].static_templates
        )

    def test_theme_overrides_dirs(self):
        custom_theme_dir = "/tmp/my_custom_theme_dir"
        self.mkdocs_yaml_config["theme"] = Theme(name=TECHDOCS_DEFAULT_THEME)
        self.mkdocs_yaml_config["theme"].dirs.append(custom_theme_dir)
        final_config = self.techdocscore.on_config(self.mkdocs_yaml_config)
        self.assertTrue(custom_theme_dir in final_config["theme"].dirs)
        self.assertTrue(
            self.techdocscore.tmp_dir_techdocs_theme.name in final_config["theme"].dirs
        )

    def test_template_renders__multiline_value_as_valid_json(self):
        self.techdocscore.on_config(self.mkdocs_yaml_config)
        env = Environment(
            loader=PackageLoader("test", self.techdocscore.tmp_dir_techdocs_theme.name),
            autoescape=select_autoescape(),
        )
        template = env.get_template("techdocs_metadata.json")
        config = {
            "site_name": "my site",
            "site_description": "my very\nlong\nsite\ndescription",
        }
        rendered = template.render(config=config)
        as_json = json.loads(rendered)
        self.assertEquals(config, as_json)
