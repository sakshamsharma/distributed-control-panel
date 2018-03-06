#!/usr/bin/env python3

import urllib.request
import urllib.error


def get_link(ip, port, path):
    return "http://{}:{}/{}".format(ip, port, path)


def make_get_request(ip, port, path):
    contents = ''
    try:
        contents = urllib.request.urlopen(get_link(ip, port, path)).read()
    except urllib.error.HTTPError as e:
        print("Error during GET request:", e)
    finally:
        return contents


def make_post_request(ip, port, path, data):
    contents = ''
    try:
        contents = urllib.request.urlopen(get_link(ip, port, path),
                                          data=data).read()
    except urllib.error.HTTPError as e:
        print("Error during POST request:", e)
    finally:
        return contents
    return contents
