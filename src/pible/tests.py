import pible
from unittest import TestCase


class PibleTests(TestCase):
    def test_bible_obj(self):
        bible = pible.Bible()
        self.assertEqual(repr(bible), "<pible Bible class>")

    def test_bible_book_obj(self):
        bible = pible.Bible()
        john = bible["John"]
        self.assertEqual(repr(john), "BibleBook<John>")
        with self.assertRaises(ValueError):
            joe = bible["Joe"]

    def test_bible_chapter_obj(self):
        bible = pible.Bible()
        john = bible["John"]
        john_3 = john[3]
        self.assertEqual(repr(john_3), "BibleChapter<John 3>")
        with self.assertRaises(IndexError):
            john_99 = john[99]

    def test_bible_verse_obj(self):
        bible = pible.Bible()
        john = bible["John"]
        john_3_16 = john[3][16]
        self.assertEqual(repr(john_3_16), "BibleVerse<John 3:16>")
        self.assertEqual(
            str(john_3_16),
            "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
        )
        with self.assertRaises(IndexError):
            not_a_verse = john[3][99]
