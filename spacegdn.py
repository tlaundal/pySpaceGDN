""" API module for pySpaceGDN.

This is a really light wrapper around the API.
It only loads the json to python objects.

All public functions will return a list of results if the query was
successfull, or a dictionary with the error if it failed. The module is written
for both Python 2.7.x and Python 3.x, the only thing to keep in mind is that
the strings in the results will always be utf-8.

"""

import json
try:
    from urllib2 import urlopen, Request, HTTPError
except ImportError:
    from urllib.error import HTTPError
    from urllib.request import urlopen, Request

__author__ = 'totokaka'
__version__ = '0.1'

USER_AGENT = 'pySpaceGDN 0.1'
BASE = 'http://gdn.api.xereo.net/v1/'
DEBUG = False


def __request(url, page=1):
    """ Base Request.

    The parent function that all public functions call in order to initiate
    communication to the API.  Simply converts the Pythonic values into the
    the URL format expected by the API.  Also will add the User-Agent defined
    by the USER_AGENT variable.

    This takes two arguments:
        url    The URL to fetch. For example 'jar'
        page   The page number to fetch. Defaults to 1

    """
    _debug('requesting url {} page {}', repr(BASE+url), repr(page))
    url += '?page='+str(page)

    headers = {}
    headers['User-Agent'] = USER_AGENT
    headers['Accept'] = 'application/json'

    try:
        response = urlopen(Request(BASE + url, headers=headers)).read()
    except HTTPError as err:
        _debug('HTTPError')
        return json.loads(
            '\n'.join([line.decode("utf-8") for line in err.readlines()]))
    else:
        _debug('SUCCESS')
        return json.loads(response.decode("utf-8"))


def _request(url):
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
        response = __request(url, page=page)
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


def jars(jar=None):
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
    return _request(url)


def channels(jar=None, channel=None):
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
    return _request(url)


def versions(jar=None, channel=None, version=None):
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
    return _request(url)


def builds(jar=None, channel=None, version=None, build=None):
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
    return _request(url)


def _get_id(result, key, key_name='name', id_name='id'):
    """ Internal function for use in get_id.

    This function extacts the id_name for the results of one of the fetcher
    functions in this module if the key watches the value of the result's
    key_name.

    Return the value of the result's id_name if found. 0 if not found. <0 if
    result was error.

    """
    if type(result) is list:
        for element in result:
            if element[key_name].lower() == key.lower():
                return element[id_name]
        return 0
    else:
        return -result['code']


def get_id(jar=None, channel=None, version=None, build=None):
    """ Get the ID for jar, channel, version or build.

    This function will fetch the ID for the `highest` argument specified. This
    means that if jar, version and build are specified the id of the build will
    be returned. You should specify as many of the `lower` arguments as you
    can, so you get the correct result.

    Arguments:
        jar        The name of the jar, must be string
        channel    The name of the channel, must be string
        version    The name of the version, must be string
        build      The number of the build, must be integer

    Returns an integer with the id. The returned value will be zero if the
    object was not found, and the negative value of the error code if something
    went wrong.

    """
    if jar is not None:
        jar = _get_id(jars(), jar)
        if jar <= 0:
            return jar
    if channel is not None:
        channel = _get_id(channels(jar=jar), channel)
        if channel <= 0:
            return channel
    if version is not None:
        version = _get_id(versions(jar=jar, channel=channel), version,
                          'version')
        if version <= 0:
            return version
    if build is not None:
        build = _get_id(builds(jar=jar, channel=channel, version=version),
                        build, 'build')
        if build <= 0:
            return build

    if build is not None:
        return build
    elif version is not None:
        return version
    elif channel is not None:
        return channel
    elif jar is not None:
        return jar
    else:
        return 0
