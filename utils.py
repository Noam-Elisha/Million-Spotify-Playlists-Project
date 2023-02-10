import sqlite3
import pandas as pd
import json
import pickle

class DataInterface:

    default_value = [None, None, None, None, None, None,None, None, None, None, None, None, None, None, None, None, None, None]

    def __init__(self, database_path = "data/playlistDB.db", json_folder_path = "../spotify_million_playlist_dataset/data", song_cache_path = "data/song_cache.dat"):
        self.database_path = database_path
        self.json_folder_path = json_folder_path
        self.con = sqlite3.connect(self.database_path)
        self.cur = self.con.cursor()
        self.song_map = pickle.load(open(song_cache_path, "rb"))
        self.cache_slice = -1
        self.cached_data = None

    def get_songs_from_playlist(self, pid):
        playlist = self.get_playlist_tracks(pid)
        return list(map(lambda x: self.song_map.get(x["track_uri"], self.default_value), playlist))

    def get_playlist_as_dataframe(self, pid):
        playlist = self.get_songs_from_playlist(pid)
        return pd.DataFrame(playlist, columns = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "type", "id", "uri", "track_href", "analysis_url", "duration_ms", "time_signature"])

    def get_playlist_info(self, pid):
        slice = pid//1000 * 1000
        if slice == self.cache_slice:
            return self.cached_data["playlists"][pid%1000]
        else:
            file = f"mpd.slice.{slice}-{slice + 999}.json"
            json_data = json.load(open(f"{self.json_folder_path}/{file}", "r"))
            self.cache_slice = slice
            self.cached_data = json_data
            return self.cached_data["playlists"][pid%1000]
    
    def get_playlist_tracks(self, pid):
        return self.get_playlist_info(pid)["tracks"]


