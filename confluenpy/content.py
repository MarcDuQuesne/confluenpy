"""
Classes that represent Confluence pages, macros and content.
"""
from typing import List, Literal, Optional, Tuple

from atlassian import Confluence


class TextFormattingMixin:
    """
    Class to add text formatting to the page content.
    """

    @classmethod
    def strong(cls, text: str) -> str:
        """
        Add strong (bold) text to the page.

        example: *strong*
        """
        return f"*{text}*"

    @classmethod
    def emphasis(cls, text: str):
        """
        Add emphasis text to the page.

        example: _emphasis_
        """
        return f"_{text}_"

    @classmethod
    def citation(cls, text: str):
        """
        Add a citation to the page.

        example: ??citation??
        """
        return f"??{text}??"

    @classmethod
    def deleted(cls, text: str):
        """
        Add deleted text to the page.

        example: -deleted-
        """
        return f"-{text}-"

    @classmethod
    def inserted(cls, text: str):
        """
        Add inserted text to the page.

        example: +inserted+
        """
        return f"+{text}+"

    @classmethod
    def subscript(cls, text: str):
        """
        Add subscript text to the page.

        example: ~subscript~
        """
        return f"~{text}~"

    @classmethod
    def superscript(cls, text: str):
        """
        Add superscript text to the page.

        example: ^superscript^
        """
        return f"^{text}^"

    @classmethod
    def monospaced(cls, text: str):
        """
        Add monospaced text to the page.

        example: {{monospaced}}
        """
        return f"{{{{{text}}}}}"

    @classmethod
    def block_quote(cls, text: str):
        """
        Add a block quote to the page.

        example:
            {quote}
            This is a block quote.
            {quote}
        """
        return f"bq. {text}"

    @classmethod
    def color(cls, text: str, color: str):
        """
        Add colored text to the page.

        example: {color:red}red{color}
        """
        return f"{{color:{color}}}{text}{{color}}"

    @classmethod
    def textbreak(cls):
        """
        Add a line break to the page.
        """
        return "\\"


class MacrosMixin:
    """
    Class to add macros to the page content.

    see https://confluence.atlassian.com/doc/macros-139387.html
    """

    # pylint: disable=too-many-arguments
    def toc(
        self,
        printable: bool = False,
        style: Literal["square"] = "square",
        max_level: int = 4,
        indent="5px",
        min_level: int = 1,
        _class: Literal["bigpink"] = "bigpink",
        exclude: Optional[str] = None,
        include: Optional[str] = None,
        _type: Literal["list"] = "list",
        outline: bool = True,
    ):
        """
        Table of contents macro.
        example: {toc:printable=true|style=square|maxLevel=6|indent=5px|minLevel=1|class=bigpink|exclude=[1//2]|type=list|outline=true|include=.*}

        See https://confluence.atlassian.com/doc/table-of-contents-macro-182682099.html

        params:
        minLevel: int (default 1) - The minimum heading level to include in the table of contents.
        maxLevel: int (default 3) - The maximum heading level to include in the table of contents.
        style: string (default square) - The style of the table of contents.
        indent: string (default 5px) - The amount of indentation for each level of the table of contents.
        class: string (default bigpink) - The CSS class to apply to the table of contents.
        include: string - A regular expression to include headings in the table of contents.
        exclude: string - A regular expression to exclude headings from the table of contents.
        type: string  (default list) - The type of table of contents to display.
        outline: boolean (default true) - Whether to display the table of contents as an outline.
        printable: boolean (default false) - Whether to display the table of contents as printable.
        """
        exclude_str = f"|exclude={exclude}" if exclude else ""
        include_str = f"|include={include}" if include else ""
        self.content.append(
            f"{{toc:printable={printable}|style={style}|maxLevel={max_level}|indent={indent}|"
            f"minLevel={min_level}|class={_class}{exclude_str}|type={_type}|outline={outline}|"
            f"{include_str}}}"
        )

    def code_block(
        self,  # pylint: disable=too-many-arguments
        title: str,
        content: str,
        theme: Literal["DJango", "Emacs", "FadeToGrey", "Midnight", "RDark", "Eclipse", "Confluence", "Default"] = "Default",
        linenumbers: bool = False,
        language: Literal[
            "ActionScript",
            "AppleScript",
            "Bash",
            "C#",
            "C++",
            "CSS",
            "ColdFusion",
            "Delphi",
            "Diff",
            "Erlang",
            "Groovy",
            "HTML and XML",
            "Java",
            "Java FX",
            "JavaScript",
            "PHP",
            "Plain Text",
            "PowerShell",
            "Python",
            "Ruby",
            "SQL",
            "Sass",
            "Scala",
            "Visual Basic",
            "YAML",
        ] = "java",
        firstline: int = 1,
        collapse: bool = False,
    ):
        """
        Code block macro.

        example: {code:title=This is my title|theme=FadeToGrey|linenumbers=true|language=java|firstline=0001|collapse=true}
        """

        self.content.append(
            f"{{code:title={title}|theme={theme}|linenumbers={linenumbers}|"
            f"language={language}|firstline={firstline}|collapse={collapse}}}"
            f"{content}{{code}}"
        )


