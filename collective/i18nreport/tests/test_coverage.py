from collective.i18nreport import coverage
from collective.i18nreport.tests.helpers import make_absolute
from unittest2 import TestCase
import os


TEST_EXAMPLE_PATH = os.path.join(os.path.dirname(__file__), 'example')


class TestCalculateCoverForPath(TestCase):

    def test(self):
        self.assertEqual(coverage.calculate_coverage_for_path(TEST_EXAMPLE_PATH),
                         {'plone': {'nl': 93}, 'linguaplone': {'nl': 100}})


class TestCalculateCoverageForDomain(TestCase):

    def test_one_language(self):
        potfiles = [make_absolute('foo/i18n/plone.pot')]
        pofiles = {'nl': [make_absolute('foo/i18n/plone-nl.po')]}
        self.assertEquals(coverage.calculate_coverage_for_domain(potfiles, pofiles),
                          {'nl': 92})

    def test_all_languages(self):
        self.maxDiff = None
        potfiles = [make_absolute('foo/i18n/plone.pot')]
        pofiles = {'nl': [make_absolute('foo/i18n/plone-nl.po')]}

        expected = {u'nl': 92,
                    u'aa': 0, u'ab': 0, u'ae': 0, u'af': 0, u'ak': 0, u'am': 0, u'an': 0, u'ar': 0,
                    u'as': 0, u'ay': 0, u'az': 0, u'ba': 0, u'be': 0, u'bg': 0, u'bh': 0, u'bi': 0,
                    u'bm': 0, u'bn': 0, u'bo': 0, u'br': 0, u'bs': 0, u'ca': 0, u'ce': 0, u'ch': 0,
                    u'co': 0, u'cr': 0, u'cs': 0, u'cu': 0, u'cv': 0, u'cy': 0, u'da': 0, u'de': 0,
                    u'dv': 0, u'dz': 0, u'ee': 0, u'el': 0, u'en': 0, u'eo': 0, u'es': 0, u'et': 0,
                    u'eu': 0, u'fa': 0, u'ff': 0, u'fi': 0, u'fj': 0, u'fo': 0, u'fr': 0, u'fy': 0,
                    u'ga': 0, u'gd': 0, u'gl': 0, u'gn': 0, u'gu': 0, u'gv': 0, u'ha': 0, u'he': 0,
                    u'hi': 0, u'ho': 0, u'hr': 0, u'ht': 0, u'hu': 0, u'hy': 0, u'hz': 0, u'ia': 0,
                    u'id': 0, u'ie': 0, u'ig': 0, u'ii': 0, u'ik': 0, u'io': 0, u'is': 0, u'it': 0,
                    u'iu': 0, u'ja': 0, u'jv': 0, u'ka': 0, u'kg': 0, u'ki': 0, u'kj': 0, u'kk': 0,
                    u'kl': 0, u'km': 0, u'kn': 0, u'ko': 0, u'kr': 0, u'ks': 0, u'ku': 0, u'kv': 0,
                    u'kw': 0, u'ky': 0, u'la': 0, u'lb': 0, u'lg': 0, u'li': 0, u'ln': 0, u'lo': 0,
                    u'lt': 0, u'lu': 0, u'lv': 0, u'mg': 0, u'mh': 0, u'mi': 0, u'mk': 0, u'ml': 0,
                    u'mn': 0, u'mo': 0, u'mr': 0, u'ms': 0, u'mt': 0, u'my': 0, u'na': 0, u'nb': 0,
                    u'nd': 0, u'ne': 0, u'ng': 0, u'nn': 0, u'no': 0, u'nr': 0, u'nv': 0,
                    u'ny': 0, u'oc': 0, u'oj': 0, u'om': 0, u'or': 0, u'os': 0, u'pa': 0, u'pi': 0,
                    u'pl': 0, u'ps': 0, u'pt': 0, u'qu': 0, u'rm': 0, u'rn': 0, u'ro': 0, u'ru': 0,
                    u'rw': 0, u'sa': 0, u'sc': 0, u'sd': 0, u'se': 0, u'sg': 0, u'sh': 0, u'si': 0,
                    u'sk': 0, u'sl': 0, u'sm': 0, u'sn': 0, u'so': 0, u'sq': 0, u'sr': 0, u'ss': 0,
                    u'st': 0, u'su': 0, u'sv': 0, u'sw': 0, u'ta': 0, u'te': 0, u'tg': 0, u'th': 0,
                    u'ti': 0, u'tk': 0, u'tl': 0, u'tn': 0, u'to': 0, u'tr': 0, u'ts': 0, u'tt': 0,
                    u'tw': 0, u'ty': 0, u'ug': 0, u'uk': 0, u'ur': 0, u'uz': 0, u've': 0, u'vi': 0,
                    u'vk': 0, u'vo': 0, u'wa': 0, u'wo': 0, u'xh': 0, u'yi': 0, u'yo': 0, u'za': 0,
                    u'zh': 0, u'zu': 0}

        self.assertEquals(
            coverage.calculate_coverage_for_domain(potfiles, pofiles, all_languages=True),
            expected)
