=======================
 collective.i18nreport
=======================

Creates a coverage report of internationalizations.


Usage
=====

Install it using buildout:

.. code:: ini

    [buildout]
    parts =
        report

    [report]
    recipe = zc.recipe.egg
    eggs = collective.i18nreport

Or you can checkout the repository and use it from source:

.. code:: shell

    $ git clone https://github.com/collective/collective.i18nreport.git
    $ ln -s development.cfg buildout.cfg
    $ python2.7 bootstrap.py
    $ bin/buildout
    $ bin/i18nreport --help
    Usage: i18nreport [-h] [--path PATH] [--format FORMAT] [--all-languages]

    Options:
      -h, --help            show this help message and exit
      -p PATH, --path=PATH  Path to scan for translations (defaults to pwd)
      -f FORMAT, --format=FORMAT
                            Formats: json, html
      -a, --all-languages   Show also languages wich are not translated at all


Links
-----

- Main github project repository: https://github.com/collective/collective.i18nreport
- Issue tracker: https://github.com/collective/collective.i18nreport/issues
- Package on pypi: http://pypi.python.org/pypi/collective.i18nreport
- Continuous integration: https://jenkins.4teamwork.ch/search?q=collective.i18nreport
