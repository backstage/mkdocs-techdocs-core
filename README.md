# mkdocs-techdocs-core

This is the base [Mkdocs](https://mkdocs.org) plugin used when using Mkdocs with Spotify's [TechDocs](https://backstage.io/docs/features/techdocs/techdocs-overview). It is written in Python and packages all of our Mkdocs defaults, such as theming, plugins, etc in a single plugin.

[![Package on PyPI](https://img.shields.io/pypi/v/mkdocs-techdocs-core)](https://pypi.org/project/mkdocs-techdocs-core/)

## Usage

> Requires Python version >= 3.8

```bash
$ pip install mkdocs-techdocs-core
```

Once you have installed the `mkdocs-techdocs-core` plugin, you'll need to add it to your `mkdocs.yml`.

```yaml
site_name: Backstage Docs

nav:
  - Home: index.md
  - Developing a Plugin: developing-a-plugin.md

plugins:
  - techdocs-core
```

## Development

### Running Locally

You can install this package locally using `pip` and the `--editable` flag used for making developing Python packages.

```bash
pip install --editable .
```

You'll then have the `techdocs-core` package available to use in Mkdocs and `pip` will point the dependency to this folder.

### Linting

We use [black](https://github.com/psf/black) as our linter. Please run it against your code before submitting a pull request.

```bash
pip install black
black .
```

**Note:** This will write to all Python files in `src/` with the formatted code. If you would like to only check to see if it passes, simply append the `--check` flag.

### Testing Dependencies End-to-End

If you have made changes to the plugin itself, or updated a dependency it's
strongly recommended to test the plugin.

To build a version of the `spotify/techdocs` docker image with your changes,
run the below script in this repository:
```bash
./build-e2e-image.sh
```
_The script is only tested on OSX_

The script assumes that you have the 
[image repository](https://github.com/backstage/techdocs-container) cloned in a
sibling directory to this repository (or you can specify its location).

It will build an image called `mkdocs:local-dev` including the changes you 
have made locally. To test the image in backstage, edit the config (e.g. 
`app-config.yaml`) with the following:

```yaml
techdocs:
  generator:
    runIn: "docker"
    dockerImage: "mkdocs:local-dev"
    pullImage: false
```

### Release

1. Update the [Changelog](https://github.com/backstage/mkdocs-techdocs-core/blob/main/README.md#changelog).
2. Bump up the version number in `setup.py` which triggers the release workflow on [GitHub Actions](.github/workflows/pypi-publish.yml) to publish a new version in PyPI.

## MkDocs plugins and extensions

The TechDocs Core MkDocs plugin comes with a set of extensions and plugins that mkdocs supports. Below you can find a list of all extensions and plugins that are included in the
TechDocs Core plugin:

**Plugins**:

- [search](https://www.mkdocs.org/user-guide/configuration/#search): A search plugin is provided by default with MkDocs which uses [lunr.js](https://lunrjs.com/) as a search engine.
- [mkdocs-monorepo-plugin](https://github.com/backstage/mkdocs-monorepo-plugin): This plugin enables you to build multiple sets of documentation in a single MkDocs project. It is designed to address writing documentation in Spotify's largest and most business-critical codebases (typically monoliths or monorepos).

**Extensions**:

- [admonition](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#admonitions): Admonitions, also known as call-outs, are an excellent choice for including side content without significantly interrupting the document flow. Material for MkDocs provides several different types of admonitions and allows for the inclusion and nesting of arbitrary content.
- [toc](https://python-markdown.github.io/extensions/toc/): The Table of Contents extension generates a Table of Contents from a Markdown document and adds it into the resulting HTML document.
  This extension is included in the standard Markdown library.
- [pymdown](https://facelessuser.github.io/pymdown-extensions/): PyMdown Extensions is a collection of extensions for Python Markdown.
  All extensions are found under the module namespace of pymdownx.
  - caret: Caret is an extension that is syntactically built around the ^ character. It adds support for inserting superscripts and adds an easy way to place <ins>text</ins> in an <_ins_> tag.
  - critic: Critic adds handling and support of Critic Markup.
  - details: Details creates collapsible elements with <_details_> and <_summary_> tags.
  - emoji: Emoji makes adding emoji via Markdown easy 😄.
  - superfences: SuperFences is like Python Markdown's fences, but better. Nest fences under lists, admonitions, and other syntaxes. You can even create special custom fences for content like UML.
  - inlinehilite: InlineHilite highlights inline code: from module import function as func.
  - magiclink: MagicLink linkafies URL and email links without having to wrap them in Markdown syntax. Also, shortens repository issue, pull request, and commit links automatically for popular code hosting providers. You can even use special shorthand syntax to link to issues, diffs, and even mention people
  - mark: Mark allows you to mark words easily.
  - smartsymbols: SmartSymbols inserts commonly used Unicode characters via simple ASCII representations: =/= → ≠.
  - highlight: Highlight allows you to configure the syntax highlighting of SuperFences and InlineHilite. Also passes standard Markdown indented code blocks through the syntax highlighter.
  - extra: Extra is just like Python Markdown's Extra package except it uses PyMdown Extensions to substitute similar extensions.
  - tabbed: Tabbed allows for tabbed Markdown content.
  - tasklist: Tasklist allows inserting lists with check boxes.
  - tilde: Tilde is syntactically built around the ~ character. It adds support for inserting subscripts and adds an easy way to place text in a <_del_> tag.
- [markdown_inline_graphviz](https://pypi.org/project/markdown-inline-graphviz/): A Python Markdown extension replaces inline Graphviz definitions with inline SVGs or PNGs.
  Activate the inline_graphviz extension using the [usage instructions](https://github.com/sprin/markdown-inline-graphviz#usage).

- [plantuml_markdown](https://pypi.org/project/plantuml-markdown/): This plugin implements a block extension which can be used to specify a PlantUML diagram which will be converted into an image and inserted in the document.

  - Note that the format `svg_object` is not supported for rendering diagrams. Read more in the [TechDocs troubleshooting](https://backstage.io/docs/features/techdocs/troubleshooting#plantuml-with-svg_object-doesnt-render) section.

- [mdx_truly_sane_lists](https://pypi.org/project/mdx-truly-sane-lists/): An extension for Python-Markdown that makes lists truly sane. Features custom indents for nested lists and fix for messy linebreaks and paragraphs between lists.

### Other plugins and extensions

Note that the above set of plugins and extensions represents an opinionated
list providing a core set of functionality necessary for most technical
documentation needs (hence: `techdocs-core`). PRs introducing new plugins or
extensions are welcome, but they are not guaranteed to be accepted.

In order to solve your organization's specific needs, you're encouraged to
install any necessary extensions/plugins in your own environment on top of
`techdocs-core` (be it the TechDocs backend container, or a custom TechDocs
build container).

## Caveats

### Theme

We only use `material-mkdocs` as base styles because Backstage also uses the `Material UI` on the client-side. We don't expect people to use themes other than `Material UI` to maintain consistency across all Backstage pages (in other words, documentation pages have the same look and feel as any other Backstage page) and so we use the `BackstageTheme` configured in Front-end application as the source of truth for all application design tokens like colors, typography and etc. So here you can [see](https://github.com/backstage/backstage/blob/master/plugins/techdocs/src/reader/components/TechDocsReaderPageContent/dom.tsx#L160-L692) that some styles will always be overridden regardless of the `mkdocs-material` plugin theme settings and this can cause unexpected behavior for those who override the theme setting in a `mkdocs.yaml` file.

## Changelog

### 1.4.0
 - Updated minimum mkdocs dependency from `1.5` to `1.6`
   - Fixes issue [#187](https://github.com/backstage/mkdocs-techdocs-core/issues/187)
 - mkdocs-material bumped to `9.5.27`

### 1.3.6
 - Bumped `mkdocs-material` to `9.5.26`.
 
### 1.3.5
 - Bumped `mkdocs-material` to `9.5.13` which adds support for card grids and grid layouts

### 1.3.3
 - Bumped `mkdocs-material` to `9.4.14` which add support for: Mermaid.js version 10.6.1, emoji extension and updated MkDocs to 1.5.3
 - Added tests for `Python` version `3.11`

### 1.3.2
 - Bumped `pymdown-extensions` to `10.3.1` which add material.extensions support
 - Removed support for `Python` version `3.7`

### 1.3.1
 - Bumped `pygments` to `2.17.2` which includes JSX support.

### 1.3
 - Bumped `mkdocs-material` (and its dependencies) from `9.1.3` to `9.2.7` causing a few changes:
   - MkDocs dependency is now `1.5`
 - `theme.palette` is now hardcoded to `{}` instead of `""` which caused some issues with some Material plugins

### 1.2.3
 - Bumped `pygments` to `2.16.1`, which also fixes a [vulnerability](https://github.com/advisories/GHSA-mrwq-x4v8-fh7p).
 - Update dependency `plantuml-markdown` to `3.9.2`.

### 1.2.2
 - Added config override of `pymdownx.snippets` for [security](https://github.com/facelessuser/pymdown-extensions/security/advisories/GHSA-jh85-wwv9-24hv). `restrict_base_path` will always be `true`. If you currently use snippets with files outside of the directory, those files will no longer be included. 

### 1.2.1
 - Use latest version of `pymdown-extensions` which contains [security fixes](https://github.com/backstage/mkdocs-techdocs-core/pull/123).

### 1.2.0
 - Updated `mkdocs-material` (and its dependencies) from `8.1.11` to `9.1.3` causing a few changes:
   -  Some `mkdocs-material` features were made opt-in v9. In order to preserve compatibility, they are now hardcoded as enabled by `mkdocs-techdocs-core`. The features are
      -  `navigation.footer`
      -  `content.action.edit`
   -  `theme.palette` is now hardcoded to `""` to preserve previous behavior. Without hardcoding the palette, it gets the value `default`, causing unwanted visual changes. 
   -  Some components e.g. admonitions have a slightly different look.
   -  Minor color changes that can be avoided by also updating to the latest version of `@backstage/plugin-techdocs` which compensates these changes.

### 1.1.7

- Updated `mkdocs-monorepo-plugin` to `1.0.4`, which includes a compatibility
  fix for `mkdocs` versions `1.4.0` and newer.

### 1.1.6

- Removed pins on the `pyparsing` and `Jinja2` dependencies, which are no
  longer needed.
- Pinned `mkdocs-monorepo-plugin` and `markdown_inline_graphviz_extension` to
  specific (latest) releases to improve stability. Going forward, these (along
  with all other feature-related deps) will be bumped regularly and any changes
  will be reflected in this changelog.

### 1.1.5

- Added support for Python 3.10 [#73](https://github.com/backstage/mkdocs-techdocs-core/pull/73)
- Resolved a run-time error introduced in `1.1.4` that prevented sites from
  being built under certain circumstances.

### 1.1.4

- Support markdown version >3.2,<4
- Use markdown_inline_graphviz_extension 1.1.1 which supports svg rendering for markdown >=3.3

### 1.1.3

- Upgraded `plantuml-markdown` to `3.5.1`, which removes `uuid` as a dependency.

### 1.1.2

- Simplify theme code to update only the attribute necessary by backstage.

### 1.1.1

- Fix run-time `AttributeError: 'Theme' object has no attribute 'copy'`

### 1.1.0

- Add new capability to override mkdocs theme attributes

> **Note:** Look the caveats section in readme about the Backstage theme consideration

### 1.0.2

- Bumped `pymdown-extensions` to 9.3 and enabled `pygments_lang_class` to allow easier targeting of codeblocks by language in TechDocs Addons.

### 1.0.1

`Jinja2` pinned to v3.0.3.

### 1.0.0

- This package has been promoted to v1.0!

> **Note:** Going forward, this package will follow [semver](https://semver.org/#semantic-versioning-200) conventions.

### 0.2.3

- Upgrade mkdocs-material and its dependencies

### 0.2.2

- Update `plantuml-markdown` version to 3.5.0 for image maps support

### 0.2.1

- Fix run-time `module 'pyparsing' has no attribute 'downcaseTokens'` error as
  a result of shifting python dependencies.
- Update to latest `mkdocs-monorepo-plugin`, which allows use of `.yaml` file
  extensions and non-slug-like `site_name`s in monorepos.

### 0.2.0

- Add mdx_truly_sane_lists for dealing with the very annoying bullet differences in mkdocs vs commonmark / gf markdown. See https://github.com/backstage/backstage/issues/6057#issuecomment-862822002

### 0.1.2

- Fix the dependency version of Markdown to ensure GraphViz SVG rendering works.

### 0.1.1

- Ensure required mkdocs-monorepo-plugin is compatible with Mkdocs `1.2.x`.

### 0.1.0

- Improved dependency compatibility with other mkdocs plugins.
- Upgraded mkdocs minimum to `1.2.2`

### 0.0.16

- Reused data from `requirements.txt` file in `install_requires` of `setup.py`. [#24](https://github.com/backstage/mkdocs-techdocs-core/pull/24)

### 0.0.15

- Upgrade monorepo to track latest patch, includes various bug fixes. [#22](https://github.com/backstage/mkdocs-techdocs-core/pull/22)

### 0.0.14

- Upgrade plantuml-markdown to 3.4.2 with support for external file sources. [#18](https://github.com/backstage/mkdocs-techdocs-core/pull/18)

### 0.0.13

- Fixed issue where the whole temp directory could be included in the built site output. [#7](https://github.com/backstage/mkdocs-techdocs-core/issues/7)

### 0.0.12

- Updated home repository to be the new https://github.com/backstage/mkdocs-techdocs-core

### 0.0.11

- Any MkDocs plugin configurations from mkdocs.yml will now work and override the default configuration. See https://github.com/backstage/backstage/issues/3017

### 0.0.10

- Pin Markdown version to fix issue with Graphviz

### 0.0.9

- Change development status to 3 - Alpha

### 0.0.8

- Superfences and Codehilite doesn't work very well together (squidfunk/mkdocs-material#1604) so therefore the codehilite extension is replaced by pymdownx.highlight

* Uses pymdownx extensions v.7.1 instead of 8.0.0 to allow legacy_tab_classes config. This makes the techdocs core plugin compatible with the usage of tabs for grouping markdown with the following syntax:

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

- "PyMdown Extensions includes three extensions that are meant to replace their counterpart in the default Python Markdown extensions." Therefore some extensions has been taken away in this version that comes by default from pymdownx.extra which is added now (https://facelessuser.github.io/pymdown-extensions/usage_notes/#incompatible-extensions)

### 0.0.7

- Fix an issue with configuration of emoji support

### 0.0.6

- Further adjustments to versions to find ones that are compatible

### 0.0.5

- Downgrade some versions of markdown extensions to versions that are more stable

### 0.0.4

- Added support for more mkdocs extensions
  - mkdocs-material
  - mkdocs-monorepo-plugin
  - plantuml-markdown
  - markdown_inline_graphviz_extension
  - pygments
  - pymdown-extensions

## License

Copyright 2020-2023 © The Backstage Authors. All rights reserved. The Linux Foundation has registered trademarks and uses trademarks. For a list of trademarks of The Linux Foundation, please see our Trademark Usage page: https://www.linuxfoundation.org/trademark-usage

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
