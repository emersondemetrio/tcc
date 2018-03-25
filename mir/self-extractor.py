"""
This module reads the information from given folder
"""

from __future__ import print_function
import os
import argparse
import json
import sys

import tcc_essentia

OUTPUT_FOLDER = os.path.abspath("./results")

def main():
	"""main"""

	desc = "This module reads the information from given folder."
	parser = argparse.ArgumentParser(description=desc)

	print("\n[ TCC - TRACK EXTRACTOR ]\n%s\n" % desc)

	parser.add_argument('-i', '--input_folder')
	parser.add_argument('-o', '--output_folder', default=OUTPUT_FOLDER)
	parser.add_argument('-p', '--profile', default="profile.yml")

	parsed = parser.parse_args()

	walk_in_folders(parsed.input_folder, parsed.output_folder)


def get_path(a, b):
	return os.path.abspath(os.path.join(a, b))

def walk_in_folders(input_folder, output_folder):

	for root, _dirs, files in os.walk(input_folder):
		for file_name in files:
			if ".mp3" in file_name:
				path = get_path(root, file_name)
				tcc_essentia.run_esem(
					path,
					"profile.yml",
					output_folder
				)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("done.")
