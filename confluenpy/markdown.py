"""
Module to convert markdown to confluence wiki markup.
"""

import logging
import re
from pathlib import Path

import validators

from confluenpy.content import PageContent
from typing import Optional

logger = logging.getLogger(__name__)


class MarkdownToConfluenceConverter:
    """
    Class to convert markdown to confluence wiki markup.
    """

    local_images_to_be_uploaded = []

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
        s (str): The string to check

        Returns:
        bool: True if the string is an image, False otherwise.
        """
        return re.match(r".*\!\[.*\]\(.*\.(jpg|jpeg|png|gif|bmp|svg.*)\).*", text)

    @staticmethod
    def convert_image(text: str, image_width: Optional[int] = None) -> str:
        """
        Convert a Markdown image to Confluence Wiki markup image.

        example: ![Drag Racing](Dragster.jpg)

        Args:
        text (str): A string containing an image in Markdown format.

        Returns:
        str: A string containing the image in Confluence Wiki markup format.
        """

        # Regular expression to match Markdown image format and convert to Confluence Wiki markup
        match_regex = r"!\[(.*?)\]\((.*\.(jpg|jpeg|png|gif|bmp|svg)[^\)]*)?\)"

        # search for the image in the text
        for match in re.findall(match_regex, text):
            # Extract the image title and url
            _title = match[0]
            url = match[1]
            try:
                assert validators.url(url), f"Invalid URL: {url}"
                text = re.sub(match_regex, f"!{url}!", text)
            except AssertionError as err:
                # check if the image is local
                local_file = Path(url)
                if Path(url).exists():
                    logger.warning("Local image detected: %s", url)  # MG possible issue with path. Is this the relative path to the markdown?
                    text = re.sub(match_regex, f"!{local_file.name}!", text)

                    # If image_width is provided, append it to the local file name
                    if image_width:
                        text = text[:-1] + f"|width={image_width}!"

                    # add the local image to the list of images to be uploaded
                    MarkdownToConfluenceConverter.local_images_to_be_uploaded.append(local_file)
                else:
                    logger.error("Invalid URL %s: %s", url, err)

        return text

    @staticmethod
    def convert_emphasis(text: str) -> str:
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

    @staticmethod
    def convert_link(text: str) -> str:
        """
        Convert a Markdown link to Confluence Wiki markup link.

        Args:
        link_markdown (str): A string containing a link in Markdown format.

        Returns:
        str: A string containing the link in Confluence Wiki markup format.
        """
        # Regular expression to match Markdown link format
        # markdown_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        # matches = re.findall(markdown_link_pattern, text)

        # converted_line = re.sub(r"\[.*\]\((http[s]?[^)]+)\)", r"['\1]", text)
        converted_line = re.sub(r"\[(.*)\]\((.*)\)", r"[\1|\2]", text)
        return converted_line

    @staticmethod
    def convert_header(text: str) -> str:
        """
        Convert a Markdown header to Confluence Wiki markup header.

        Args:
        text (str): A string containing a header in Markdown format.

        Returns:
        str: A string containing the header in Confluence Wiki markup format.
        """
        # Regular expression to match Markdown header format and convert to Confluence Wiki markup
        converted_line = re.sub(r"^(#+)\s*(.*?)$", lambda m: f"h{len(m.group(1))}. {m.group(2)}", text)

        return converted_line

    @staticmethod
    def convert_list(text: str) -> str:
        """
        Convert a Markdown simple or numbered list to Confluence Wiki markup equivalent.

        Args:
        text (str): A string containing a list element in Markdown format.

        Returns:
        str: A string containing the list in Confluence Wiki markup format.
        """

        def simple_list_match(match: str) -> str:
            spaces = match.group(1)
            item = match.group(3)
            stars = "*" * int(len(spaces) / 2 + 1)
            return f"{stars} {item}"

        # Use regex to match lines with leading spaces followed by '- item'
        pattern = re.compile(r"^(\s*)([-*]) (.*)$", re.MULTILINE)
        text = pattern.sub(simple_list_match, text)

        def numbered_list_match(match: str) -> str:
            number = int(match.group(1))
            item = match.group(2)
            hashes = "#" * number
            return f"{hashes} {item}"

        # Use regex to match lines with leading numbers followed by a space and text
        pattern = re.compile(r"^(\d+)\. (.*)$", re.MULTILINE)
        text = pattern.sub(numbered_list_match, text)
        return text

    @classmethod
    def convert(cls, markdown_text: str, image_width: Optional[int] = None) -> PageContent:
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

            # Order matters!
            line = cls.convert_emphasis(line)
            line = cls.convert_image(line, image_width=image_width)
            line = cls.convert_link(line)
            line = cls.convert_header(line)
            line = cls.convert_list(line)

            if cls.is_block_code(line):
                # Simple approach to capture code block, assuming it starts and ends in the file correctly
                language = line.replace("```", "").strip()
                code_content = []
                line = next(lines)  # Move to the next line to start capturing the code
                while not cls.is_block_code(line):
                    code_content.append(line)
                    line = next(lines)
                confluence_content.code_block(title="", content="\n".join(code_content), language=language)
            # elif cls.is_image(line):
            #     image = re.search(r"(\!\[.*\]\(.*\.(jpg|jpeg|png|gif|bmp|svg\??[a-z=]*)\))", line).group(0)
            #     # Extract the image title and url
            #     url = re.search(r"\((.*)\)", image).group(1)
            #     _title = re.search(r"\[(.*)\]", image).group(1)

            #     try:
            #         assert validators.url(url), f"Invalid URL: {url}"
            #         confluence_content.image(url)
            #     except AssertionError as err:
            #         logger.error("Invalid URL %s: %s", url, err)
            else:
                confluence_content.text(line)  # Treat as plain text

        return confluence_content
