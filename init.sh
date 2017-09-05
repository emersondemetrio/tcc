#!/bin/bash

export PYTHONPATH=.

LAST_FM_KEY="last-fm-key-xD"

echo "STEP 1 - Extract Tracks to csv/json file:"

python3 file_analyst/track_extractor.py -i /media/emerson/Dados/music/;

echo "STEP 2 - Populate DB:"

python3 expose_steps/db_populate.py;

echo "STEP 3 - Update MBID:"

python3 expose_steps/mbid_crawler.py -k $LAST_FM_KEY;

echo "STEP 4 - Update TAGS:"

python3 expose_steps/tag_crawler.py -k $LAST_FM_KEY;

echo "STEP 4 - Create Spectros:"

python3 expose_steps/image_creator.py -n 1000 -workers_number=20 # this will take a loooot of time...

echo "STEP 5 - Training:"
echo "NOT YET IMPLEMENTED"

echo "STEP 6 - Analysis:"
echo "NOT YET IMPLEMENTED"

echo "STEP 7 - Test with new File:"
echo "NOT YET IMPLEMENTED"
