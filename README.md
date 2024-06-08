# ConfluenPy

ConfluenPy is a Python package that allows you to interact with Atlassian Confluence via the REST API to programmatically create and update documentation pages content.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![pylint](https://github.com/MarcDuQuesne/confluenpy/actions/workflows/pylint.yml/badge.svg?branch=main)
![Build/Release](https://github.com/MarcDuQuesne/confluenpy/actions/workflows/tag-and-release.yml/badge.svg?branch=main)
![Coverage](https://raw.githubusercontent.com/MarcDuQuesne/confluenpy/main/.github/coverage.svg)

# Example usage

```python
    # Example usage
    confluence = atlassian.Confluence(
        url='https://example.atlassian.net/',
        username='your.user@company.com',
        password=os.getenv('CONFLUENCE_API_TOKEN')
        )

    page = Page(title='WonderDocs', space='IsVast', confluence=confluence)

    # Add a table of contents
    page.body.toc()
    # Add a horizontal rule
    page.body.horizontal_rule()
    # Takes the Readme.md file and converts it to confluence format
    with open('README.md', encoding='utf-8') as markdown_text:
        markdown = MarkdownToConfluenceConverter.convert(markdown_text.read())
        # Only takes the second section of the markdown file
        page.body.content += markdown.section(2)

    # Upload any local images referenced in the markdown
    for file in MarkdownToConfluenceConverter.local_images_to_be_uploaded:
        page.attach_content(
            content=file.open("rb"),
            name=file.name,
        )

    # Adds some more content
    page.body.heading('h1', "Biggest heading")
    page.body.block_quote('This is a paragraph')
    page.body.code_block(title='tt', content='Wonderful code')

    # Update the page
    page.update()
```

# Installation

Simply install the package using pip:

```bash
pip install confluenpy
```

# Usage

Confluence pages are represented by the `Page` class. The page content is handled by a `PageBody` object, which represents it in the [confluence wiki markup](https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html).
The following confluence macros are also supported via the wiki markup (see the `MacroMixin` class for details):
    - `toc`
    - `code block`

## Markup support
The `MarkdownToConfluenceConverter` class allows to convert markdown to confluence wiki markup. The following markdown elements are supported:

    - headings
    - code blocks
    - images (both public and local to the repository, see the example above)
    - links
    - lists (ordered and unordered)

Regular markup notation is also supported (bold, italic..).

### Example:

This content:

```markdown
# Header

## Header

- list level 1
- list level 2

1. numbered list 1
2. numbered list 2

[here](https://www.google.com)
![excalidraw](excalidraw.png)
```

will be converted to:

```confluence
h1. Header

h2. Header

* list level 1
** list level 2

# numbered list 1
## numbered list 2

[here|https://www.google.com]
![excalidraw|excalidraw.png]
```
