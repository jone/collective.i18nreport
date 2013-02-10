from collective.i18nreport.coverage import calculate_coverage_for_path
import argh
import json
import os

formatters = {
    'json': lambda data: json.dumps(data, indent=4)}


@argh.arg('--path', '-p', help='Path to scan for translations (defaults to pwd)')
@argh.arg('--format', '-f', help=', '.join(formatters.keys()))
@argh.arg('--all-languages', '-a', help='Show also languages wich are not translated at all')
def command(path=None, format='json', all_languages=False):
    if path is None:
        path = os.getcwd()

    coverage = calculate_coverage_for_path(path, all_languages=all_languages)

    formatter = formatters[format]
    return formatter(coverage)


def main():
    argh.dispatch_command(command)
