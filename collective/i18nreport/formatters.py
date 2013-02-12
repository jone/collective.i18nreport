from mako.template import Template
from plone.i18n.locales.languages import LanguageAvailability
import json
import os


def json_formatter(data):
    return json.dumps(data, indent=4)


def html_formatter(data):
    # generate a table
    domains = tuple(sorted(data.keys()))
    headings = ['Language'] + list(domains)

    languages = LanguageAvailability().getLanguages(combined=True)
    lang_codes = set(reduce(lambda x, y: x + y, map(dict.keys, data.values())))

    rows = []
    for lang_code in lang_codes:
        row = [{'content': languages.get(lang_code, {}).get('name', lang_code),
                'classes': 'bold'}]

        for domain in domains:
            value = data.get(domain, {}).get(lang_code, None)

            if value:
                classes = ''

                if value <= 50:
                    classes = 'red'

                elif value <= 80:
                    classes = 'yellow'

                elif value <= 99:
                    classes = 'blue'

                else:
                    classes = 'green'

                row.append({'content': '%s%%' % value,
                            'classes': classes})
            else:
                row.append({'content': '-',
                            'classes': 'red'})

        rows.append(row)

    rows.sort(key=lambda item: item[0])

    template_path = os.path.join(os.path.dirname(__file__), 'template.html')
    return Template(filename=template_path).render(headings=headings,
                                                   rows=rows)
