"""
Module to convert markdown to confluence wiki markup.
"""

import logging
import re

import validators

from confluenpy.content import PageContent

logger = logging.getLogger(__name__)


class MarkdownToConfluenceConverter:
    """
    Class to convert markdown to confluence wiki markup.
    """

    @staticmethod
    def is_header(text: str) -> bool:
        """
        Check if the given string is a header according to specific rules.
        A string is considered a header if it starts with one or more '#' characters
        followed immediately by a space and then any characters.

        Parameters:
        s (str): The string to check.

        Returns:
        bool: True if the string is a header, False otherwise.
        """
        # Check if the string starts with '#' and has a space after the '#' characters
        if text.startswith("#"):
            # Find the index of the first space after the initial '#' characters
            space_index = text.find(" ")
            # Check if there's a space and it's immediately after the '#' characters
            if space_index > 0 and all(char == "#" for char in text[:space_index]):
                return True
        return False

    @staticmethod
    def is_block_code(text: str) -> bool:
        """
        Check if the given string is a block of code according to specific rules.
        A string is considered a block of code if it starts and ends with three backticks.

        Parameters:
        s (str): The string to check.

        Returns:
        bool: True if the string is a block of code, False otherwise.
        """
        return text.startswith("```")

    @staticmethod
    def is_image(text: str) -> bool:
        """
        Check if the given string is an image according to specific rules.
        A string is considered an image if it starts with '!' and contains an image extension.

        example: ![Drag Racing](Dragster.jpg)

        Parameters:
        s (str): The string to check.

        Returns:
        bool: True if the string is an image, False otherwise.
        """
        return re.match(r".*\!\[.*\]\(.*\.(jpg|jpeg|png|gif|bmp|svg.*)\).*", text)

    @staticmethod
    def emphasis(text: str) -> str:
        """
        Transforms text by replacing single backticks around words with underscores,
        while leaving text within triple backticks unchanged.

        Args:
        text (str): The input string containing words within single or triple backticks.

        Returns:
        str: The transformed string with single backticks replaced by underscores and triple backticks preserved.
        """
        # First, temporarily replace triple backticks with a placeholder to avoid altering them in the next step
        placeholder = "TRIPLEBACKTICK"
        text_with_placeholder = re.sub(r"```", placeholder, text)

        # Replace single backticks with underscores
        text_transformed = re.sub(r"`([^`]*)`", r"_\1_", text_with_placeholder)

        # Restore triple backticks from placeholder
        final_text = re.sub(placeholder, "```", text_transformed)

        return final_text

    @classmethod
    def convert(cls, markdown_text: str) -> PageContent:
        """
        Convert the markdown to confluence wiki markup.

        params:
        markdown_text: string - The markdown text to convert.

        returns:
        confluence_content: ConfluencePageContent - The confluence wiki markup.
        """

        confluence_content = PageContent()

        lines = iter(markdown_text.split("\n"))
        for line in lines:

            line = cls.emphasis(line)

            if cls.is_header(line):
                n_hashes = line.split(" ")[0].count("#")
                confluence_content.heading(f"h{n_hashes}", line[n_hashes + 1 :])

            elif cls.is_block_code(line):
                # Simple approach to capture code block, assuming it starts and ends in the file correctly
                language = line.replace("```", "").strip()
                code_content = []
                line = next(lines)  # Move to the next line to start capturing the code
                while not cls.is_block_code(line):
                    code_content.append(line)
                    line = next(lines)
                confluence_content.code_block(title="", content="\n".join(code_content), language=language)
            elif cls.is_image(line):
                image = re.search(r"(\!\[.*\]\(.*\.(jpg|jpeg|png|gif|bmp|svg\??[a-z=]*)\))", line).group(0)
                # Extract the image title and url
                url = re.search(r"\((.*)\)", image).group(1)
                _title = re.search(r"\[(.*)\]", image).group(1)

                try:
                    assert validators.url(url), f"Invalid URL: {url}"
                    confluence_content.image(url)
                except AssertionError as err:
                    logger.error("Invalid URL %s: %s", url, err)
            else:
                confluence_content.text(line)  # Treat as plain text

        return confluence_content
