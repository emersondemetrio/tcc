#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Build Atajo Office App
"""

from __future__ import print_function
import os
import subprocess
import hashlib

def log_message(msg, level=-1):
    """Log message preceded by the log level"""

    header = "INFO" if level < 0 else "WARNING" if level == 0 else "ERROR"
    print("\n[ {} ]\n{}".format(header, msg))

def get_hash(a_string, concat_after=""):
    """Return MD5 of string and concat something after"""

    return "{}{}".format(
        hashlib.md5(a_string).hexdigest(),
        concat_after
    )

def run_rim(command_name, music, output_folder, output_format, profile=""):
    """Run ESEM with args"""

    log_message("\nExtracting '{}' From: '{}' \n".format(command_name, music))

    output_file = os.path.join(
        output_folder,
        get_hash(music, output_format),
    )

    if not os.path.exists(output_file):
        if profile != "":
            command = [command_name, music, output_file, profile]
        else:
            command = [command_name, music, output_file]

        subprocess.call(command)

        print("\nDone.")

def run_mfcc(music, output_folder):
    """run essentia_streaming_mfcc"""

    run_rim("essentia_streaming_mfcc", music, output_folder, ".yml")

def run_esem(music, profile, output_folder):
    """run essentia_streaming_mfcc"""

    run_rim("essentia_streaming_extractor_music", music, output_folder, ".json", profile)

if __name__ == "__main__":
    try:
        print("Import this file.")
    except KeyboardInterrupt:
        print("Bye.")
