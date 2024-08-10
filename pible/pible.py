from .translations import esv, kjv

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
                f"{translation} is not a supported translation. Must be one of: {BIBLE_TRANSLATIONS}"
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
        self.verse_number = verse
        if self.translation == "ESV" and not api_key:
            raise ValueError("Using ESV requires an API key from api.esv.org")
        self.api_key = api_key
        self.text = self._get_text()

    @property
    def book(self):
        return BibleBook(self._book_title, self.translation, self.api_key)

    @property
    def chapter(self):
        return BibleChapter(
            self._book_title, self._chapter_number, self.translation, self.api_key
        )

    @property
    def address(self):
        return f"{self._book_title} {self._chapter_number}:{self.verse_number}"

    def __repr__(self):
        return (
            f"BibleVerse<{self._book_title} {self._chapter_number}:{self.verse_number}>"
        )

    def _get_text(self):
        match self.translation:
            case "KJV":
                return kjv.get_verse_text(self)
            case "ESV":
                return esv.get_verse_text(self)

    def __str__(self):
        if self.text == "":
            self.text = self._get_text()
        return self.text

    def __eq__(self, other):
        if not isinstance(other, BibleVerse):
            return False
        return (
            self.__repr__() == other.__repr__()
            and self.translation == other.translation
        )

    def next_verse(self):
        try:
            next_verse = BibleVerse(
                self._book_title,
                self._chapter_number,
                self.verse_number + 1,
                self.translation,
                self.api_key,
            )
        except ValueError:
            if (self._chapter_number + 1) <= BIBLE_CHAPTERS[self._book_title]:
                next_verse = BibleVerse(
                    self._book_title,
                    self._chapter_number + 1,
                    1,
                    self.translation,
                    self.api_key,
                )
            else:
                next_verse = None
        return next_verse


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
        if self.translation == "ESV" and not api_key:
            raise ValueError("Using ESV requires an API key from api.esv.org")
        self.api_key = api_key

    @property
    def book(self):
        return BibleBook(self._book_title, self.translation, self.api_key)

    @property
    def verses(self):
        verses = []
        verse_num = 1
        while True:
            try:
                current_verse = BibleVerse(
                    self._book_title,
                    self._chapter_number,
                    verse_num,
                    self.translation,
                    self.api_key,
                )
            # when we reach an invalid verse past the end of the chapter, break
            except ValueError:
                break
            verses.append(current_verse)
            verse_num += 1
        return tuple(verses)

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

    def __str__(self):
        return str(self._chapter_number)


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
        if self.translation == "ESV" and not api_key:
            raise ValueError("Using ESV requires an API key from api.esv.org")
        self.api_key = api_key

    def __repr__(self):
        return f"BibleBook<{self._title}>"

    def __str__(self):
        return self._title

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
        if self.translation == "ESV" and not api_key:
            raise ValueError("Using ESV requires an API key from api.esv.org")
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