class PageContent(MacrosMixin, TextFormattingMixin):
    """
    Class to create a confluence page content in the 'wiki markup' style.

    see https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html
    """

    def __init__(self):
        self.content = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # No action needed on exit

    def append(self, content: str):
        """
        Append content to the page.

        params:
        content: string - The content to append.
        """
        self.content.append(content)

    def extend(self, content: "PageContent"):
        """
        Extend the page content.

        params:
        content: list - The content to extend with.
        """
        self.content.extend(content.content)

    def heading(self, heading: Literal["h1", "h2", "h3", "h4", "h5", "h6"], text: str):
        """
        Add a heading to the page.

        example: h1. My heading

        params:
        heading: string - The heading level (h1, h2, h3, h4, h5, h6).
        text: string - The text of the heading.
        """
        self.content.append(f"{heading}. {text}")

    def horizontal_rule(self):
        """
        Add a horizontal rule to the page.
        """
        self.content.append("----")

    # pylint: disable=too-many-arguments
    def image(
        self,
        url: str,
        title: Optional[str] = None,
        align: Optional[Literal["left", "right", "bottom", "center", "top"]] = None,
        border: Optional[int] = None,
        bordercolor: Optional[str] = None,
        hspace: Optional[int] = None,
        vspace: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        alt: Optional[str] = None,
        thumbnail: Optional[bool] = None,
    ):
        """
        Add an image to the page with various customization options.

        :param title: Specifies alternate text for the image, displayed when the pointer hovers over the image.
        :param url: The URL of the image to be added.
        :param align: The alignment of the image within the page. Available values are 'left', 'right', 'bottom', 'center', 'top'. Optional.
        :param border: Specifies the width of the border around the image (in pixels). Optional.
        :param bordercolor: Specifies the color of the border. Use color names or hex values. Optional.
        :param hspace: Specifies the horizontal space (in pixels) to be inserted to the left and right of the image. Optional.
        :param vspace: Specifies the vertical space (in pixels) to be inserted above and below the image. Optional.
        :param width: Specifies the width of the image (in pixels), overriding the natural width. Optional.
        :param height: Specifies the height of the image (in pixels), overriding the natural height. Optional.
        :param alt: Specifies alternate text for the image for accessibility and is retrievable via search. Optional.

        Example usage:
            image(title="My image", url="http://www.example.com/image.jpg")
        """

        title = f"title={title}" if title else ""
        align = f", align={align}" if align else ""
        border = f", border={border}" if border else ""
        bordercolor = f", bordercolor={bordercolor}" if bordercolor else ""
        hspace = f", hspace={hspace}" if hspace else ""
        vspace = f", vspace={vspace}" if vspace else ""
        width = f", width={width}" if width else ""
        height = f", height={height}" if height else ""
        alt = f", alt={alt}" if alt else ""
        thumbnail = f", thumbnail={thumbnail}" if thumbnail else ""

        self.content.append(f"!{url}|{title}{align}{border}{bordercolor}{hspace}{vspace}{width}{height}{alt}{thumbnail}!")

    @classmethod
    def divide_into_sections(cls, content: List, level: int) -> List:
        """
        Divides lines into sections based on the level of the header.
        Note that the first section is always the content before the first header.

        params:
        content: list - The lines to divide.
        level: int - The level of the header.

        returns:
        sections: list - The sections.
        """
        cnt = iter(content)
        current_section_n = -1
        sections = []
        section = []
        for line in cnt:
            if line.startswith(f"h{level+1}"):
                sections.append(section)
                section = []
                current_section_n += 1
            section.append(line)

        sections.append(section)
        return sections

    def section(self, section_number: Tuple) -> List:
        """
        Select a (sub)section from the document

        example: section((1,2)) selects the second subsection of the first section
        """
        lines = self.content
        if isinstance(section_number, int):  # single section
            section_number = [section_number]

        for level, section in enumerate(section_number):
            lines = self.divide_into_sections(lines, level)[section]
        return lines

    def _list(self, items: List, style: Literal["-", "*", "**", "***", "****"] = "-"):  # past 4 levels you're on your own
        """
        Add a list to the page.

        example:
               - item 1
               - item 2
        """
        for item in items:
            self.content.append(f"{style} {item}\n")

    def numbered_list(self, items: List, style=Literal["#", "##", "###", "####"]):  # past 4 levels you're on your own
        """
        Add a list to the page.

        example:
                  1. Here's a sentence.
                        a. This is a sub-list point.
                        b. And a second sub-list point.
        """
        for item in items:
            self.content.append(f"{style} {item}\n")

    def table(self):
        """
        Add a table to the page.

        example:
            {section:border=true}
            {column:width=30%}
            Text for this column goes here. This is  the smaller column with a width of only 30%.
            {column}
            {column:width=70%}
            Text for this column goes here. This is  the larger column with a width of 70%.
            {column}
            {section}
        """

    def text(self, text: str):
        """
        Add text to the page.

        example: This is a paragraph
        """
        self.content.append(text)

    def render(self):
        """
        Render the page content.
        """
        return "\n".join(self.content)


