import requests

URL = 'https://en.wiktionary.org/w/api.php'

def fetch(word: str) -> str:
    """Fetch the wikitext for an article on wiktionary.org

    :param word: Word to fetch
    :type word: str
    :raises ValueError: If the article does not exist
    :return: Wikitext for the requested word
    :rtype: str
    """
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