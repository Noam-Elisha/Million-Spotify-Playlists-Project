import os, json, pickle

data_path = "..\spotify_million_playlist_dataset\data"

song_artist_map = {}
artists = set()

song_lengths_ms = []
playlist_lengths = []
for file in os.listdir(data_path):
    chunk = json.load(open(f"{data_path}/{file}", "r"))
    print(f"starting on slice {chunk['info']['slice']}")
    
    for playlist in chunk["playlists"]:
        playlist_lengths.append(playlist["num_tracks"])
        for song in playlist["tracks"]:
            song_lengths_ms.append(song["duration_ms"])
            artist = song["artist_uri"]
            id = song["track_uri"]
            if id in song_artist_map:
                continue
            song_artist_map[id] = artist
            artists.add(artist)

pickle.dump(song_artist_map, open("data/song_artists_uri.dat", "wb"))
pickle.dump(artists, open("data/artists_uri.dat", "wb"))

sum_songlen = sum(song_lengths_ms)
os.system(f'send_message "counted {len(artists)} unique artists"')
os.system(f'send_message "counted {sum_songlen/36000} total hours of music"')
os.system(f'send_message "counted {len(song_lengths_ms)} total songs"')
os.system(f'send_message "counted {sum(playlist_lengths)/len(playlist_lengths)} average songs per playlist"')