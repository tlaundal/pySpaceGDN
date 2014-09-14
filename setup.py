""" Setup.py for pySpaceGDN. """

from distutils.core import setup
import pyspacegdn

setup(
    name=pyspacegdn.name,
    version=pyspacegdn.version,
    description='Python Module for the SpaceGDN JSON API',
    author='totokaka',
    author_email='mail+pyspacegdn@totokaka.io',
    url='https://github.com/totokaka/pySpaceGDN',
    packages=['pyspacegdn', 'pyspacegdn.requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)
