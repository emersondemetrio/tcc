"""
This module reads the information from given folder
"""
from __future__ import print_function
import os
import argparse
import util.utils as utils
import json
import sys
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

GENRE_CODES = {
    "eletronic"         : 0,
    "grunge"            : 1,
    "hard-rock"         : 2,
    "hip-hop"           : 3,
    "indie"             : 4,
    "metal"             : 5,
    "new-metal"         : 6,
    "pop"               : 7,
    "pop-rock"          : 8,
    "progressive-metal" : 9,
    "punk"              : 10,
    "ska"               : 11
}

def main():
    """main"""

    desc = "This module reads the information from given folder."
    parser = argparse.ArgumentParser(description=desc)

    print("\n[ TCC - TRACK EXTRACTOR ]\n%s\n" % desc)

    parser.add_argument('-i', '--input_folder', default=utils.get_valid_folder_path("results"))
    parser.add_argument('-o', '--output_folder', default=utils.get_valid_folder_path("results"))
    parser.add_argument('-p', '--profile', default="profile.yml")

    parsed = parser.parse_args()

    walk_in_folders(
        parsed.input_folder,
        os.path.join(parsed.output_folder, "parsed")
    )

def get_genre_code(name):
    """
    Return the code for given genre
    """

    return GENRE_CODES[name]


def get_genre_code_tuple(genre_code):
    """return genre array"""

    codes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    codes [genre_code] = 1;

    return tuple(codes)

def walk_in_folders(full_path, output_folder):
    """
    Reading Information in Folder
    """

    data_set = SupervisedDataSet(13, 12)

    for root, _dirs, files in os.walk(full_path):
        for file_name in files:

            if ".json" in file_name:
                full_file_name = os.path.join(root, file_name)
                curr = utils.read_json_file(full_file_name)
                genre = root.split("/")[6]
                genre_code = get_genre_code(genre)

                print("FILE: ", file_name, curr["metadata"]["tags"]["file_name"], "GENRE: ", genre, genre_code)

                t_input = tuple(curr["lowlevel"]["mfcc"]["mean"])

                data_set.addSample(t_input, get_genre_code_tuple(genre_code))

    neural_network = buildNetwork(13, 4, 12, bias=True)

    trainer = BackpropTrainer(neural_network, data_set)

    print("Training...")

    for i in range(1000):
        trainer.train()
    print("Done.")

    ## pop-rock
    test = tuple(
        [-639.92388916, 92.7311630249, -6.63165950775, 22.4517841339, 7.37339067459, -1.02510261536, -5.08265829086, 1.70268416405, -2.5901350975, -6.00173950195, -7.20496797562, -3.18132972717, -3.99400472641]
    )

    ge_exp = "new-metal"
    ge_exp_code = get_genre_code(ge_exp)

    result = neural_network.activate(test)
    print("RESULT: ")

    for r in result:
        print("R: ", r)

    print("EXPECT POS: ", ge_exp, ge_exp_code)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.show_message("Bye.")

