from pathlib import Path
from typing import Literal
try:
    import ujson as json
except ImportError:
    import json

BIBLE_TRANSLATIONS = (
    "KJV",
    "ESV"
)

BIBLE_CHAPTERS = {
    "Genesis": 50,
    "Exodus": 40,
    "Leviticus": 27,
    "Numbers": 36,
    "Deuteronomy": 34,
    "Joshua": 24,
    "Judges": 21,
    "Ruth": 4,
    "1 Samuel": 31,
    "2 Samuel": 24,
    "1 Kings": 22,
    "2 Kings": 25,
    "1 Chronicles": 29,
    "2 Chronicles": 36,
    "Ezra": 10,
    "Nehemiah": 13,
    "Esther": 10,
    "Job": 42,
    "Psalms": 150,
    "Proverbs": 31,
    "Ecclesiastes": 12,
    "Song of Solomon": 8,
    "Isaiah": 66,
    "Jeremiah": 52,
    "Lamentations": 5,
    "Ezekiel": 48,
    "Daniel": 12,
    "Hosea": 14,
    "Joel": 3,
    "Amos": 9,
    "Obadiah": 1,
    "Jonah": 4,
    "Micah": 7,
    "Nahum": 3,
    "Habakkuk": 3,
    "Zephaniah": 3,
    "Haggai": 2,
    "Zecheriah": 14,
    "Malachi": 4,
    "Matthew": 28,
    "Mark": 16,
    "Luke": 24,
    "John": 21,
    "Acts": 28,
    "Romans": 16,
    "1 Corinthians": 16,
    "2 Corinthians": 13,
    "Galatians": 6,
    "Ephesians": 6,
    "Philippians": 4,
    "Collossians": 4,
    "1 Thessalonians": 5,
    "2 Thessalonians": 5,
    "1 Timothy": 6,
    "2 Timothy": 4,
    "Titus": 3,
    "Philemon": 1,
    "Hebrews": 13,
    "James": 5,
    "1 Peter": 5,
    "2 Peter": 3,
    "1 John": 5, 
    "2 John": 1, 
    "3 John": 1,
    "Jude": 1,
    "Revelation": 22
}

BIBLE_BOOKS = tuple(BIBLE_CHAPTERS.keys())

JSON_FILES = {book: f"{book.replace(' ', '')}.json" for book in BIBLE_BOOKS}

class BibleVerse:
    def __init__(self, book: Literal[BIBLE_BOOKS], chapter: Integer, verse: Integer, text: String, translation: Literal(BIBLE_TRANSLATIONS) = "KJV", api_key: String|None = None):
        if translation not in BIBLE_TRANSLATIONS:
            raise ValueError(f"{translation} is not a supported translation. Please choose KJV or ESV.")
        self.translation = translation
        if book not in BIBLE_BOOKS:
            raise ValueError(f"Invalid value for book: {value}")
        self.book_title = book
        if (chapter < 1) or (chapter > BIBLE_CHAPTERS[self.book_title]):
            raise ValueError(f"{self.book_title} does not contain chapter {chapter}.")
        self.chapter_number = chapter
        self.verse_number = verse
        self.text = text
        self.api_key = api_key

    @property
    def book(self):
        return BibleBook(self.book_title, self.translation, self.api_key)

    @property
    def chapter(self):
        return BibleChapter(self.book_title, self.chapter_number, self.translation, self.api_key)

class BibleChapter:
    def __init__(self, book: Literal[BIBLE_BOOKS], chapter: Integer, translation: Literal(BIBLE_TRANSLATIONS) = "KJV", api_key: String|None = None):
        if translation not in BIBLE_TRANSLATIONS:
            raise ValueError(f"{translation} is not a supported translation. Please choose KJV or ESV.")
        self.translation = translation
        if book not in BIBLE_BOOKS:
            raise ValueError(f"Invalid value for book: {value}")
        self.book_title = book
        if (chapter < 1) or (chapter > BIBLE_CHAPTERS[self.book_title]):
            raise IndexError(f"{self.book_title} does not contain chapter {chapter}.")
        self.chapter = chapter
        self.api_key = api_key

    @property
    def book(self):
        return BibleBook(self.book_title, self.translation, self.api_key)

    # @property
    # def verses(self):
    #     return tuple(BibleVerse(self.title, num, self.translation, self.api_key) for num in range(1, BIBLE_CHAPTERS[self.title]+1))


    def __getitem__(self, index):
        return BibleVerse(
                    self.book_title,
                    self.chapter,
                    index,
                    self.translation,
                    self.api_key
                )
        # match self.translation:
        #     case "KJV":
        #         json_file = Path("./json") / JSON_FILES[self.book_title]
        #         with open(json_file, mode="r") as file: 
        #             data = json.loads(file.read())
        #         chapter = data[str(self.chapter)]
        #         try:
        #             verse = chapter[str(index)]
        #         except KeyError as err:
        #             raise IndexError(f"{self.title} chapter {self.chapter} does not contain verse {index}.") from err
        #         return BibleVerse(
        #             self.book_title,
        #             self.chapter,
        #             index,
        #             self.translation,
        #             self.api_key
        #         )
        #     case "ESV":
        #         print("ESV support is still under construction.")


class BibleBook:
    def __init__(self, book: Literal[BIBLE_BOOKS], translation: Literal(BIBLE_TRANSLATIONS) = "KJV", api_key: String|None = None):
        if translation not in BIBLE_TRANSLATIONS:
            raise ValueError(f"{translation} is not a supported translation. Please choose KJV or ESV.")
        self.translation = translation
        if book not in BIBLE_BOOKS:
            raise ValueError(f"Invalid value for book: {value}")
        self.title = book
        self.api_key = api_key

    def __str__(self):
        return f"BibleBook<{self.title}>"

    def __getitem__(self, index):
        return BibleChapter(self.title, index, self.translation, self.api_key)

    @property
    def chapters(self):
        return tuple(BibleChapter(self.title, num, self.translation, self.api_key) for num in range(1, BIBLE_CHAPTERS[self.title]+1))
