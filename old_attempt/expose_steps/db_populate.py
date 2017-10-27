"""
Testing DB
"""

import os
import json
import argparse
import util.utils as utils
from util.tracks_db import TracksDb

def main():
    """
    Populating Database with csv/json file:
    """

    desc = "This module populate the Database with information in csv/json file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-f', '--input_folder', default="results")
    parser.add_argument('-i', '--input_file', default="output.json")
    parser.add_argument('-m', '--insert_mode', default="truncate")
    parser.add_argument('-lp', '--limit_population', default="no")
    parser.add_argument('-tl', '--tracks_limit', default=300000)

    parsed = parser.parse_args()

    insert_mode = parsed.insert_mode
    tracks_limit = int(parsed.tracks_limit)
    limit_population = False if parsed.limit_population == "no" else True

    tdb = TracksDb()

    if insert_mode == "truncate":
        tdb.truncate()

    json_file = os.path.join(parsed.input_folder, parsed.input_file)
    all_tracks = utils.read_json_file(json_file)

    if limit_population:
        all_tracks = all_tracks[:tracks_limit]

    for pre_track in all_tracks:
        track = json.loads(pre_track)
        tdb.insert_track(track)

        print(">", json.dumps(track), "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye.")
