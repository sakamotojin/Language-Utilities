#!/usr/bin/env python
import urllib.request

def getSite(url):
    return urllib.request.urlopen(url)

if __name__ == '__main__':
    content = getSite('http://www.google.com').read()
    print(content)