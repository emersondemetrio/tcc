#!/bin/bash

export PYTHONPATH=.

echo "STEP 1 - Extract Tracks to csv/json file:"

python3 file_analyst/track_extractor.py -i /media/emerson/Dados/music/
