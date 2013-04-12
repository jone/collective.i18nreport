from setuptools import setup, find_packages
import os


version = '1.2.1'

setup(
    name='collective.i18nreport',
    version=version,
    description="Internationalization coverage report",

    long_description=open('README.rst').read() + '\n' + \
        open(os.path.join('docs', 'HISTORY.txt')).read(),

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        ],

    keywords='i18n coverage',
    author='Jonas Baumann',
    author_email='jone@jone.ch',
    url='https://github.com/collective/collective.i18nreport',

    license='GPL2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'setuptools',
        'i18ndude',
        'plone.i18n',
        'mako',
        ],

    extras_require={
        'tests': [
            'unittest2',
            ]},

    entry_points = {
        'console_scripts' : [
            'i18nreport = collective.i18nreport:main',
            ],
        })
