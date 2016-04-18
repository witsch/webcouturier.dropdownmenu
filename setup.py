# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '3.0.0.dev0'

setup(name='webcouturier.dropdownmenu',
      version=version,
      description="Dropdown menus for global navigation in Plone",
      long_description=(open("README.rst").read() + '\n' +
                        open("docs/INSTALL.txt").read() + '\n' +
                        open('CHANGES.rst').read()),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Plone :: 4.3',
          'Framework :: Plone :: 5.0',
          'Framework :: Plone',
          "License :: OSI Approved :: GNU General Public License (GPL)",
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='web couturier dropdown menu navigation',
      author='Denys Mishunov',
      author_email='denys.mishunov@gmail.com',
      url='http://plone.org/products/webcouturier-dropdownmenu',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['webcouturier'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'AccessControl',
          'Acquisition',
          'plone.app.controlpanel',
          'plone.app.layout',
          'plone.app.portlets',
          'plone.browserlayer',
          'plone.memoize',
          'plone.theme',
          'Products.CMFCore',
          'Products.CMFPlone',
          'Products.GenericSetup',
          'setuptools',
          'zope.component',
          'zope.formlib',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'plone.testing',
              'transaction',
              'unittest2',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
