import urllib.request

try:
    import ujson as json
except ImportError:
    import json

API_ENDPOINT = "https://api.esv.org/v3/passage/text/"


def request_from_api(verse):
    url = f"{API_ENDPOINT}?q={verse._book_title}+{verse._chapter_number}:{verse.verse_number}&include-passage-references=false&include-verse-numbers=false&include-first-verse-numbers=false&include-footnotes=false&include-headings=false&include-selahs=false"
    request = urllib.request.Request(url)
    request.add_header("Authorization", f"Token {verse.api_key}")
    response = urllib.request.urlopen(request, timeout=10)
    return json.loads(response.read())


def get_verse_text(verse):
    data = request_from_api(verse)
    if data["query"] != verse.address:
        raise ValueError(
            f"{verse._book_title} chapter {verse._chapter_number} does not contain verse {verse.verse_number}."
        )
    return data["passages"][0]
