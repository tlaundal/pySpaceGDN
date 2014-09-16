:orphan:

Welcome to pySpaceGDN!
======================================

pySpaceGDN is a python package for using the SpaceGDN API. It is designed to be
easy to use, but at the same time be as powerful as SpaceGDN.

Have a look::

    >>> from pyspacegdn import SpaceGDN
    >>> # An instance of the SpaceGDN class is the entry point to pySpaceGDN
    ... gdn = SpaceGDN()
    >>> # We create a request that gets all available types of games, and fetch the result
    ... response = gdn.find().type('type').fetch()
    >>> # We check that the request was successful
    ... response.ok
    True
    >>> # We print the results:
    ... for type in response.data:
    ...     print('Type:', type['name'])
    ...
    Type: Unstable 1.7.x (Public Beta Test Pack)
    Type: Tech World
    Type: Agrarian Skies: Hardcore Quest
    Type: BloodNBones
    >>> # There are many more types, but I've cut them out here



Contents
~~~~~~~~~

.. toctree::
    :maxdepth: 3

    reference

Indices and tables
~~~~~~~~~~~~~~~~~~

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