class Page:
    """
    A class to represent a Confluence page.

    params:
    title: string - The title of the page.
    space: string - The space of the page.
    confluence: Confluence - The Confluence connector.
    """

    def __init__(self, title: str, space: str, confluence: Confluence):
        self.title = title
        self.space = space
        self.confluence = confluence
        self.body = PageContent()

    @property
    def page_id(self):
        """
        Get the page ID.

        returns:
        page_id: int - The page ID.
        """
        return self.confluence.get_page_id(self.space, self.title)

    def page_exists(self) -> bool:
        """
        Check if a page exists in Confluence.

        returns:
        exists: bool - Whether the page exists.
        """
        return self.confluence.page_exists(space=self.space, title=self.title, type="page")

    def update(self, minor_edit: bool = False, full_width: bool = False) -> dict:
        """
        Update the body of a page in Confluence.

        params:
        body: ConfluencePageContent - The content of the page.
        minor_edit: bool (default False) - Whether the edit is minor.
        full_width: bool (default False) - Whether the page is full width.

        returns:
        status: dict - The status of the page update.
        """
        status = self.confluence.update_page(
            page_id=self.page_id,
            title=self.title,
            body=self.body.render(),
            parent_id=None,
            type="page",
            representation="wiki",
            minor_edit=minor_edit,
            full_width=full_width,
        )
        return status
