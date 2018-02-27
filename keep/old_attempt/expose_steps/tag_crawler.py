""" API Lvl 1 Tests """

import os
import argparse
import util.utils as utils

from util.httpy import Httpy
from crawler.last_fm import LastFm

def init_tests(last_fm_key, json_file, output_file):
    """ init tests """
    http_py = Httpy()
    last_fm = LastFm(last_fm_key, "http", "ws.audioscrobbler.com/2.0/", "json", http_py)
    run_tests(json_file, last_fm, output_file)

def parse_tags(tags):
    """ parsing last fm taggs """
    taggs = []
    for lfm_tag in tags:
        taggs.append(lfm_tag["name"])

    return taggs

def parse_level_2(track):
    """ parser lvl 2 """
    return {
        "artist": track["artist"]["name"],
        "track": track["name"],
        "mbid": track["mbid"],
        "tags": parse_tags(track["toptags"]["tag"])
    }


def run_tests(json_file, last_fm, output_file):

    """ running tests """
    level2 = []
    responses = []
    request_limit = 100
    request_counter = 0

    for mbid_track in utils.read_json_file(json_file):
        if mbid_track["mbid"]:
            if request_counter < request_limit:
                responses.append(
                    last_fm.get_track_info("", True, mbid_track["mbid"])["track"]
                )
                request_counter = request_counter + 1

    for rep in responses:
        level2.append(parse_level_2(rep))

    utils.write_json_file(output_file, level2)

def main():
    """ main """

    desc = "API LVL 1"
    parser = argparse.ArgumentParser(description=desc)

    print("\n[ TCC - API LVL 2 ]\n%s\n" % desc)
    parser.add_argument('-k', '--api_key', required=True)
    parser.add_argument('-f', '--input_folder', default=utils.get_valid_folder_path("results"))
    parser.add_argument('-i', '--input_file', default="level1")
    parser.add_argument('-o', '--output_file', default="level2")
    parsed = parser.parse_args()

    json_file = os.path.join(parsed.input_folder, parsed.input_file + ".json")
    output_file = os.path.join(parsed.input_folder, parsed.output_file + ".json")

    init_tests(parsed.api_key, json_file, output_file)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.show_message("Bye.")
