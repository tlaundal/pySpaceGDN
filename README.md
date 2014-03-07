## What is pySpaceGDN?

pySpaceGDN is a client-side module for interfacing with the SpaceGDN API over Python.

## How do I install this?

pySpaceGDN is available via pip and easy_install.  You can also manually install pySpaceGDN by simply downloading the code here and installing it using the `setup.py` file.

#### Examples:

__Using pip:__

`pip install pyspacegdn`

__Using Easy_Install:__

`easy_install pyspacegdn`

__Manually:__

After you have cloned this repo:

`python setup.py install`

## How do I use the API?

    import spacegdn
    help(spacegdn)

Overloadable variables:

* spacegdn.USER_AGENT - This should be set to whatever your application is.  By default, it will report as pySpaceGDN 1.0.
* spacegdn.BASE - This is the base URL to SpaceGDN used by pySpaceGDN. Currently you have to set this to "http://spacegdn.totokaka.io/v1/" for spacegdn to work. This is because the official host is 
currently down.
* spacegdn.DEBUG - Whether debug output should be printed, this is only useful for developer.
