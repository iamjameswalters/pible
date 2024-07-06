# pible

A Python library for working with Bible books and verses.

## Example Usage

```python

from pible import Bible

bible = Bible()

john = bible["John"]

favorite_verse = john[3][16]

print(favorite_verse)
# For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.

john_3_17 = favorite_verse.next_verse()
```

## Translations

### King James Version

The library includes the [text of the KJV](https://github.com/aruljohn/Bible-kjv), which is public domain. 

### English Standard Version

Support is planned for using Crossway's [ESV API](https://api.esv.org/). ESV content is copyrighted by Crossway, and you will have to agree to their terms and conditions when applying for your API key in order to use the ESV within pible.

### Others

Interested in adding support for another translation? PRs welcome 🙂️