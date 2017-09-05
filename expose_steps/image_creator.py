"""
Creating Music Images
"""

import os
from threading import Thread
import argparse
import subprocess
import util.utils as utils
from util.tracks_db import TracksDb

def create_image(input_name, output_name):
    """
    Creates song image
    Original Command:
    ffmpeg -i input.mp3 -filter_complex "compand,showwavespic=s=640x120" -frames:v 1 output.png
    """

    if not os.path.exists(output_name):
        print("New Image: {}".format(output_name))

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

def create_images_from_list(songs_path_list, images_folder):
    """Create image creating worker"""

    folders = []
    for song in songs_path_list:
        artist_folder = os.path.join(images_folder, song['artist'])

        if not os.path.exists(artist_folder):
            utils.create_folder(artist_folder)
            folders.append(artist_folder)

        output_file = song['path'].split("/").pop()
        output_file = os.path.join(artist_folder, output_file.replace(".mp3", ".png"))

        create_image(song['path'], output_file)

def main():
    """
    Create ffmpeg workers
    """

    desc = "This module Create png images from songs."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-n', '--total_number', default=1000)
    parser.add_argument('-w', '--workers_number', default=1)
    parser.add_argument('-o', '--output_folder', default="results/images")

    parsed = parser.parse_args()
    workers_number = int(parsed.workers_number)
    total = int(parsed.total_number)

    images_folder = utils.get_valid_folder_path(parsed.output_folder)
    tdb = TracksDb()

    for worker_number in range(0, workers_number):
        songs_path_list = []
        print("\nNew Worker: %s\n" % worker_number)

        conditions = [{
            "field": "has_image",
            "value": "= 0"
        }]

        for track in tdb.get_tracks(conditions=conditions, limit=total):
            track['track'] = track['name']
            tdb.update_track(track['id'], field="has_image", val=1, is_int=True)
            songs_path_list.append(track)

        cim_thread = Thread(
            target=create_images_from_list,
            args=(songs_path_list[:total], images_folder,)
        )

        cim_thread.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye.")
