# CHANGELOG

<!-- version list -->
## v1.5.4 (2025-06-26)

- Added proper plugin config to fix `Unrecognised configuration name` error when any config is provided

## 1.5.3

- Added support for PyMdown Blocks extensions

## 1.5.2

- Update `markdown_inline_graphviz_extension` to use forked `markdown-graphviz-inline` instead due to abandonment of original dependency.

## 1.5.1

- Minimum supported Python version is now 3.9
- Update dependency `mkdocs-material` to v9.5.46
- Update dependency `mkdocs-redirects` to v1.2.2

## 1.5.0

- Renamed package namespace from `src` to `techdocs_core`
- Fix small deprecation in tests (`assertEquals` -> `assertEqual`) as it was deprecated since Python 3.2 and removed in 3.12

## 1.4.2

- Fixes an issue where individual extension configurations were being ignored if the extension was included within `pymdownx.extra`. See [#147](https://github.com/backstage/mkdocs-techdocs-core/issues/147)

## 1.4.1

- Introduced mkdocs-redirects plugin (v`1.2.1`).

## 1.4.0

- Updated minimum mkdocs dependency from `1.5` to `1.6`
  - Fixes issue [#187](https://github.com/backstage/mkdocs-techdocs-core/issues/187)
- mkdocs-material bumped to `9.5.27`

## 1.3.6

- Bumped `mkdocs-material` to `9.5.26`.

## 1.3.5

- Bumped `mkdocs-material` to `9.5.13` which adds support for card grids and grid layouts

## 1.3.3

- Bumped `mkdocs-material` to `9.4.14` which add support for: Mermaid.js version 10.6.1, emoji extension and updated MkDocs to 1.5.3
- Added tests for `Python` version `3.11`

## 1.3.2

- Bumped `pymdown-extensions` to `10.3.1` which add material.extensions support
- Removed support for `Python` version `3.7`

## 1.3.1

- Bumped `pygments` to `2.17.2` which includes JSX support.

## 1.3

- Bumped `mkdocs-material` (and its dependencies) from `9.1.3` to `9.2.7` causing a few changes:
  - MkDocs dependency is now `1.5`
- `theme.palette` is now hardcoded to `{}` instead of `""` which caused some issues with some Material plugins

## 1.2.3

- Bumped `pygments` to `2.16.1`, which also fixes a [vulnerability](https://github.com/advisories/GHSA-mrwq-x4v8-fh7p).
- Update dependency `plantuml-markdown` to `3.9.2`.

## 1.2.2

- Added config override of `pymdownx.snippets` for [security](https://github.com/facelessuser/pymdown-extensions/security/advisories/GHSA-jh85-wwv9-24hv). `restrict_base_path` will always be `true`. If you currently use snippets with files outside of the directory, those files will no longer be included.

## 1.2.1

- Use latest version of `pymdown-extensions` which contains [security fixes](https://github.com/backstage/mkdocs-techdocs-core/pull/123).

## 1.2.0

- Updated `mkdocs-material` (and its dependencies) from `8.1.11` to `9.1.3` causing a few changes:
  - Some `mkdocs-material` features were made opt-in v9. In order to preserve compatibility, they are now hardcoded as enabled by `mkdocs-techdocs-core`. The features are
    - `navigation.footer`
    - `content.action.edit`
  - `theme.palette` is now hardcoded to `""` to preserve previous behavior. Without hardcoding the palette, it gets the value `default`, causing unwanted visual changes.
  - Some components e.g. admonitions have a slightly different look.
  - Minor color changes that can be avoided by also updating to the latest version of `@backstage/plugin-techdocs` which compensates these changes.

## 1.1.7

- Updated `mkdocs-monorepo-plugin` to `1.0.4`, which includes a compatibility
  fix for `mkdocs` versions `1.4.0` and newer.

## 1.1.6

- Removed pins on the `pyparsing` and `Jinja2` dependencies, which are no
  longer needed.
- Pinned `mkdocs-monorepo-plugin` and `markdown_inline_graphviz_extension` to
  specific (latest) releases to improve stability. Going forward, these (along
  with all other feature-related deps) will be bumped regularly and any changes
  will be reflected in this changelog.

## 1.1.5

- Added support for Python 3.10 [#73](https://github.com/backstage/mkdocs-techdocs-core/pull/73)
- Resolved a run-time error introduced in `1.1.4` that prevented sites from
  being built under certain circumstances.

## 1.1.4

- Support markdown version >3.2,<4
- Use markdown_inline_graphviz_extension 1.1.1 which supports svg rendering for markdown >=3.3

## 1.1.3

- Upgraded `plantuml-markdown` to `3.5.1`, which removes `uuid` as a dependency.

## 1.1.2

- Simplify theme code to update only the attribute necessary by backstage.

## 1.1.1

- Fix run-time `AttributeError: 'Theme' object has no attribute 'copy'`

## 1.1.0

- Add new capability to override mkdocs theme attributes

> **Note:** Look the caveats section in readme about the Backstage theme consideration

## 1.0.2

- Bumped `pymdown-extensions` to 9.3 and enabled `pygments_lang_class` to allow easier targeting of codeblocks by language in TechDocs Addons.

## 1.0.1

`Jinja2` pinned to v3.0.3.

## 1.0.0

- This package has been promoted to v1.0!

> **Note:** Going forward, this package will follow [semver](https://semver.org/#semantic-versioning-200) conventions.

## 0.2.3

- Upgrade mkdocs-material and its dependencies

## 0.2.2

- Update `plantuml-markdown` version to 3.5.0 for image maps support

## 0.2.1

- Fix run-time `module 'pyparsing' has no attribute 'downcaseTokens'` error as
  a result of shifting python dependencies.
- Update to latest `mkdocs-monorepo-plugin`, which allows use of `.yaml` file
  extensions and non-slug-like `site_name`s in monorepos.

## 0.2.0

- Add mdx_truly_sane_lists for dealing with the very annoying bullet differences in mkdocs vs commonmark / gf markdown. See <https://github.com/backstage/backstage/issues/6057#issuecomment-862822002>

## 0.1.2

- Fix the dependency version of Markdown to ensure GraphViz SVG rendering works.

## 0.1.1

- Ensure required mkdocs-monorepo-plugin is compatible with Mkdocs `1.2.x`.

## 0.1.0

- Improved dependency compatibility with other mkdocs plugins.
- Upgraded mkdocs minimum to `1.2.2`

## 0.0.16

- Reused data from `requirements.txt` file in `install_requires` of `setup.py`. [#24](https://github.com/backstage/mkdocs-techdocs-core/pull/24)

## 0.0.15

- Upgrade monorepo to track latest patch, includes various bug fixes. [#22](https://github.com/backstage/mkdocs-techdocs-core/pull/22)

## 0.0.14

- Upgrade plantuml-markdown to 3.4.2 with support for external file sources. [#18](https://github.com/backstage/mkdocs-techdocs-core/pull/18)

## 0.0.13

- Fixed issue where the whole temp directory could be included in the built site output. [#7](https://github.com/backstage/mkdocs-techdocs-core/issues/7)

## 0.0.12

- Updated home repository to be the new <https://github.com/backstage/mkdocs-techdocs-core>

## 0.0.11

- Any MkDocs plugin configurations from mkdocs.yml will now work and override the default configuration. See <https://github.com/backstage/backstage/issues/3017>

## 0.0.10

- Pin Markdown version to fix issue with Graphviz

## 0.0.9

- Change development status to 3 - Alpha

## 0.0.8

- Superfences and Codehilite doesn't work very well together (squidfunk/mkdocs-material#1604) so therefore the codehilite extension is replaced by pymdownx.highlight

- Uses pymdownx extensions v.7.1 instead of 8.0.0 to allow legacy_tab_classes config. This makes the techdocs core plugin compatible with the usage of tabs for grouping markdown with the following syntax:

````
    ```java tab="java 2"
        public void function() {
            ....
        }
    ```
````

as well as the new

````
    === "Java"

    ```java
    public void function() {
        ....
    }
    ```
````

The pymdownx extension will be bumped too 8.0.0 in the near future.

- pymdownx.tabbed is added to support tabs to group markdown content, such as codeblocks.

- "PyMdown Extensions includes three extensions that are meant to replace their counterpart in the default Python Markdown extensions." Therefore some extensions has been taken away in this version that comes by default from pymdownx.extra which is added now (<https://facelessuser.github.io/pymdown-extensions/usage_notes/#incompatible-extensions>)

## 0.0.7

- Fix an issue with configuration of emoji support

## 0.0.6

- Further adjustments to versions to find ones that are compatible

## 0.0.5

- Downgrade some versions of markdown extensions to versions that are more stable

## 0.0.4

- Added support for more mkdocs extensions
  - mkdocs-material
  - mkdocs-monorepo-plugin
  - plantuml-markdown
  - markdown_inline_graphviz_extension
  - pygments
  - pymdown-extensions
