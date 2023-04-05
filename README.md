# WikipediaMultistreamExtractor

This is a simple application that extracts articles from Wikipedia backup files.

## Installation

```
pip install wikipedia_multistream_extractor
```

## Usage


From the CLI:
```
 wikipedia_multistream_extractor SRC DEST
```

As a library:
```
from wikipedia_multistream_extractor import dump_wiki_pages, extract_wiki_pages


dump_wiki_pages(src, dst, preprocessor=None, writer=None)

# Or

pages = extract_wiki_pages(src) 
```

You can pass a `preprocessor` to dump_wiki_pages if you wanted to transform the data.
  - Your function should accept two arguments `page` and `title`.
  - It should return the modified `page` as a str, unless your writer expects something different.
  - If you return None the page will be skipped by the writer.

You can also pass a `writer` if the intended output is not xml.
  - Your function should accept four arguments `page`, `title`, `dest_path` and `safe_title`.
  - IF you pass a `writer` it's up to you two write the file, not further action is taken.
  - `safe_title` *should* be a safe filename to use when writing the file, `title` is almost certainly not.

This library was built on Windows using Python 3.9.13.

It *should* work on other platforms but it has not been **tested**.


## License

  The license is MIT, see the LICENSE file for details.


## Contributing

  PRs welcome, please have type annotations and docstrings.


## Todos
  - Extracting a single article, based on the index offsets.
  - Extracting the index files.
  - Create a UI that displays the index file contents and allows the users to select articles.
  - Extracting multiple articles at offsets.
  - Use multiprocessing?
  - Write some tests.