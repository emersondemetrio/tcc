""" API Lvl 1 Tests """

import os
import re
import json
import urllib
import argparse
import util.utils as utils

from util.httpy import Httpy
from util.tracks_db import TracksDb
from crawler.last_fm import LastFm

def url_encode(track):
    """ url encode """
    return urllib.parse.urlencode({
        "artist": utils.sanitize_string(track["artist"].replace("\uf022", ""), [], force=True),
        "track": re.sub(r"\w*\d\w*", "", track["track"]).strip()
    })

def parse_level_1(track):
    """ parse lvl 1 """
    return {
        "artist": track["artist"],
        "track": track["name"],
        "mbid": track["mbid"]
    }

def run_tests(json_file, last_fm, output_file, limit=False, request_limit=300000):
    """ running tests """
    tdb = TracksDb()

    all_tracks = utils.read_json_file(json_file)

    if limit:
        all_tracks = all_tracks[:request_limit]

    responses = []
    for pre_track in all_tracks:
        track = json.loads(pre_track)
        req_url = url_encode(track)
        incoming_response = last_fm.search_track(req_url)

        tmp_rp = incoming_response["results"]

        if (int(tmp_rp["opensearch:totalResults"]) > 0
                and tmp_rp["trackmatches"]["track"][0]["mbid"] == ""):

            new_attempt_url = urllib.parse.urlencode({
                "track": re.sub(r"\w*\d\w*", "", track["track"]).strip()
            })

            incoming_response = last_fm.search_track(new_attempt_url)

        if (int(tmp_rp["opensearch:totalResults"]) > 0
                and tmp_rp["trackmatches"]["track"][0]["mbid"] != ""):
                tdb.update_mbid(track, tmp_rp["trackmatches"]["track"][0]["mbid"])

        responses.append(incoming_response)

    possible_mbid_tracks = []

    for rep in responses:
        resp = rep["results"]

        if int(resp["opensearch:totalResults"]) > 0:
            possible_mbid_tracks.append(
                parse_level_1(
                    resp["trackmatches"]["track"][0]
                )
            )

    utils.write_json_file(output_file, possible_mbid_tracks)

def main():
    """ main """

    desc = "API LVL 1"
    parser = argparse.ArgumentParser(description=desc)

    print("\n[ TCC - API LVL 1 ]\n%s\n" % desc)
    parser.add_argument('-k', '--api_key', required=True)
    parser.add_argument('-f', '--input_folder', default=utils.get_valid_folder_path("results"))
    parser.add_argument('-i', '--input_file', default="output")
    parser.add_argument('-o', '--output_file', default="level1")
    parser.add_argument('-lp', '--limit_population', default="no")
    parser.add_argument('-tl', '--tracks_limit', default=300000)
    parsed = parser.parse_args()

    json_file = os.path.join(parsed.input_folder, parsed.input_file + ".json")
    output_file = os.path.join(parsed.input_folder, parsed.output_file + ".json")

    tracks_limit = int(parsed.tracks_limit)
    limit_population = False if parsed.limit_population == "no" else True

    last_fm_key = parsed.api_key
    http_py = Httpy()
    last_fm = LastFm(last_fm_key, "http", "ws.audioscrobbler.com/2.0/", "json", http_py)

    run_tests(json_file, last_fm, output_file, limit=limit_population, request_limit=tracks_limit)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.show_message("Bye.")
