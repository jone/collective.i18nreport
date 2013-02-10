import os.path
import re
import shutil
import subprocess
import tempfile


def find_domains_in_path(path):
    domains = {}

    for potfile in find_files_in_path('pot', path):
        domain = get_domain_of_potfile(potfile)
        if domain not in domains:
            domains[domain] = {'potfiles': [],
                               'languages': {}}

        domains[domain]['potfiles'].append(potfile)
        get_pofiles_for_potfile(potfile, domains[domain]['languages'])

    return domains


def find_files_in_path(extension, directory):
    return map(os.path.normcase,
               map(os.path.abspath, check_output(
                'find %s -name "*.%s"' % (directory, extension)).splitlines()))


def get_domain_of_potfile(path):
    """Detect the domain of a potfile.

    Strategies:
    locales-directory: the basename of the file is the domain
    i18n-directory: the domain is specified within the file ("Domain: ..")
    """

    type_ = get_definition_type(path)

    if type_ == 'locales':
        domain, _ext = os.path.splitext(os.path.basename(path))

    elif type_ == 'i18n':
        domain_definitions = check_output(
            'grep -hr "\\"Domain: " %s' % path).splitlines()
        assert len(domain_definitions) == 1, \
            'Multiple or no domain definitions in %s' % path
        domain = domain_definitions[0]
        domain = re.match(r'".*?: ([^\\]+)\\n"', domain).groups()[0]

    return domain


def get_language_of_pofile(path):
    """Return the language of a po file.

    Strategies:
    locales-directory: the language-code is part of the path
    i18n-directory: the language is specified within the file
    ("Language-Code: ..")
    """

    type_ = get_definition_type(path)

    if type_ == 'locales':
        parts = path.split('/')
        language = parts[-3]

    elif type_ == 'i18n':
        language_definitions = check_output(
            'grep -hr "\\"Language-Code: " %s' % path).splitlines()
        assert len(language_definitions) == 1, \
            'Multiple or no language definitions in %s' % path
        language = language_definitions[0]
        language = re.match(r'".*?: ([^\\]+)\\n"', language).groups()[0]

    return language


def get_definition_type(path):
    """Returns the translation definition type for a .pot- or .po-file path.
    """

    if '/i18n/' in path:
        return 'i18n'

    elif '/locales/' in path:
        return 'locales'

    else:
        raise ValueError('File %s is neither in an "i18n" or '
                         'in a "locales" directory.' % path)


def get_pofiles_for_potfile(potfile, result):
    type_ = get_definition_type(potfile)
    directory = os.path.dirname(potfile)
    domain = get_domain_of_potfile(potfile)

    for pofile in find_files_in_path('po', directory):
        if type_ == 'i18n' and not os.path.basename(pofile).startswith(domain):
            continue

        elif type_ == 'locales' and \
                os.path.basename(pofile) != '%s.po' % domain:
            continue

        lang = get_language_of_pofile(pofile)
        if lang not in result:
            result[lang] = []

        result[lang].append(pofile)


def count_messages(path):
    """Counts the amount of messages in a po-file or pot-file.
    """

    msgids = len(check_output('grep -r "msgid" %s' % path).splitlines())

    # Subtract one msgid: the first msgid in each file is
    # the "template" definition.
    return msgids - 1


class create_tempdir():
    """Context manager for creating a temporary directory.
    The directory is deleted automatically when leaving the context managare.

    Example:

    >>> with create_tempdir() as path:
    ...     do_something(path)

    """

    def __init__(self):
        self.directory = None

    def __enter__(self):
        self.directory = tempfile.mkdtemp()
        return self.directory

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.directory, True)


def check_output(cmd):
    """Runs a command and returns the shell output.
    """

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    exitcode = proc.wait()

    if exitcode != 0:
        raise subprocess.CalledProcessError(exitcode, cmd)

    return proc.stdout.read()
