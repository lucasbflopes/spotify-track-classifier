import pickle
import sys
import json
from api.spotify_api_wrapper import SpotifyAPIWrapper

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

if len(sys.argv) < 2:
	print('usage: python {} "track_name"'.format(sys.argv[0].split('/')[-1]))
	exit()
else:
	track_query = sys.argv[1]

with open('model_trained.pkl', 'rb') as fin:
	model = pickle.load(fin)

with open('./api/client_keys.json') as fin:
	KEYS = json.load(fin)

CLIENT_ID = KEYS['clientID']
CLIENT_SECRET = KEYS['clientSecret']	

api = SpotifyAPIWrapper(CLIENT_ID, CLIENT_SECRET)
trackInfo = api.get_track_info(track_query)
trackFeatures = api.get_track_features(AUDIO_FEATURES, [trackInfo['id']])

if trackInfo:
	prediction = model.predict(trackFeatures.values)
	print("Title ".ljust(12) + ': ' + trackInfo['title'].capitalize())
	print("Artist ".ljust(12) + ': ' + trackInfo['artist'].capitalize())
	print("Prediction ".ljust(12) + ': ' + prediction[0].capitalize())
else:
	print("Track not found")