#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Build Atajo Office App
"""

from __future__ import print_function
import os
import sys
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

def run_esem(music, output, profile):
    """Run ESEM with args"""

    subprocess.call([
        "essentia_streaming_extractor_music",
        music,
        output,
        profile
    ])

def main():
    """Main"""

    if len(sys.argv) < 2:
        log_message("Unable to run. Please inform the music")
        sys.exit(-1)
    else:
        music = os.path.abspath(sys.argv[1])
        output = os.path.abspath(
            os.path.join(
                ".",
                "output",
                get_hash(music, ".json"),
            )
        )
        profile = os.path.abspath(
            os.path.join(".", "profile.yml")
        )
        run_esem(music, output, profile)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_message("Bye.")
