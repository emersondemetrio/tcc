"""
Testing DB
"""

import os
import json
import util.utils as utils
from util.tracks_db import TracksDb

def test():
    """
    Testing
    """
    tdb = TracksDb()

    json_file = os.path.join("results", "output.json")

    for pre_track in utils.read_json_file(json_file):
        track = json.loads(pre_track)
        tdb.insert_track(track)
        print(">", json.dumps(track), "\n")


if __name__ == "__main__":
    try:
        test()
    except KeyboardInterrupt:
        print("Bye.")
