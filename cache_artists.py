import utils
import pickle
import spotipy
import time
import os, sys
import json
from spotipy.oauth2 import SpotifyOAuth

# oauth = SpotifyOAuth(client_id="c50a8e4da53044e4a1c90cd037b22ed7", client_secret="a22f42a4f5744e0ca9d7a634389c2e76", scope ="user-modify-playback-state", redirect_uri="http://localhost:8080")
# sp = spotipy.Spotify(auth_manager=oauth)

oauth = SpotifyOAuth(client_id="dd6bf69c0ef44869a55574e11ba8b1d9", client_secret="6fcb51ecd6c845bf81b991235829ae1b", scope ="user-modify-playback-state", redirect_uri="http://localhost:8080")
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
