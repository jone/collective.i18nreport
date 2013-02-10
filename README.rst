=======================
 collective.i18nreport
=======================

Creates a coverage report of translations.


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

    $ git clone https://github.com/jone/collective.i18nreport.git
    $ ln -s development.cfg buildout.cfg
    $ python2.7 bootstrap.py
    $ bin/buildout
    $ bin/i18nreport


::

    usage: i18nreport [-h] [--path PATH] [--format FORMAT] [--all-languages]

    optional arguments:
      -h, --help            show this help message and exit
      --path PATH, -p PATH  Path to scan for translations (defaults to pwd)
      --format FORMAT, -f FORMAT
                            json, html
      --all-languages, -a   Show also languages wich are not translated at all
