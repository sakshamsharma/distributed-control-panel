#!/usr/bin/env python3

import urllib.request


def get_link(ip, port, path):
    return "http://{}:{}/{}".format(ip, port, path)


def make_get_request(ip, port, path):
    contents = urllib.request.urlopen(get_link(ip, port, path)).read()
    return contents


def make_post_request(ip, port, path, data):
    contents = urllib.request.urlopen(get_link(ip, port, path),
                                      data=data).read()
    return contents
