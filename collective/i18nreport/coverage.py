from i18ndude.catalog import MessageCatalog


def coverage(path):
    """Calculates the translation coverage for each domain found in the given path.
    """


def calculate_coverage_for_domain(potfiles, languages):
    pot_catalog = catalog_of_files(potfiles)
    total = len(pot_catalog.keys())

    coverage = {}

    for lang, paths in languages.items():
        lang_catalog = catalog_of_files(paths)

        translated = 0
        for msgid in pot_catalog.keys():
            if msgid in lang_catalog and lang_catalog[msgid].msgstr:
                if not [1 for fuzzy in lang_catalog[msgid].comments if 'fuzzy' in fuzzy]:
                    translated += 1

        percentage = int(translated / (total * 1.0) * 100)
        if percentage == 99:
            percentage = 100
        coverage[lang] = percentage

    return coverage


def catalog_of_files(paths):
    if not paths:
        raise ValueError()

    catalog = None

    for path in paths:
        if not catalog:
            catalog = MessageCatalog(filename=path)
        else:
            catalog.merge(MessageCatalog(filename=path))

    return catalog
