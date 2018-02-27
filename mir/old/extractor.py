"""
This module reads the information from given folder
"""

import os
import argparse
import util.utils as utils
import tcc_essentia

def main():
    """main"""

    desc = "This module reads the information from given folder."
    parser = argparse.ArgumentParser(description=desc)

    print("\n[ TCC - TRACK EXTRACTOR ]\n%s\n" % desc)

    parser.add_argument('-i', '--input_folder', default=utils.get_cur_location())
    parser.add_argument('-o', '--output_folder', default=utils.get_valid_folder_path("results"))
    parser.add_argument('-p', '--profile', default="profile.yml")

    parsed = parser.parse_args()

    walk_in_folders(
        parsed.input_folder,
        parsed.profile,
        parsed.output_folder
    )

def walk_in_folders(full_path, profile, output_folder):
    """
    Reading Information in Folder
    """

    genres = dict()

    for root, _dirs, files in os.walk(full_path):
        for file_name in files:
            if ".mp3" in file_name:
                full_file_name = os.path.join(root, file_name)
                genre = root.split("/")[5]
                genre_dir = os.path.join(output_folder, genre)

                if not os.path.exists(genre_dir):
                    os.makedirs(genre_dir)

                if not genre in genres:
                    genres[genre] = []

                genres[genre].append(full_file_name)


    for genre in genres:
        genre_dir = os.path.join(output_folder, genre)

        for music in genres[genre]:
            tcc_essentia.run_esem(
                music,
                profile,
                genre_dir
            )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.show_message("Bye.")
