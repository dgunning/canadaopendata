import rich
import re

LANGUAGES = {
    'en': 'en',
    'english': 'en',
    'fr': 'fr',
    'french': 'fr',
    'francais': 'fr',
    'anglais': 'en'
}


def lang(language: str):
    if not language:
        return 'en'
    return LANGUAGES.get(language.lower(), 'en')


def first(iterable, default=None) -> object:
    "Return first item in iterable, or default."
    return next(iter(iterable), default)


def dirprint(obj: object):
    rich.print(obj.__class__.__name__)
    rich.print('--------------------')
    rich.print('\n'.join(sorted([a for a in dir(obj)
                                 if not a.startswith('_')])))


def generate_ngrams(s, n):
    # Convert to lowercases
    s = s.lower()

    # Replace all none alphanumeric characters with spaces
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)

    # Break sentence in the token, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


if __name__ == '__main__':
    s = """
        Natural-language processing (NLP) is an area of
        computer science and artificial intelligence
        concerned with the interactions between computers
        and human (natural) languages.
    """.strip()
    print(generate_ngrams(s, 2))