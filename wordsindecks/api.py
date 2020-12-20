import requests

URL = 'https://en.wiktionary.org/w/api.php'

def fetch(word: str) -> str:
    params = {
        "action" : "parse",
        "format" : "json",
        "prop" : "wikitext",
        "page" : word
    }

    json = requests.get(URL, params=params).json()

    if 'error' in json:
        raise ValueError('Article not found')

    return json['parse']['wikitext']['*']