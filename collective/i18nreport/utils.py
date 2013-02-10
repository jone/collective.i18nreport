import os.path
import re
import shutil
import subprocess
import tempfile


def find_domains_in_path(path):
    potfiles = {}

    for potfile in find_files_in_path('pot', path):
        potfiles[potfile] = {'domain': get_domain_of_potfile(potfile),
                             'languages': get_pofiles_for_potfile(potfile),
                             'messages': count_messages(potfile)}

    return potfiles


def find_files_in_path(extension, directory):
    return map(os.path.normcase,
               map(os.path.abspath,
                   subprocess.check_output('find %s -name "*.%s"' % (directory, extension),
                                           shell=True).splitlines()))


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
        domain_definitions = subprocess.check_output(
            'grep -hr "\\"Domain: " %s' % path, shell=True).splitlines()
        assert len(domain_definitions) == 1, 'Multiple or no domain definitions in %s' % path
        domain = domain_definitions[0]
        domain = re.match(r'".*?: ([^\\]+)\\n"', domain).groups()[0]

    return domain


def get_language_of_pofile(path):
    """Return the language of a po file.

    Strategies:
    locales-directory: the language-code is part of the path
    i18n-directory: the language is specified within the file ("Language-Code: ..")
    """

    type_ = get_definition_type(path)

    if type_ == 'locales':
        parts = list(reversed(path.split('/')))
        language = parts[parts.index('locales') - 1]

    elif type_ == 'i18n':
        language_definitions = subprocess.check_output(
            'grep -hr "\\"Language-Code: " %s' % path, shell=True).splitlines()
        assert len(language_definitions) == 1, 'Multiple or no language definitions in %s' % path
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
        raise ValueError(
            'File %s is neither in an "i18n" or in a "locales" directory.' % path)


def get_pofiles_for_potfile(potfile):
    type_ = get_definition_type(potfile)
    directory = os.path.dirname(potfile)
    domain = get_domain_of_potfile(potfile)

    languages = {}

    if type_ == 'i18n':
        for pofile in find_files_in_path('po', directory):
            if not os.path.basename(pofile).startswith(domain):
                continue

            languages[get_language_of_pofile(pofile)] = pofile

    elif type_ == 'locales':
        for pofile in find_files_in_path('po', directory):
            if os.path.basename(pofile) != '%s.po' % domain:
                continue

            languages[get_language_of_pofile(pofile)] = pofile

    return languages


def count_messages(path):
    """Counts the amount of messages in a po-file or pot-file.
    """

    msgids = len(subprocess.check_output('grep -r "msgid" %s' % path, shell=True).splitlines())

    # Subtract one msgid: the first msgid in each file is the "template" definition.
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
