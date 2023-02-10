import utils
import pickle
import spotipy
import time
import os, sys
import json
from spotipy.oauth2 import SpotifyOAuth

# oauth = SpotifyOAuth(client_id="", client_secret=", scope ="user-modify-playback-state", redirect_uri="http://localhost:8080")
# sp = spotipy.Spotify(auth_manager=oauth)

oauth = SpotifyOAuth(client_id="", client_secret="", scope ="user-modify-playback-state", redirect_uri="http://localhost:8080")
sp = spotipy.Spotify(auth_manager=oauth)

artist_uris = pickle.load(open("data/artists_uri.dat", "rb"))
to_process = []
artist_data = {}
i = 0
total = len(artist_uris)
percentages = range(0, 101)
for artist in artist_uris:
    to_process.append(artist)
    if len(to_process) == 50:
        print(f"Processing 50 artists")
        processed_artists = sp.artists(to_process)["artists"]
        for data in processed_artists:
            artist_data[data["uri"]] = data
        print(f"Done")
        time.sleep(30)
        to_process = []
    i += 1
    if i / total * 100 in percentages:
        os.system(f'send_message "Processed {i/total * 100} of all artists"')
if len(to_process) != 0:
    processed_artists = sp.artists(to_process)["artists"]
    for data in processed_artists:
        artist_data[data["uri"]] = data
    to_process = []
pickle.dump(artist_data, open("data/artist_info.dat", "wb"))
os.system(f'send_message "Processed all artists"')
