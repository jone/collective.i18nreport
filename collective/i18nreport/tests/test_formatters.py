from unittest2 import TestCase
from collective.i18nreport import formatters


class TestJSONFormatter(TestCase):

    def test_json_formatting(self):
        input = {
            "plone.app.ldap": {
                "ja": 100
                }}

        expected = '''{
    "plone.app.ldap": {
        "ja": 100
    }
}
'''.strip()

        output = formatters.json_formatter(input).strip()
        self.assertEquals(output, expected,
                          '\n\nOUTPUT:\n"""%s"""\n\nEXPECTED:\n"""%s"""' % (output, expected))
