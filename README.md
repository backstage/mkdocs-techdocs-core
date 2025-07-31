# mkdocs-techdocs-core

test 
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

(Optional) To use material theme search to generate the `search/search_index.json` (responsible for the search functionality in the TechDocs reader), you need to add the following configuration to your `mkdocs.yml`:

```yaml
plugins:
  - techdocs-core:
      use_material_search: true
```

(Optional) To use [PyMdown Blocks Extensions](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/) (replaces `admonitions`, `pymdownx.details` and `pymdownx.tabbed` extensions), you need to add the following configuration to your `mkdocs.yml`:

```yaml
plugins:
  - techdocs-core:
      use_pymdownx_blocks: true
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

In order to publish a release, you must manually dispatch the [`manual-versioning`](https://github.com/backstage/mkdocs-techdocs-core/actions/workflows/manual-versioning.yml) GitHub Action. Please see the official GitHub documentation on [Manual Workflows](https://docs.github.com/en/actions/how-tos/managing-workflow-runs-and-deployments/managing-workflow-runs/manually-running-a-workflow?tool=webui) for full instructions.

> [!TIP]
> If you decide to provide an explicit `levelBump`, please respect SemVer. When left empty, PSR will determine the best version bump based on the commits since the previous release. Automatic Versioning does rely on `conventional-commits` which is **not** enforced within this project.

This project utilizes PSR (Python Semantic Release) to create releases.
Release Notes will be generated from commit messages and the [CHANGELOG.md](CHANGELOG.md) will be automatically updated with all commits since the previous release.

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

## [Changelog](CHANGELOG.md)

### Theme

We only use `material-mkdocs` as base styles because Backstage also uses the `Material UI` on the client-side. We don't expect people to use themes other than `Material UI` to maintain consistency across all Backstage pages (in other words, documentation pages have the same look and feel as any other Backstage page) and so we use the `BackstageTheme` configured in Front-end application as the source of truth for all application design tokens like colors, typography and etc. So here you can [see](https://github.com/backstage/backstage/blob/master/plugins/techdocs/src/reader/components/TechDocsReaderPageContent/dom.tsx#L160-L692) that some styles will always be overridden regardless of the `mkdocs-material` plugin theme settings and this can cause unexpected behavior for those who override the theme setting in a `mkdocs.yaml` file.

## License

Copyright 2020-2023 © The Backstage Authors. All rights reserved. The Linux Foundation has registered trademarks and uses trademarks. For a list of trademarks of The Linux Foundation, please see our Trademark Usage page: https://www.linuxfoundation.org/trademark-usage

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
