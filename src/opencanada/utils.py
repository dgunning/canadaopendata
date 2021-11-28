import rich

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
