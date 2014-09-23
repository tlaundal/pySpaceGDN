""" Setup.py for pySpaceGDN. """

from os import path
from setuptools import setup


def get_long_description():
    """ Read the long description. """
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.rst')) as readme:
        return readme.read()
    return None

setup(
    name='pySpaceGDN',
    version='2.0.1',
    description='Python Module for the SpaceGDN JSON API',
    long_description=get_long_description(),
    author='Tobias Laundal',
    author_email='mail+pyspacegdn@totokaka.io',
    url='https://github.com/totokaka/pySpaceGDN',
    license='MIT',
    packages=['pyspacegdn', 'pyspacegdn.requests'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='SpaceGDN pySpaceGDN SpaceCP GDN'
)
