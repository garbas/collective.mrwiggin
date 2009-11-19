from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.mrwiggin',
      version=version,
      description="Ah, yes - it's Mr Wiggin of Ironside and Malone.",
      long_description=open("README.txt").read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone portlets',
      author='Rok Garbas',
      author_email='rok2garbas.si',
      url='http://svn.plone.org/svn/collective/collective.mrwiggin',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
