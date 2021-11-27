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
