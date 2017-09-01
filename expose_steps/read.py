import os
import json
import sys
import re
import pprint

reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')

import util.utils as file_utils
import urllib

def url_encode(track):
    return urllib.urlencode({
        "artist": track["artist"].replace("\uf022", ""),
        "track": re.sub(r"\w*\d\w*", "", track["track"]).strip()
    })

request_limit = 100
request_counter = 0
requests = []

for pre_track in file_utils.read_json_file("D:/TCC/tcc/results/tracks.json"):

    if request_counter < request_limit:
        track = json.loads(pre_track)
        requests.append( url_encode(track) )
        request_counter = request_counter + 1

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(requests)