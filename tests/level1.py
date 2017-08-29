""" API Lvl 1 Tests """

import os
import re
import json
import urllib
import argparse
import util.utils as utils

from util.httpy import Httpy
from crawler.last_fm import LastFm

def init_tests(last_fm_key, json_file, output_file):
    """ init tests """
    http_py = Httpy()
    last_fm = LastFm(last_fm_key, "http", "ws.audioscrobbler.com/2.0/", "json", http_py)
    run_tests(json_file, last_fm, output_file)

def url_encode(track):
    """ url encode """
    return urllib.parse.urlencode({
        "artist": track["artist"].replace("\uf022", ""),
        "track": re.sub(r"\w*\d\w*", "", track["track"]).strip()
    })

def parse_level_1(track):
    """ parse lvl 1 """
    return {
        "artist": track["artist"],
        "track": track["name"],
        "mbid": track["mbid"]
    }

def run_tests(json_file, last_fm, output_file):
    """ running tests """

    request_limit = 100
    request_counter = 0
    responses = []

    for pre_track in utils.read_json_file(json_file):

        if request_counter < request_limit:
            track = json.loads(pre_track)
            responses.append(last_fm.search_track(url_encode(track)))
            request_counter = request_counter + 1
    print(responses)
    level1 = []

    for rep in responses:
        resp = rep["results"]
        print(resp)
        if int(resp["opensearch:totalResults"]) > 0:
            level1.append(
                parse_level_1(
                    resp["trackmatches"]["track"][0]
                )
            )

        utils.write_json_file(output_file, level1)

def main():
    """ main """

    desc = "API LVL 1"
    parser = argparse.ArgumentParser(description=desc)

    print("\n[ TCC - API LVL 1 ]\n%s\n" % desc)
    parser.add_argument('-k', '--api_key', required=True)
    parser.add_argument('-f', '--input_folder', default=utils.get_valid_folder_path("results"))
    parser.add_argument('-i', '--input_file', default="output")
    parser.add_argument('-o', '--output_file', default="level1")
    parsed = parser.parse_args()

    json_file = os.path.join(parsed.input_folder, parsed.input_file + ".json")
    output_file = os.path.join(parsed.input_folder, parsed.output_file + ".json")

    init_tests(parsed.api_key, json_file, output_file)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.show_message("Bye.")
