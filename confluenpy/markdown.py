"""
Module to convert markdown to confluence wiki markup.
"""

from confluenpy.content import PageContent


class MarkdownToConfluenceConverter:
    """
    Class to convert markdown to confluence wiki markup.
    """

    @staticmethod
    def is_header(s: str) -> bool:
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
        if s.startswith('#'):
            # Find the index of the first space after the initial '#' characters
            space_index = s.find(' ')
            # Check if there's a space and it's immediately after the '#' characters
            if space_index > 0 and all(char == '#' for char in s[:space_index]):
                return True
        return False

    @staticmethod
    def is_block_code(s: str) -> bool:
        """
        Check if the given string is a block of code according to specific rules.
        A string is considered a block of code if it starts and ends with three backticks.

        Parameters:
        s (str): The string to check.

        Returns:
        bool: True if the string is a block of code, False otherwise.
        """
        return s.startswith('```')

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

        lines = iter(markdown_text.split('\n'))
        for line in lines:
            if cls.is_header(line):
                n_hashes = line.split(' ')[0].count('#')
                confluence_content.heading(f'h{n_hashes}', line[n_hashes+1:])

            elif cls.is_block_code(line):
                # Simple approach to capture code block, assuming it starts and ends in the file correctly
                language = line.replace('```', '').strip()
                code_content = []
                line = next(lines)  # Move to the next line to start capturing the code
                while not cls.is_block_code(line):
                    code_content.append(line)
                    line = next(lines)
                confluence_content.code_block(title="", content='\n'.join(code_content), language=language)
            else:
                confluence_content.text(line)  # Treat as plain text

        return confluence_content
