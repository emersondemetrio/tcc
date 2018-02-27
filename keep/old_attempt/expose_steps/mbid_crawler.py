""" API Lvl 1 Tests """

import os
import re
import sys
import json
import urllib
import argparse
import util.utils as utils

from util.httpy import Httpy
from util.tracks_db import TracksDb
from crawler.last_fm import LastFm

def check_result(result):
    """Check request result"""

    if "results" in result:
        return True
    return False

def get_mbid(result):
    """Check request result"""

    result = result["results"]
    if int(result["opensearch:totalResults"]) > 0:
        if result["trackmatches"]["track"][0]["mbid"] != "":
            mbid = result["trackmatches"]["track"][0]["mbid"]
            return mbid
    return ""

def request_attempt(track, req_url, last_fm, tdb):
    """do request and update"""

    incoming_response = last_fm.search_track(req_url)

    if check_result(incoming_response):
        mbid = get_mbid(incoming_response)
        if mbid:
            tdb.update_mbid(track, mbid)
            return True
    return False

def run_tests(json_file, last_fm, limit=False, untranslated_only=False, request_limit=300000):
    """ running tests """

    tdb = TracksDb()
    all_tracks = utils.read_json_file(json_file)

    if limit:
        all_tracks = all_tracks[:request_limit]

    if not untranslated_only:
        for pre_track in all_tracks:
            track = json.loads(pre_track)

            parsed_track_name = re.sub(r"\w*\d\w*", "", track["track"]).strip()
            parsed_track_name = re.sub(r'\d+', '', parsed_track_name)

            attempts = [
                urllib.parse.urlencode({
                    "artist": utils.sanitize_string(
                        track["artist"].replace("\uf022", ""), [], force=True
                    ),
                    "track": track["track"].strip()
                }),
                urllib.parse.urlencode({
                    "track": re.sub(r"\w*\d\w*", "", track["track"]).strip()
                }),
                urllib.parse.urlencode({
                    "track": parsed_track_name
                }),
                urllib.parse.urlencode({
                    "track": re.sub(r'\d+', '', track["track"])
                }),
                urllib.parse.urlencode({
                    "artist": utils.sanitize_string(
                        track["artist"].replace("\uf022", ""), [], force=True
                    ),
                    "track": re.sub(r'\d+', '', track["track"])
                }),
            ]

            for request_url in attempts:
                print("Track: {}\nAttempt:{}\n\n".format(track['track'], request_url))
                translated = request_attempt(track, request_url, last_fm, tdb)

                if translated:
                    break

    proced_untranslated_tracks(tdb, last_fm)

def proced_untranslated_tracks(tdb, last_fm):
    """Untranslated Tracks in DB"""
    conditions = [{
        "field": "mbid",
        "value": "IS NULL"
    }]

    tracks = tdb.get_tracks("id, artist, name", conditions)

    for track in tracks:
        track["track"] = track["name"]
        print("Track: ", track)
        parsed_track_name = re.sub(r"\w*\d\w*", "", track["track"]).strip()
        parsed_track_name = re.sub(r'\d+', '', parsed_track_name)

        """
        Chage this!
        """
        attempts = [
            urllib.parse.urlencode({
                "artist": utils.sanitize_string(
                    track["artist"].replace("\uf022", ""), [], force=True
                ),
                "track": track["track"].strip()
            }),
            urllib.parse.urlencode({
                "track": re.sub(r"\w*\d\w*", "", track["track"]).strip()
            }),
            urllib.parse.urlencode({
                "track": parsed_track_name
            }),
            urllib.parse.urlencode({
                "track": re.sub(r'\d+', '', track["track"])
            }),
            urllib.parse.urlencode({
                "artist": utils.sanitize_string(
                    track["artist"].replace("\uf022", ""), [], force=True
                ),
                "track": re.sub(r'\d+', '', track["track"])
            }),
        ]


        for request_url in attempts:
            print("Track: {}\nAttempt:{}\n\n".format(track['track'], request_url))
            translated = request_attempt(track, request_url, last_fm, tdb)

            if translated:
                break
def main():
    """ main """

    desc = "API LVL 1"
    parser = argparse.ArgumentParser(description=desc)

    print("\n[ TCC - API XT MBID 1 ]\n%s\n" % desc)
    parser.add_argument('-k', '--api_key', required=True)
    parser.add_argument('-f', '--input_folder', default=utils.get_valid_folder_path("results"))
    parser.add_argument('-i', '--input_file', default="output")
    parser.add_argument('-lp', '--limit_population', default="no")
    parser.add_argument('-uo', '--untranslated_only', default="no")
    parser.add_argument('-tl', '--tracks_limit', default=300000)
    parsed = parser.parse_args()

    json_file = os.path.join(parsed.input_folder, parsed.input_file + ".json")
    if not os.path.exists(json_file):
        utils.show_message("File does not exists: %s" % json_file, 1)
        print("Please run previous steps first.\nAborting.")
        sys.exit(-1)

    tracks_limit = int(parsed.tracks_limit)
    limit_population = False if parsed.limit_population == "no" else True
    untranslated_only = False if parsed.untranslated_only == "no" else True

    last_fm_key = parsed.api_key
    http_py = Httpy()
    last_fm = LastFm(last_fm_key, "http", "ws.audioscrobbler.com/2.0/", "json", http_py)

    run_tests(
        json_file,
        last_fm,
        limit=limit_population,
        untranslated_only=untranslated_only,
        request_limit=tracks_limit
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.show_message("Bye.")
