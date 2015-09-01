from setuptools import setup, find_packages
import os

version = '0.1.0'

setup(name='rer.consentembed',
      version=version,
      description="Extends collective.portlet.embed preventing the load of resource from external sites",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        ],
      keywords='plone plonegov embed opt-out cookie',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='https://github.com/PloneGov-IT/rer.consentembed',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rer'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.portlet.embed',
          'pyquery>=1.2.3',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
