# -*- coding: utf-8 -*-
# For Python3
import urllib.request
from urllib.parse import urlparse
import json
import requests

class HttpClient:

    def __init__(self, baseUrl ):
        self.baseUrl = baseUrl

    def requestUrl(self, url, headers={}):
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req).read()
        try:
            content = response.decode('utf-8')
        except UnicodeDecodeError:
            content = response

        # print("[RES] content = %s " % (content))
        return content