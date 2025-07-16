"""
Tests for pages and content
"""
import atlassian
import pytest
from pytest_mock import MockerFixture

from confluenpy.content import Page


@pytest.fixture
def confluence(mocker: MockerFixture):
    """
    Fixture to create a confluence connector
    """

    confluence = atlassian.Confluence(
        url="https://example.atlassian.net/",
        username="your.user@company.com",
        password="my_secret_password",
    )

    mocker.patch("atlassian.confluence.Confluence.get_page_id", return_value=123)

    return confluence


@pytest.fixture
def page(confluence: atlassian.Confluence):
    """
    Fixture to create a confluence connector
    """

    return Page(title="WonderDocs", space="IsVast", confluence=confluence)


@pytest.mark.unit
def test_page_elements(page: Page):
    """
    Test creating a page
    """

    # Add a table of contents
    page.body.toc()
    # Add a horizontal rule
    page.body.horizontal_rule()
    # Add a header
    page.body.heading("h1", "Header")
    # Add a paragraph
    page.body.text("Paragraph")
