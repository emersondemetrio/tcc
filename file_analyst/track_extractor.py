"""
This module reads the information from given folder
"""

import os
import argparse
import util.utils as utils

def main():
    """main"""

    desc = "This module reads the information from given folder."
    parser = argparse.ArgumentParser(description=desc)

    print("\n[ TCC - TRACK EXTRACTOR]\n%s\n" % desc)

    parser.add_argument('-i', '--input_folder', default=utils.get_cur_location())
    parser.add_argument('-d', '--output_folder', default=utils.get_valid_folder_path("results"))
    parser.add_argument('-f', '--output_file', default="output.txt")

    parsed = parser.parse_args()
    output_file_path = os.path.join(parsed.output_folder, parsed.output_file)
    content = walk_in_folders(parsed.input_folder)
    utils.write_file_with(output_file_path, content)
    utils.show_message("All done, take a look: %s" % output_file_path)

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
                    file_as_array[0].strip(),
                    file_as_array[1].strip(),
                    file_as_array[2].strip()
                )
                print(file_as_array)
    return output

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.show_message("Bye.")
