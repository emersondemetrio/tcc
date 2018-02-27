"""
Utils Functions
"""

import os
import io
import re
import json
import datetime as dt
import time
import shutil
import matplotlib.pyplot as plt

def get_cur_datetime():
    """get cur datetime"""

    return dt.datetime.utcfromtimestamp(time.time()).strftime("%Y/%m/%d %H:%M:%S")

def create_folder(abs_path, force=False):
    """Create a folder forcing (if force)"""

    if force:
        try:
            shutil.rmtree(abs_path)
            show_message("Removing folder: '%s'" % abs_path)
        except OSError:
            show_message("Unable to remove folder: '%s'" % abs_path, 1)

        try:
            os.makedirs(abs_path)
        except OSError:
            show_message("Unable to create folder: '%s'" % abs_path, 1)
    else:
        try:
            os.makedirs(abs_path)
        except OSError:
            if os.path.exists(abs_path):
                print("Folder '%s' already exists." % abs_path)
            else:
                show_message("Unable to create folder: '%s'" % abs_path, 1)


def sanitize_string(string, replaces, force=False):
    """Replaces given arr in s"""

    for replacing, repl_with in replaces:
        string = string.replace(replacing, repl_with)

    if force:
        string.encode('ascii', errors='ignore').decode()
        string = re.sub(r'\[[0-9]+\]', r'', string)
        string = re.sub(r'[^\x00-\x7f]', r' ', string)

    return string

def get_valid_folder_path(folder_name):
    """Get Path"""

    return os.path.abspath(os.path.join(get_cur_location(), folder_name))

def get_cur_location():
    """Get CUR DIR"""

    return os.getcwd()

def parse_to_json(file_arr):
    """Parse ARR to json"""

    return json.dumps({
        "artist": sanitize_string(file_arr[0], [], True),
        "album": file_arr[1],
        "track": file_arr[2],
        "path": file_arr[3],
    })

def write_file_with(name, content):
    """Writes file with content"""

    content.strip()
    writing_file = open(name, 'w')
    writing_file.write(content)
    writing_file.close()

def read_file(file_name):
    """Read File"""

    with io.open(file_name, encoding="utf8") as data_file:
        content = data_file.read().splitlines()

    return content

def write_json_file(file_name, tracks):
    """Write json File"""

    with open(file_name, 'w') as outfile:
        json.dump(tracks, outfile, sort_keys=True, indent=4, separators=(',', ': '))

def read_json_file(file_name):
    """Reads json File"""

    with open(file_name) as data_file:
        return json.load(data_file)

def show_message(msg, level=-1):
    """Show message with header based on level"""

    header = "INFO" if level < 0 else "WARNING" if level == 0 else "ERROR"
    print("\n[ {} ]\n{}".format(header, msg))

def plot_genre_detected(results, song_name):
    """
    Plot
    """

    labels = [
        "eletronic {} %".format(results[0]),
        "grunge {} %".format(results[1]),
        "hard-rock {} %".format(results[2]),
        "hip-hop {} %".format(results[3]),
        "indie {} %".format(results[4]),
        "metal {} %".format(results[5]),
        "new-metal {} %".format(results[6]),
        "pop {} %".format(results[7]),
        "pop-rock {} %".format(results[8]),
        "progressive-metal {} %".format(results[9]),
        "punk {} %".format(results[10]),
        "ska {} %".format(results[11])
    ]

    colors = [
        "black",
        "red",
        "blue",
        "white",
        "brown",
        "yellowgreen",
        "gold",
        "lightskyblue",
        "lightcoral",
        "orange",
        "violet",
        "purple"
    ]

    patches, texts = plt.pie(results, colors=colors, startangle=90)

    plt.title(song_name)
    plt.legend(patches, labels, loc="best")

    plt.axis('equal')
    plt.tight_layout()
    plt.show()
