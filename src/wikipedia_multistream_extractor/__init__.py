"""Extracts the XML of each page from the XML dump and writes it to a file."""
import bz2
import re
import sys
from pathlib import Path
from typing import Callable, List, Optional

import click
from tqdm import tqdm

PAGE_ELEMENT_PATTERN = re.compile(r"<page>(.*?)</page>", re.DOTALL)
TITLE_ELEMENT_PATTERN = re.compile(r"<title>(.*)</title>", re.DOTALL)
INVALID_FILENAME_CHARS = re.compile(r'[\\/:\*\?"<>\|]|\.$|^\.')


def make_valid_filename(
    filename: str, replacement: str = "_", max_length: int = 128
) -> str:
    """
    Make a string safe to use as a filename by replacing invalid characters
    with a replacement string and truncating the result to a maximum length.

    Args:
        filename: The filename to make safe.
        replacement: The string to replace invalid characters with.
        max_length: The maximum length of the resulting filename.

    Returns:
        The safe filename."""
    new_filename = re.sub(INVALID_FILENAME_CHARS, replacement, filename)
    new_filename = new_filename[:max_length]
    return new_filename


def extract_page_text(xml_text: str) -> List[str]:
    """Finds the text of each page from the XML dump.

    Args:
        xml_text: The XML dump of Wikipedia articles.

    Returns:
        A list of strings, containing the page element of an article."""
    return re.findall(PAGE_ELEMENT_PATTERN, xml_text)


def extract_wiki_pages(src: str) -> List[str]:
    """Extracts the text of each page from the XML dump.

    Args:
        src: The path to the XML dump.

    Returns:
        A list of strings, containing the page element of an article.
    """
    print(f"Extracting pages from {src}... this may take a while...")
    with bz2.open(src, "rb") as input_file:
        data: bytes = input_file.read()  # type: ignore
        return extract_page_text(data.decode("utf-8"))


def extract_title(page_text: str) -> Optional[str]:
    """Extracts the title of a Wikipedia article from the page element.

    Args:
        page_text: The page element of a Wikipedia article.

    Returns:
        The title of the article, or None if no title was found."""
    if title_match := re.search(TITLE_ELEMENT_PATTERN, page_text):
        return title_match[1]
    return None


def dump_wiki_pages(
    src: str,
    dest: str,
    preprocessor: Optional[Callable] = None,
    writer: Optional[Callable] = None,
) -> None:
    """Extracts the text of each page from the XML dump and writes it to a
    file.

    Args:
        src: The path to the XML dump.
        dest: The path to the output directory.
        preprocessor: A function that takes the page element and title as
            input and returns the page element to be written to the output
            file or None if the page should be skipped.
        writer: A function that takes the page element, title, destination
            directory, and safe title as input and writes the page to a file.

    Returns:
        None.
    """
    pages = extract_wiki_pages(src)
    dest_path = Path(dest)
    dest_path.mkdir(parents=True, exist_ok=True)
    print("Writing pages to files...")
    pages_written = 0
    for page in tqdm(pages):
        page = f"<page>{page}</page>"
        if title := extract_title(page):
            if preprocessor:
                page = preprocessor(page, title)
            if not page:
                continue
            pages_written += 1
            safe_title = make_valid_filename(title)
            if writer:
                writer(page, title, dest_path, safe_title)
            else:
                dest_filepath = dest_path / f"{safe_title}.xml"
                with open(dest_filepath, "w", encoding="utf-8") as output_file:
                    output_file.write(page)
    print(f"Done! Wrote {pages_written} out of {len(pages)} to {dest_path}.")


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.argument("dest", type=click.Path())
def main(src: str, dest: str) -> None:
    """Extracts the XML of each page from the XML dump and writes it to a
    file.

    Args:
        src: The path to the XML dump.
        dest: The path to the output directory.

    Returns:
        None.
    """
    dump_wiki_pages(src, dest)


if __name__ == "__main__":
    main(sys.argv[1:])  # pylint: disable=no-value-for-parameter
