import pandas as pd
from api.spotify_api_wrapper import SpotifyAPIWrapper
import json
from operator import itemgetter

CATEGORIES = (
	"pop",
	"indie_alt",
	"punk",
	"funk",
	"rock",
	"hiphop",
	"metal",
	"country",
	"jazz",
	"reggae",
	"classical",
	"party",
	"latin",
	"romance",
	"blues"
)

AUDIO_FEATURES = (
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo"
)

with open('./api/client_keys.json') as fin:
	KEYS = json.load(fin)

CLIENT_ID = KEYS['clientID']
CLIENT_SECRET = KEYS['clientSecret']	

api = SpotifyAPIWrapper(CLIENT_ID, CLIENT_SECRET)

dataset = pd.DataFrame()

for category in CATEGORIES:
	print("Starting '{}' track requests".format(category))
	playlistList = api.get_playlists_from_category(category)
	for userID, playlistID in playlistList:
		trackList = api.get_tracks_from_playlist(userID, playlistID)
		trackNames = list(map(itemgetter(0), trackList))
		trackIDs = list(map(itemgetter(1), trackList))
		trackFeatures = api.get_track_features(AUDIO_FEATURES, trackIDs) 
		trackFeatures['genre'] = [category] * len(trackFeatures)
		trackFeatures.insert(loc=0, column='title', value=trackNames)
		dataset = dataset.append(trackFeatures)

dataset.to_csv('./dataset/dataset2.csv', index=False)
