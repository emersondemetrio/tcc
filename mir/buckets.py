"""
Buckets Creator
"""

from __future__ import print_function
import os
import argparse
import json

def main():
	"""main"""

	desc = "\n[ TCC - Buckets Creator ]\n%s\n"
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('-i', '--input_folder')
	parsed = parser.parse_args()
	walk_in_folder(parsed.input_folder)

def read_json_file(file_name):
	"""Reads json File"""

	with open(file_name) as data_file:
		return json.load(data_file)

def create_genre_folder(name):
	print("oi")

def walk_in_folder(folder_name):

	for root, _dirs, files in os.walk(folder_name):
		for file_name in files:
			if ".json" in file_name:
				full_file_name = os.path.join(root, file_name)
				curr_track = read_json_file(full_file_name)
				try:
					bucket = curr_track['metadata']['tags']['genre'][0].split(',')[0]
					print(file_name, "genre: ", bucket)
				except NameError as identifier:
					print(NameError)




if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Bye.")
