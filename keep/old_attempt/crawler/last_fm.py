""" Last FM Module """

import sys
import os
import util.httpy

class LastFm:
    """ LastFM Class """
    def __init__(self, api_key, protocol, base_url, format, httpy):
        self.api_key = api_key
        self.protocol = protocol
        self.base_url = base_url
        self.format = format
        self.httpy = httpy
        self.methods = {
            'search': 'track.search',
            'getInfo': 'track.getInfo'
        }

    def get_request_url(self, method, params=""):
        """get_request_url"""

        req_url = "{}://{}?method={}&api_key={}".format(
            self.protocol,
            self.base_url,
            self.methods[method],
            self.api_key
        )

        if params:
            req_url = req_url + "&" + params

        return req_url + "&format=" + self.format

    def search_track(self, search_params):
        """ Search Track """
        # http://ws.audioscrobbler.com/2.0/?method=track.search&track=linkin+park+crawling&api_key=API_KEY&format=json
        request_url = self.get_request_url('search', search_params)
        print(request_url)
        return self.httpy.get(request_url)

    def get_track_info(self, url_encoded_search="", use_mbid=False, mbid=""):
        """ get_track_info """
        request_url = ""
        # http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=API_KEY&artist=linkin%20park&track=crawling&format=json
        # http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=API_KEY&mbid=MBID&format=json

        if use_mbid:
            request_url = self.get_request_url('getInfo', "&mbid=" + mbid)
        else:
            request_url = self.get_request_url('getInfo', url_encoded_search)

        print(request_url)

        return self.httpy.get(request_url)
