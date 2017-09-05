from util.tracks_db import TracksDb

tdb = TracksDb()

conditions = [{
    "field": "mbid",
    "value": "IS NULL"
}]

tracks = tdb.get_tracks("id, artist, name", conditions)

for track in tracks:
    print("Track: ", track)