"""
Utils Functions
"""

import os
import io
import json

def sanitize_string(string, replaces):
    """Replaces given arr in s"""

    for replacing, repl_with in replaces:
        string = string.replace(replacing, repl_with)
    #import re
    #string.encode('ascii', errors='ignore').decode()
    #string = re.sub(r'\[[0-9]+\]', r'', string)
    #return re.sub(r'[^\x00-\x7f]', r' ', string)
    return string

def get_valid_folder_path(folder_name):
    """Get Path"""

    return os.path.abspath(os.path.join(get_cur_location(), folder_name))

def get_cur_location():
    """Get CUR DIR"""

    return os.getcwd()

def parse_to_json(string_set):
    """Parse ARR to json"""

    file_arr = string_set.split("/")
    return json.dumps({
        "artist" : file_arr[0],
        "album"  : file_arr[1],
        "track"  : file_arr[2]
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
        json.dump(tracks, outfile)

def read_json_file(file_name):
    """Reads json File"""

    with open(file_name) as data_file:
        return json.load(data_file)

def show_message(msg, level=-1):
    """Show message with header based on level"""

    header = "INFO" if level < 0 else "WARNING" if level == 0 else "ERROR"
    print("\n[ {} ]\n{}".format(header, msg))
