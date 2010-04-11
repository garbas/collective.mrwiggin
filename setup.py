from setuptools import setup, find_packages
import os

version = '0.1a1'

setup(name='collective.mrwiggin',
      version=version,
      description="Forget about viewlets, it's portlets time! Ah, yes - it's Mr Wiggin of Ironside and Malone.",
      long_description=open("README.txt").read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone portlets',
      author='Rok Garbas',
      author_email='rok2garbas.si',
      url='http://github.com/garbas/collective.mrwiggin',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.portlets',
          'plone.app.registry',
          'plone.app.jquerytools',
          'collective.monkeypatcher',
          'z3c.form==1.9',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
