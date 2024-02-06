"""
E2e test, publishing a page to confluence
"""
import os
from pathlib import Path

import atlassian
import pytest

from confluenpy.content import Page
from confluenpy.markdown import MarkdownToConfluenceConverter

requires_existing_confluence = pytest.mark.skipif("CONFLUENCE_API_TOKEN" not in os.environ, reason="No Confluence API token set")


@pytest.fixture
def confluence():
    """
    Confluence instance
    """
    return atlassian.Confluence(
        url=os.getenv("CONFLUENCE_URL"), username=os.getenv("CONFLUENCE_USERNAME"), password=os.getenv("CONFLUENCE_API_TOKEN")
    )


@pytest.mark.end_to_end
@requires_existing_confluence
def test_publish_page(confluence: atlassian.Confluence):
    """
    Test publishing a page to confluence

    To run this, make sure you have a .env file with the following variables:
    CONFLUENCE_URL: The url for your confluence
    CONFLUENCE_USER: Your confluence username
    CONFLUENCE_API_TOKEN: https://id.atlassian.com/manage-profile/security/api-tokens
    CONFLUENCE_PAGE: a page in your confluence
    CONFLUENCE_SPACE: a space in your confluence
    """

    page = Page(title=os.getenv("CONFLUENCE_PAGE"), space=os.getenv("CONFLUENCE_SPACE"), confluence=confluence)

    # Add a table of contents
    page.body.toc()
    # Add a horizontal rule
    page.body.horizontal_rule()

    # Add the readme
    readme = Path(__file__).parent.parent / "README.md"
    with readme.open(encoding="utf-8") as markdown_text:
        markdown = MarkdownToConfluenceConverter.convert(markdown_text.read())
        page.body.extend(markdown)

    # Update the page
    status = page.update()
    assert status["type"] == "page", status
