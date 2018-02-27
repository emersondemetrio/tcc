"""
Neural Network with different inputs

Obs.: python2
"""

from __future__ import print_function
import os
import argparse
import util.utils as utils

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

from tcc_essentia import run_esem

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

NN_INPUT_NUMBER = 5
NN_OUTPUT_NUMBER = 12
NN_LAYERS_NUMBER = 5
NN_TRAINING_ROUNDS = 10

def main():
    """main"""

    cur_path = os.path.abspath(".")

    desc = "TCC - Neural Nework."
    parser = argparse.ArgumentParser(description=desc)

    print("\n[ TCC - Neural Network ]\n%s\n" % desc)

    parser.add_argument('-i', '--input_folder', default=utils.get_valid_folder_path("results"))
    parser.add_argument('-f', '--input_file', required=True)
    parser.add_argument('-g', '--input_genre', required=True)
    parser.add_argument('-p', '--profile', default="profile.yml")

    parsed = parser.parse_args()

    output_folder = os.path.join(cur_path, "input")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    raw_input_path = run_esem(
        parsed.input_file,
        os.path.join(cur_path, "profile.yml"),
        output_folder
    )

    run_nn(
        parsed.input_folder,
        raw_input_path,
        parsed.input_genre,
        parsed.input_file.split("/")[-1]
    )

def get_genre_code(name):
    """
    Return the code for given genre
    """

    return GENRE_CODES[name]

def get_genre_code_tuple(genre_code):
    """return genre array"""

    codes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    codes[genre_code] = 1.0

    return tuple(codes)

def run_nn(data_set_path, raw_input_path, input_genre, song_name):
    """
    Run Neural Network
    """

    data_set = SupervisedDataSet(
        NN_INPUT_NUMBER,
        NN_OUTPUT_NUMBER
    )

    for root, _dirs, files in os.walk(data_set_path):
        for file_name in files:
            if ".json" in file_name:

                full_file_name = os.path.join(root, file_name)
                curr_track = utils.read_json_file(full_file_name)

                curr_track_genre = root.split("/")[6]
                genre_code = get_genre_code(curr_track_genre)

                print(
                    "Including in set: ",
                    file_name,
                    curr_track_genre,
                    genre_code
                )

                data_set.addSample(
                    (
                        float(curr_track["lowlevel"]["average_loudness"]),
                        float(curr_track["rhythm"]["bpm"]),
                        float(curr_track["rhythm"]["beats_loudness"]["mean"]),
                        float(curr_track["rhythm"]["danceability"]),
                        float(curr_track["tonal"]["chords_changes_rate"]),
                    ),
                    get_genre_code_tuple(genre_code),
                )

    neural_network = buildNetwork(
        NN_INPUT_NUMBER,
        NN_LAYERS_NUMBER,
        NN_OUTPUT_NUMBER,
        bias=False
    )

    trainer = BackpropTrainer(
        neural_network,
        data_set
    )

    for index in range(NN_TRAINING_ROUNDS):
        print("Training:", index, trainer.train())

    input_data = utils.read_json_file(raw_input_path)

    print("INPUT: ", raw_input_path, input_genre)

    restult = neural_network.activate(
        (
            float(input_data["lowlevel"]["average_loudness"]),
            float(input_data["rhythm"]["bpm"]),
            float(input_data["rhythm"]["beats_loudness"]["mean"]),
            float(input_data["rhythm"]["danceability"]),
            float(input_data["tonal"]["chords_changes_rate"]),
        )
    )

    print("RESULT: ")
    print([r * 100 for r in restult])

    utils.plot_genre_detected(
        [format(r * 100, '.2f') for r in restult],
        "{} ({})".format(song_name, input_genre)
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.show_message("Bye.")
