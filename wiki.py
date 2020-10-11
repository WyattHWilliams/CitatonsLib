import wikipediaapi
import string


excluded_sections = ['References']


def make_printable(s):
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, s))


def check_wiki_exist(pg_name):
    wiki = wikipediaapi.Wikipedia(
        'en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    page = wiki.page(pg_name)
    return page.exists()


def fetch_wiki_data(pg_name):
    wiki = wikipediaapi.Wikipedia(
        'en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    page = wiki.page(pg_name)
    return page
