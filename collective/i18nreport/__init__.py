from collective.i18nreport import formatters
from collective.i18nreport.coverage import calculate_coverage_for_path
import argh
import os


FORMATTERS = {
    'json': formatters.json_formatter,
    'html': formatters.html_formatter}


@argh.arg('--path', '-p', help='Path to scan for translations (defaults to pwd)')
@argh.arg('--format', '-f', help=', '.join(FORMATTERS.keys()))
@argh.arg('--all-languages', '-a', help='Show also languages wich are not translated at all')
def command(path=None, format='json', all_languages=False):
    if path is None:
        path = os.getcwd()

    coverage = calculate_coverage_for_path(path, all_languages=all_languages)

    formatter = FORMATTERS[format]
    return formatter(coverage)


def main():
    argh.dispatch_command(command)
