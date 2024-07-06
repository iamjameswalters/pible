from pathlib import Path

try:
    import ujson as json
except ImportError:
    import json


def get_verse_text(verse):
    json_file = (
        Path(__file__).parent / f"kjv_json/{verse._book_title.replace(' ', '')}.json"
    )
    with open(json_file, mode="r", encoding="utf8") as file:
        data = json.loads(file.read())
    chapter = data[str(verse._chapter_number)]
    try:
        verse_text = chapter[str(verse.verse_number)]
    except KeyError:
        raise ValueError(
            f"{verse._book_title} chapter {verse._chapter_number} does not contain verse {verse.verse_number}."
        )
    return verse_text
