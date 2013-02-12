from collective.i18nreport.utils import find_domains_in_path
from i18ndude.catalog import MessageCatalog
from plone.i18n.locales.languages import LanguageAvailability


def calculate_coverage_for_path(path, all_languages=False):
    """Calculates the translation coverage for each domain found in
    the given path.
    """

    result = {}

    for domain, item in find_domains_in_path(path).items():
        coverage = calculate_coverage_for_domain(
            all_languages=all_languages, **item)
        if not coverage:
            continue

        result[domain] = coverage

    return result


def calculate_coverage_for_domain(potfiles, languages, all_languages=False):
    """Returns a code to coverage (percentage) dict for
    the given potfiles / languages.
    """
    pot_catalog = catalog_of_files(potfiles)
    if not pot_catalog:
        return None

    total = len(pot_catalog.keys())

    if all_languages:
        coverage = dict(map(lambda lang: (lang, 0),
                            LanguageAvailability().getAvailableLanguages()))

    else:
        coverage = {}

    for lang, paths in languages.items():
        lang_catalog = catalog_of_files(paths)
        if not lang_catalog:
            continue

        translated = 0
        for msgid in pot_catalog.keys():
            if msgid in lang_catalog and lang_catalog[msgid].msgstr:
                if not [1 for fuzzy in lang_catalog[msgid].comments
                        if 'fuzzy' in fuzzy]:
                    translated += 1

        percentage = int(translated / (total * 1.0) * 100)
        if percentage == 99:
            percentage = 100
        coverage[lang] = percentage

    return coverage


def catalog_of_files(paths):
    """Returns a merged message catalog of all provided paths.
    """
    if not paths:
        raise ValueError()

    catalog = None

    for path in paths:
        try:
            if not catalog:
                catalog = MessageCatalog(filename=path)
            else:
                catalog.merge(MessageCatalog(filename=path))

        except AttributeError:
            # Skip file - not valid
            pass

    return catalog
