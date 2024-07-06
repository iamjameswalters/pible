import re, urllib.request

try:
    import ujson as json
except ImportError:
    import json

API_ENDPOINT = "https://api.esv.org/v3/passage/text/"

def request_from_api(verse):
    url = f"{API_ENDPOINT}?q={verse._book_title}+{verse._chapter_number}:{verse._verse_number}&include-passage-references=false&include-verse-numbers=false&include-first-verse-numbers=false&include-footnotes=false&include-headings=false&include-selahs=false"
    request = urllib.request.Request(url)
    request.add_header("Authorization", f"Token {verse.api_key}")
    response = urllib.request.urlopen(request)
    if not 200 <= response.status < 300:
        raise HttpError(response.status)
    return response

def parse_response_data(response):
    data = json.loads(response.read())
    verse = data["passages"][0]
    pattern = "(.*?)\s\(ESV\)"
    match = re.search(pattern, verse)
    return match[1]


def get_verse_text(verse):
    api_response = request_from_api(verse)
    return parse_response_data(api_response)
