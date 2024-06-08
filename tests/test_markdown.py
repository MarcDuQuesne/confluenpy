"""
Tests for the markdown module.
"""

from pathlib import Path

import pytest

from confluenpy.content import PageContent
from confluenpy.markdown import MarkdownToConfluenceConverter


@pytest.mark.integration
def test_conversion():
    """
    Check that the readme for this project can be added to a confluence page.
    """

    readme = Path(__file__).parent.parent / "README.md"

    with readme.open(encoding="utf-8") as markdown_text:
        markdown = MarkdownToConfluenceConverter.convert(markdown_text.read())
        assert isinstance(markdown, PageContent)


@pytest.mark.integration
def test_string_conversion():
    """
    Check that the readme for this project can be added to a confluence page.
    """

    markdown = """
# Header

## Header

- list level 1
  - list level 2

1. numbered list 1
2. numbered list 2

[here](https://www.google.com)
![excalidraw](excalidraw.png)

"""

    wiki_markdown = """
h1. Header

h2. Header

* list level 1
** list level 2

# numbered list 1
## numbered list 2

[here|https://www.google.com]
![excalidraw|excalidraw.png]

"""

    converted_markup = "\n".join(MarkdownToConfluenceConverter.convert(markdown).content)

    assert converted_markup == wiki_markdown, "Conversion failed"


@pytest.mark.unit
def test_convert_header():
    """
    Test the conversion of headers.
    """
    assert MarkdownToConfluenceConverter.convert_header("# Header") == "h1. Header"
    assert MarkdownToConfluenceConverter.convert_header("## Header") == "h2. Header"
    assert MarkdownToConfluenceConverter.convert_header("## Header ##") == "h2. Header ##"


@pytest.mark.unit
def test_convert_list():
    """
    Test the conversion of headers.
    """
    assert MarkdownToConfluenceConverter.convert_list("- element") == "* element"
    assert MarkdownToConfluenceConverter.convert_list("- *element*") == "* *element*"
    assert MarkdownToConfluenceConverter.convert_list("* *element*") == "* *element*"
    assert MarkdownToConfluenceConverter.convert_list("  - element") == "** element"
    assert MarkdownToConfluenceConverter.convert_list("1. element") == "# element"
    assert MarkdownToConfluenceConverter.convert_list("2. element") == "## element"


@pytest.mark.unit
def test_convert_link():
    """
    Test the conversion of links.
    """
    assert MarkdownToConfluenceConverter.convert_link("[Link](link)") == "[Link|link]"
