"""
This module reads the information from given folder
"""

import os
import argparse
import util.utils as utils
import json_parser

def main():
    """main"""

    desc = "This module reads the information from given folder."
    parser = argparse.ArgumentParser(description=desc)

    print("\n[ TCC - TRACK EXTRACTOR ]\n%s\n" % desc)

    parser.add_argument('-i', '--input_folder', default=utils.get_cur_location())
    parser.add_argument('-f', '--output_folder', default=utils.get_valid_folder_path("results"))
    parser.add_argument('-o', '--output_file', default="output")

    parsed = parser.parse_args()

    csv_file = os.path.join(parsed.output_folder, parsed.output_file + ".txt")
    json_file = os.path.join(parsed.output_folder, parsed.output_file + ".json")

    content = walk_in_folders(parsed.input_folder)
    utils.write_file_with(csv_file, content)

    json_parser.parse(parsed.input_folder, csv_file, json_file)

    utils.show_message("All done, take a look: %s" % csv_file)

def walk_in_folders(full_path):
    """
    Reading Information in Folder
    """

    sanitize_set = [
        ["./", ""],
        [".mp3", ""],
        [full_path, ""]
    ]

    output = ""
    for root, _dirs, files in os.walk(full_path):
        for file_name in files:
            if ".mp3" in file_name:
                full_file_name = os.path.join(root, file_name)
                file_as_array = utils.sanitize_string(full_file_name, sanitize_set).split("/")

                output = "{}{}/{}/{};\n".format(
                    output,
                    file_as_array[0],
                    file_as_array[1],
                    file_as_array[2]
                )
                print("Reading: ", file_as_array)
    return output

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.show_message("Bye.")
