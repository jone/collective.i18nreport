from collective.i18nreport import utils
from collective.i18nreport.tests.helpers import make_absolute
from collective.i18nreport.tests.helpers import make_relative_recursively
from unittest2 import TestCase
import os
import subprocess


TEST_EXAMPLE_PATH = os.path.join(os.path.dirname(__file__), 'example')


class TestUtils(TestCase):

    def test_find_domains_in_path(self):
        self.maxDiff = None
        self.assertEqual(
            make_relative_recursively(utils.find_domains_in_path(TEST_EXAMPLE_PATH)),

            {'plone': {
                    'potfiles': ['foo/i18n/plone.pot',
                                 'foo/locales/locales/plone.pot'],
                    'languages': {
                        'nl': ['foo/i18n/plone-nl.po',
                               'foo/locales/locales/nl/LC_MESSAGES/plone.po']}},

             'linguaplone': {
                    'potfiles': ['foo/locales/locales/linguaplone.pot'],
                    'languages': {
                        'nl': ['foo/locales/locales/nl/LC_MESSAGES/linguaplone.po']}},

             })

    def test_find_files_in_path(self):
        results = make_relative_recursively(utils.find_files_in_path('pot', TEST_EXAMPLE_PATH))

        self.assertEquals(results, ['foo/i18n/plone.pot',
                                    'foo/locales/locales/linguaplone.pot',
                                    'foo/locales/locales/plone.pot'])

    def test_get_domain_of_potfile(self):
        self.assertEqual(
            utils.get_domain_of_potfile(make_absolute('foo/i18n/plone.pot')),
            'plone')

        self.assertEqual(
            utils.get_domain_of_potfile(make_absolute('foo/locales/locales/linguaplone.pot')),
            'linguaplone')

        self.assertEqual(
            utils.get_domain_of_potfile(make_absolute('foo/locales/locales/plone.pot')),
            'plone')

    def test_get_language_of_pofile(self):
        self.assertEqual(utils.get_language_of_pofile(
                make_absolute('foo/locales/locales/nl/LC_MESSAGES/linguaplone.po')),
                'nl')

        self.assertEqual(utils.get_language_of_pofile(
                    make_absolute('foo/locales/locales/nl/LC_MESSAGES/plone.po')),
                    'nl')

        self.assertEqual(utils.get_language_of_pofile(make_absolute('foo/i18n/plone-nl.po')),
                         'nl')

    def test_get_definition_type(self):
        self.assertEqual(utils.get_definition_type('foo/i18n/plone.pot'), 'i18n')
        self.assertEqual(utils.get_definition_type('foo/locales/locales/plone.pot'), 'locales')

        with self.assertRaises(ValueError):
            utils.get_definition_type('foo')

    def test_get_pofiles_for_potfile__i18n(self):
        result = {}
        utils.get_pofiles_for_potfile(make_absolute('foo/i18n/plone.pot'), result)
        result = make_relative_recursively(result)

        self.assertEqual(result, {'nl': ['foo/i18n/plone-nl.po']})

    def test_get_pofiles_for_potfile__locales(self):
        result = {}
        utils.get_pofiles_for_potfile(make_absolute('foo/locales/locales/plone.pot'), result)
        result = make_relative_recursively(result)

        self.assertEqual(result, {'nl': ['foo/locales/locales/nl/LC_MESSAGES/plone.po']})

    def test_get_pofiles_for_potfile__extends(self):
        result = {'nl': ['something.po']}
        utils.get_pofiles_for_potfile(make_absolute('foo/locales/locales/plone.pot'), result)
        result = make_relative_recursively(result)

        self.assertEqual(result, {'nl': ['foo/locales/locales/nl/LC_MESSAGES/plone.po',
                                         'something.po']})

    def test_count_msgids(self):
        self.assertEqual(
            utils.count_messages(make_absolute('foo/locales/locales/linguaplone.pot')),
            3)

        self.assertEqual(
            utils.count_messages(make_absolute('foo/locales/locales/plone.pot')),
            4)

        self.assertEqual(
            utils.count_messages(make_absolute('foo/i18n/plone.pot')),
            25)

    def test_tempdir_context_manager__success(self):
        with utils.create_tempdir() as path:
            self.assertTrue(os.path.exists(path))
            os.mkdir(os.path.join(path, 'foo'))

        self.assertFalse(os.path.exists(path))

    def test_tempdir_context_manager__failure(self):
        with self.assertRaises(ValueError):
            with utils.create_tempdir() as path:
                raise ValueError()

        self.assertFalse(os.path.exists(path))

    def test_check_output__returns_output(self):
        self.assertEqual(utils.check_output('echo "foo\nbar"'), 'foo\nbar\n')

    def test_check_output__raises_on_failure(self):
        with self.assertRaises(subprocess.CalledProcessError) as cm:
            utils.check_output('exit 1')

        self.assertEqual(str(cm.exception),
                         "Command 'exit 1' returned non-zero exit status 1")
