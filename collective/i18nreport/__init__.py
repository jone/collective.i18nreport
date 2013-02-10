from collective.i18nreport.coverage import calculate_coverage_for_path
import argh
import json
import os

formatters = {
    'json': json.dumps}


@argh.arg('--path', help='Path to scan for translations (defaults to pwd)')
@argh.arg('--format', help=', '.join(formatters.keys()))
def command(path=None, format='json'):
    if path is None:
        path = os.getcwd()

    formatter = formatters[format]
    return formatter(calculate_coverage_for_path(path))


def main():
    argh.dispatch_command(command)
