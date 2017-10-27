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
    "eletronic"         : 1,
    "grunge"            : 2,
    "hard-rock"         : 3,
    "hip-hop"           : 4,
    "indie"             : 5,
    "metal"             : 6,
    "new-metal"         : 7,
    "pop"               : 8,
    "pop-rock"          : 9,
    "progressive-metal" : 10,
    "punk"              : 11,
    "ska"               : 12
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


def walk_in_folders(full_path, output_folder):
    """
    Reading Information in Folder
    """

    data_set = SupervisedDataSet(13, 1)

    for root, _dirs, files in os.walk(full_path):
        for file_name in files:

            if ".json" in file_name:
                full_file_name = os.path.join(root, file_name)
                curr = utils.read_json_file(full_file_name)
                genre = root.split("/")[6]
                genre_code = get_genre_code(genre)

                print("FILE: ", file_name, curr["metadata"]["tags"]["file_name"], "GENRE: ", genre, genre_code)

                t_input = tuple(curr["lowlevel"]["mfcc"]["mean"])
                print(t_input)
                data_set.addSample(t_input, genre_code)

    neural_network = buildNetwork(13, 4, 1, bias=True)

    trainer = BackpropTrainer(neural_network, data_set)

    for i in range(2000):
        print(trainer.train())

    test = tuple([-631.971496582, 121.894683838, -30.9424991608, 9.7442483902, 0.577766537666, 5.28025388718, -4.99692964554, 8.93616294861, -1.2865601778, 3.46211123466, -0.934040367603, -5.2112455368, 4.20084095001])

    restult = neural_network.activate(test)
    print("RESULT: ", restult)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.show_message("Bye.")

