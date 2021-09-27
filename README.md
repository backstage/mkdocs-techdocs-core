# mkdocs-techdocs-core

This is the base [Mkdocs](https://mkdocs.org) plugin used when using Mkdocs with Spotify's [TechDocs](https://backstage.io/docs/features/techdocs/techdocs-overview). It is written in Python and packages all of our Mkdocs defaults, such as theming, plugins, etc in a single plugin.

[![Package on PyPI](https://img.shields.io/pypi/v/mkdocs-techdocs-core)](https://pypi.org/project/mkdocs-techdocs-core/)

## Usage

> Requires Python version >= 3.7

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

### Testing Depedencies End-to-End

Much of the value of this plugin lies in its dependencies, on which there are
implicit dependencies upstream in the Backstage TechDocs frontend plugin. Each
time you update a pinned dependency, it's important to test that generated
documentation can be loaded and parsed as expected in the Backstage frontend.
The recommended way to do so is the following:

1. Make the expected dependency change locally in `requirements.txt`.
2. Clone the [techdocs-container](https://github.com/backstage/techdocs-container)
   image and, within the cloned directory, copy the entire contents of your
   local version of `mkdocs-techdocs-core`, e.g. named `local-mkdocs-techdocs-core`.
3. Just before the `RUN pip install` command in `techdocs-container`'s
   Dockerfile, add a `COPY` command that copies the contents of your modified
   `mkdocs-techdocs-core` directory into the container's file system. Something
   like: `COPY ./local-mkdocs-techdocs-core/ /local-mkdocs-techdocs-core/`
4. Modify the `RUN pip install`... command to install an editable version of
   the copied local plugin, rather than the specific version. Something like...
   `RUN pip install --upgrade pip && pip install -e /local-mkdocs-techdocs-core`
5. Build the modified image: `docker build -t mkdocs:local-dev .`
6. Modify your local Backstage instance to use your locally built
   `techdocs-container` instead of using the published image by setting the
   following configuration:

```yaml
techdocs:
  generator:
    runIn: 'docker'
    dockerImage: 'mkdocs:local-dev'
```

### Release

1. Update the [Changelog](https://github.com/backstage/mkdocs-techdocs-core/blob/main/README.md#changelog).
2. Bump up the version number in `setup.py` which triggers the release workflow on [GitHub Actions](.github/workflows/pypi-publish.yml) to publish a new version in PyPI.

## MkDocs plugins and extensions

The TechDocs Core MkDocs plugin comes with a set of extensions and plugins that mkdocs supports. Below you can find a list of all extensions and plugins that are included in the
TechDocs Core plugin:

Plugins:

- [search](https://www.mkdocs.org/user-guide/configuration/#search): A search plugin is provided by default with MkDocs which uses [lunr.js](https://lunrjs.com/) as a search engine.
- [mkdocs-monorepo-plugin](https://github.com/backstage/mkdocs-monorepo-plugin): This plugin enables you to build multiple sets of documentation in a single MkDocs project. It is designed to address writing documentation in Spotify's largest and most business-critical codebases (typically monoliths or monorepos).

Extensions:

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

## Changelog

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

Copyright 2020-2021 © The Backstage Authors. All rights reserved. The Linux Foundation has registered trademarks and uses trademarks. For a list of trademarks of The Linux Foundation, please see our Trademark Usage page: https://www.linuxfoundation.org/trademark-usage

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
