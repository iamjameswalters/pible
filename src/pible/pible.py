from pathlib import Path

try:
    import ujson as json
except ImportError:
    import json

BIBLE_TRANSLATIONS = ("KJV", "ESV")

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
    "Zechariah": 14,
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
    "Colossians": 4,
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
    "Revelation": 22,
}

BIBLE_BOOKS = tuple(BIBLE_CHAPTERS.keys())


class BibleVerse:
    text = ""

    def __init__(
        self,
        book: str,
        chapter: int,
        verse: int,
        translation: str = "KJV",
        api_key: str | None = None,
    ):
        if translation not in BIBLE_TRANSLATIONS:
            raise ValueError(
                f"{translation} is not a supported translation. Please choose KJV or ESV."
            )
        self.translation = translation
        if book not in BIBLE_BOOKS:
            raise ValueError(
                f"Invalid value for book: {book}. Must be one of: {BIBLE_BOOKS}"
            )
        self._book_title = book
        if (chapter < 1) or (chapter > BIBLE_CHAPTERS[self._book_title]):
            raise ValueError(f"{self._book_title} does not contain chapter {chapter}.")
        self._chapter_number = chapter
        self._verse_number = verse
        self.api_key = api_key

    @property
    def book(self):
        return BibleBook(self._book_title, self.translation, self.api_key)

    @property
    def chapter(self):
        return BibleChapter(
            self._book_title, self._chapter_number, self.translation, self.api_key
        )

    def __repr__(self):
        return f"BibleVerse<{self._book_title} {self._chapter_number}:{self._verse_number}>"

    def __str__(self):
        if self.text == "":
            match self.translation:
                case "KJV":
                    json_file = (
                        Path(__file__).parent
                        / f"kjv_json/{self._book_title.replace(' ', '')}.json"
                    )
                    with open(json_file, mode="r", encoding="utf8") as file:
                        data = json.loads(file.read())
                    chapter = data[str(self._chapter_number)]
                    try:
                        verse_text = chapter[str(self._verse_number)]
                    except KeyError:
                        raise IndexError(
                            f"{self._book_title} chapter {self._chapter_number} does not contain verse {self._verse_number}."
                        )
                    self.text = verse_text
                case "ESV":
                    print("ESV support is still under construction.")
        return self.text


class BibleChapter:
    def __init__(
        self,
        book: str,
        chapter: int,
        translation: str = "KJV",
        api_key: str | None = None,
    ):
        if translation not in BIBLE_TRANSLATIONS:
            raise ValueError(
                f"{translation} is not a supported translation. Please choose KJV or ESV."
            )
        self.translation = translation
        if book not in BIBLE_BOOKS:
            raise ValueError(
                f"Invalid value for book: {book}. Must be one of: {BIBLE_BOOKS}"
            )
        self._book_title = book
        if (chapter < 1) or (chapter > BIBLE_CHAPTERS[self._book_title]):
            raise IndexError(f"{self._book_title} does not contain chapter {chapter}.")
        self._chapter_number = chapter
        self.api_key = api_key

    @property
    def book(self):
        return BibleBook(self._book_title, self.translation, self.api_key)

    @property
    def verses(self):
        return tuple(
            BibleVerse(
                self._book_title,
                self._chapter_number,
                num,
                self.translation,
                self.api_key,
            )
            for num in range(1, BIBLE_CHAPTERS[self._book_title] + 1)
        )

    def __getitem__(self, index):
        return BibleVerse(
            self._book_title,
            self._chapter_number,
            index,
            self.translation,
            self.api_key,
        )

    def __repr__(self):
        return f"BibleChapter<{self._book_title} {self._chapter_number}>"


class BibleBook:
    def __init__(self, book: str, translation: str = "KJV", api_key: str | None = None):
        if translation not in BIBLE_TRANSLATIONS:
            raise ValueError(
                f"{translation} is not a supported translation. Please choose KJV or ESV."
            )
        self.translation = translation
        if book not in BIBLE_BOOKS:
            raise ValueError(
                f"Invalid value for book: {book}. Must be one of: {BIBLE_BOOKS}"
            )
        self._title = book
        self.api_key = api_key

    def __repr__(self):
        return f"BibleBook<{self._title}>"

    def __getitem__(self, index):
        return BibleChapter(self._title, index, self.translation, self.api_key)

    @property
    def chapters(self):
        return tuple(
            BibleChapter(self._title, num, self.translation, self.api_key)
            for num in range(1, BIBLE_CHAPTERS[self._title] + 1)
        )


class Bible:
    def __init__(self, translation: str = "KJV", api_key: str | None = None):
        if translation not in BIBLE_TRANSLATIONS:
            raise ValueError(
                f"{translation} is not a supported translation. Please choose KJV or ESV."
            )
        self.translation = translation
        self.api_key = api_key

    def __repr__(self):
        return "<pible Bible class>"

    def __getitem__(self, book):
        return BibleBook(book, self.translation, self.api_key)

    @property
    def books(self):
        return tuple(
            BibleBook(book, self.translation, self.api_key) for book in BIBLE_BOOKS
        )
