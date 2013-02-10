from collective.i18nreport import coverage
from collective.i18nreport.tests.helpers import make_absolute
from unittest2 import TestCase
import os


TEST_EXAMPLE_PATH = os.path.join(os.path.dirname(__file__), 'example')


class TestCalculateCoverageForDomain(TestCase):

    def test_example(self):
        potfiles = [make_absolute('foo/i18n/plone.pot')]
        pofiles = {'nl': [make_absolute('foo/i18n/plone-nl.po')]}
        self.assertEquals(coverage.calculate_coverage_for_domain(potfiles, pofiles),
                          {'nl': 92})
