""" Setup.py for pySpaceGDN. """
from distutils.core import setup
import spacegdn

setup(
    name='pySpaceGDN',
    version=spacegdn.__version__,
    description='Python Module for the SpaceGDN JSON API',
    author=spacegdn.__author__,
    author_email='mail@totokaka.io',
    url='https://github.com/totokaka/pySpaceGDN',
    py_modules=['spacegdn'],
    classifiers=[
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)
