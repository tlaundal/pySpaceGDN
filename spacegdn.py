""" API module for pySpaceGDN.

This is a really light wrapper around the API.
It only loads the json to python objects.

All public functions will return a list of results if the query was
successfull, or a dictionary with the error if it failed. The module is written
for both Python 2.7.x and Python 3.x, the only thing to keep in mind is that
the strings in the results will always be utf-8.

All functions may raise HTTPErrors.

Most functions should be self explainable, but this should probably be read
first: https://github.com/connor4312/SpaceGDN
Notably is searching which is done from the regular methods, for example:
    spacegdn.jars(where=something)

"""

import json
try:
    from urllib2 import urlopen, Request, HTTPError
except ImportError:
    from urllib.error import HTTPError
    from urllib.request import urlopen, Request

__author__ = 'totokaka'
__version__ = '1.0'

USER_AGENT = 'pySpaceGDN 0.1'
BASE = 'http://gdn.api.xereo.net/v1/'
DEBUG = False


def __request(url, query=None):
    """ Base Request.

    The parent function that all public functions call in order to initiate
    communication to the API.  Simply converts the Pythonic values into the
    the URL format expected by the API.  Also will add the User-Agent defined
    by the USER_AGENT variable.

    This takes three arguments:
        url    The URL to fetch. For example 'jar'
        page   The page number to fetch. Defaults to 1
        query  Queries. Notably here is where and sort.

    This will raise an HTTPError if we get an HTTPError from SpaceGDN that
    does not have code 400.

    """
    if query is None:
        query = {}
    query = '?' + '&'.join([str(key) + '=' + str(value) for key, value
                            in query.items()])

    url += query

    _debug('requesting url {}', repr(BASE+url))

    headers = {}
    headers['User-Agent'] = USER_AGENT
    headers['Accept'] = 'application/json'

    try:
        response = urlopen(Request(BASE + url, headers=headers)).read()
    except HTTPError as err:
        _debug('HTTPError')
        if err.code == 400 or err.code == 492:
            return json.loads(
                '\n'.join([line.decode("utf-8") for line in err.readlines()]))
        else:
            raise err
    else:
        _debug('SUCCESS')
        return json.loads(response.decode("utf-8"))


def _request(url, **query):
    """ Base Request which fetches all pages.

    This is a wrapper around __request which fetches all pages, and extracts
    only the result or the error. This means that it does not contain the info
    about how many pages was in the result, if it was successfull, etc.

    This function takes one argument:
        url    The URL to fetch

    This function returns a list of results if the request was successfull, but
    if the request was unsuccessfull it will return a dict of the error.

    """
    results = []
    page = 1
    while True:
        query['page'] = page
        response = __request(url, query)
        if response is None or not response['success']:
            return response['error']
        results += response['results']
        if not response['pages']['has_next']:
            break
        page += 1
    return results


def _debug(message, *args):
    """ Debug output. """
    if DEBUG:
        print(message.format(*args))


def jars(jar=None, **query):
    """ Jars.

    List jars. All available or just one.

    This takes one argument:
        jar    The id of a jar to get info about

    This function returns a list of results if the request was successfull, but
    if the request was unsuccessfull it will return a dict of the error.

    """
    url = 'jar'
    if not jar is None:
        url += '/' + str(jar)
    return _request(url, **query)


def channels(jar=None, channel=None, **query):
    """ Channels.

    List channels. All available, for a specific jar or just one.

    This takes two arguments:
        jar        The jar to get channels for
        channel    The channel to get info about

    This function returns a list of results if the request was successfull, but
    if the request was unsuccessfull it will return a dict of the error.

    """
    url = ''
    if jar is not None:
        url = 'jar/' + str(jar) + '/'
    url += 'channel'
    if channel is not None:
        url += '/' + str(channel)
    return _request(url, **query)


def versions(jar=None, channel=None, version=None, **query):
    """ Versions.

    List versions. All available, for a specific jar, for a specific channel
    or just one.

    This takes three arguments:
        jar        The jar to get versions for
        channel    The channel to get versions for
        version    The version to get info about

    This function returns a list of results if the request was successfull, but
    if the request was unsuccessfull it will return a dict of the error.

    """
    url = ''
    if jar is not None:
        url = 'jar/' + str(jar) + '/'
    if channel is not None:
        url += 'channel/' + str(channel) + '/'
    url += 'version'
    if version is not None:
        url += '/' + str(version)
    return _request(url, **query)


def builds(jar=None, channel=None, version=None, build=None, **query):
    """ Builds.

    List builds. All available, for a specific jar, for a specific channel,
    for a specific version or just one.

    This takes three arguments:
        jar        The jar to get builds for
        channel    The channel to get builds for
        version    The version to get builds for
        build      The build to get info about

    This function returns a list of results if the request was successfull, but
    if the request was unsuccessfull it will return a dict of the error.

    """
    url = ''
    if jar is not None:
        url = 'jar/' + str(jar) + '/'
    if channel is not None:
        url += 'channel/' + str(channel) + '/'
    if version is not None:
        url += 'version/' + str(version) + '/'
    url += 'build'
    if build is not None:
        url += '/' + str(build)
    return _request(url, **query)


def _get_id(result):
    """ Undocumented internal function. """
    if not type(result) is list:
        return result['code']
    elif len(result) <= 0:
        return -1
    else:
        return result[0]['id']


def get_id(jar=None, channel=None, version=None, build=None):
    """ Get the ID for jar, channel, version or build.

    This function will fetch the ID for the `highest` argument specified. This
    means that if jar, version and build are specified the id of the build will
    be returned. You should specify as many of the `lower` arguments as you
    can, so you get the correct result. More specific fetching will also be
    faster. On all arguments except `build` you can supply an integer, and that
    integer will be considered the id.

    Arguments:
        jar        The name of the jar
        channel    The name of the channel
        version    The name of the version
        build      The number of the build, must be integer

    Returns an integer with the id. The returned value will be zero if the
    object was not found, and the negative value of the error code if something
    went wrong.

    """
    return_value = 0
    if jar is not None and type(jar) is not int:
        jar = _get_id(jars(where='jar.name.eq.'+jar))
        if jar <= 0:
            return jar
        else:
            return_value = jar
    if channel is not None and type(channel) is not int:
        channel = _get_id(channels(jar=jar, where='channel.name.eq.'+channel))
        if channel <= 0:
            return -1
        else:
            return_value = channel
    if version is not None and type(version) is not int:
        version = _get_id(versions(jar=jar, channel=channel,
                                   where='version.version.eq.' + version))
        if version <= 0:
            return -1
        else:
            return_value = version
    if build is not None:
        build = _get_id(builds(jar=jar, channel=channel, version=version,
                               where='build.build.eq.' + str(build)))
        if build <= 0:
            return -1
        else:
            return_value = build

    return return_value
