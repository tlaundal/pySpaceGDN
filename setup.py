""" Setup.py for pySpaceGDN. """

from setuptools import setup

setup(
    name='pySpaceGDN',
    version='2.0.0-dev',
    description='Python Module for the SpaceGDN JSON API',
    author='Tobias Laundal',
    author_email='mail+pyspacegdn@totokaka.io',
    url='https://github.com/totokaka/pySpaceGDN',
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
    ]
)
