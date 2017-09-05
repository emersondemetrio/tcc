"""
Creating Music Images
"""

import os
import json
import sys
import argparse
import subprocess
import util.utils as utils
from util.tracks_db import TracksDb

def create_image(input_name, output_name):
    """
    Creates song image
    """
    utils.show_message("{} -> {}".format(input_name, output_name))
    #ffmpeg -i 01\ Disorder.mp3 -filter_complex \
    # "compand,showwavespic=s=640x120" -frames:v 1 joy-division-disorder.png

    subprocess.call([
        "ffmpeg",
        "-i",
        input_name,
        "-filter_complex",
        "compand,showwavespic=s=640x120",
        "-frames:v",
        "1",
        output_name
    ])

def main():
    """
    Populating Database with csv/json file:
    """

    desc = "This module Create png images from songs."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-udb', '--use_db', default="no")
    parser.add_argument('-ufl', '--use_file_list', default="no")
    parser.add_argument('-f', '--input_folder', default=utils.get_valid_folder_path("results"))
    parser.add_argument('-i', '--input_file', default="output")

    parsed = parser.parse_args()

    use_db = True if parsed.use_db == "yes" else False
    use_list = True if parsed.use_file_list == "yes" else False

    if not use_db and not use_list:
        use_db = True

    songs_path_list = []

    if use_list:
        json_file = os.path.join(parsed.input_folder, parsed.input_file + ".json")
        if not os.path.exists(json_file):
            utils.show_message("File does not exists: %s" % json_file, 1)
            print("Please run previous steps first.\nAborting.")
            sys.exit(-1)

        all_tracks = utils.read_json_file(json_file)
        for pre_track in all_tracks:
            track = json.loads(pre_track)
            songs_path_list.append(track)

    if use_db:
        tdb = TracksDb()
        for track in tdb.get_tracks():
            track['track'] = track['name']
            songs_path_list.append(track)

    songs_path_list = songs_path_list[:100]
    images_folder = utils.get_valid_folder_path("results/images")

    folders = []
    for song in songs_path_list:
        artist_folder = os.path.join(images_folder, song['artist'])

        if artist_folder not in folders:
            utils.create_folder(artist_folder, force=True)
            folders.append(artist_folder)

        output_file = song['path'].split("/").pop()
        output_file = os.path.join(artist_folder, output_file.replace(".mp3", ".png"))

        create_image(song['path'], output_file)

        for fdr in folders:
            print("FDR: ", fdr)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye.")
