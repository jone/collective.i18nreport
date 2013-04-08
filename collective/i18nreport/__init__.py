from collective.i18nreport import formatters
from collective.i18nreport.coverage import calculate_coverage_for_path
from optparse import OptionParser
import os
import sys


FORMATTERS = {
    'json': formatters.json_formatter,
    'html': formatters.html_formatter}


def command(path=None, format='json', all_languages=False):
    if path is None:
        path = os.getcwd()

    coverage = calculate_coverage_for_path(path, all_languages=all_languages)

    formatter = FORMATTERS[format]
    return formatter(coverage)


def parse_arguments(argv):
    usage = 'i18nreport [-h] [--path PATH] [--format FORMAT]' + \
        ' [--all-languages]'

    parser = OptionParser(usage=usage)

    parser.add_option(
        '-p', '--path', dest='path',
        help='Path to scan for translations (defaults to pwd)')

    parser.add_option(
        '-f', '--format', dest='format',
        type='choice',
        help='Formats: %s' % ', '.join(FORMATTERS.keys()),
        choices=FORMATTERS.keys())

    parser.add_option(
        '-a', '--all-languages',
        help='Show also languages wich are not translated at all',
        action='store_true')

    options, args = parser.parse_args(argv)
    if len(args) != 0:
        parser.print_help()
        sys.exit(1)

    # make a dict of options which are not None
    options = dict([(key, value) for (key, value) in vars(options).items()
                    if value is not None])

    return options


def main():
    print command(**parse_arguments(sys.argv[1:]))
    return 0
