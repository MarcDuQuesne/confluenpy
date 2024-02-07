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


@pytest.mark.unit
def test_convert_header():
    """
    Test the conversion of headers.
    """
    assert MarkdownToConfluenceConverter.convert_header("# Header") == "h1. Header"
    assert MarkdownToConfluenceConverter.convert_header("## Header") == "h2. Header"
    assert MarkdownToConfluenceConverter.convert_header("## Header ##") == "h2. Header ##"


@pytest.mark.unit
def test_convert_link():
    """
    Test the conversion of links.
    """
    assert MarkdownToConfluenceConverter.convert_link("[Link](link)") == "[link]"
