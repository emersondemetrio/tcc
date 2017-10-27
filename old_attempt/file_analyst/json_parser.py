"""
This module read and write information
"""

import io
import os
import json
import util.utils as utils

def parse(lib_path, csv_file, json_file_name):
    """Reading Walk Result"""

    tracks_arr = []
    with io.open(csv_file, encoding="utf8") as data_file:
        content = data_file.read().splitlines()

    for music in content:
        music = music.replace(";", "")
        music_set = music.split("/")
        music_set.append(os.path.join(lib_path, music + ".mp3"))

        tracks_arr.append(
            utils.parse_to_json(music_set)
        )
    utils.write_json_file(json_file_name, tracks_arr)

def show_results(json_file_name):
    """ Show Results """

    for pre_track in utils.read_json_file(json_file_name):
        track = json.loads(pre_track)
        print("Artista: " + track['artist'])
        print("Album: " + track['album'])
        print("Track: " + track['track'])
        print("Path: " + track['path'])
        print("\n---\n")
