import requests
from base64 import b64encode
import pandas as pd
import re

class SpotifyAPIWrapper(object):
    """
    A very simple wrapper around the spotify's api whereby some requests pertaining a few functionalities are done in a cleaner fashion.

    More info about how to generate your pesonal api keys read : https://developer.spotify.com/web-api/

    Constructor Parameters
    -------------------------
    clientID: personal public key provided by the api and necessary to perform some requests.
    clientSecret: personal private key provided by the api and necessary to perform some requests.
    """
    API_ENDPOINTS = {
        "category": "https://api.spotify.com/v1/browse/categories/{category_id}/playlists",
        "playlist": "https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks",
        "audio_features": "https://api.spotify.com/v1/audio-features",
        "search_track": "https://api.spotify.com/v1/search",
        "token": "https://accounts.spotify.com/api/token"
    }

    def __init__(self, clientID, clientSecret):
        self._clientID = clientID
        self._clientSecret = clientSecret
        self._token = self.request_token()
        self._header = {"Authorization": "Bearer {}".format(self._token)}


    def request_token(self):    
        """
        Request token to the Spotify's API which is needed in order to make further requests.
        In case the client key provided in the constructor is wrong, the function raises an exception.

        Returns
        -------
        token: string representing the token provided by the api.
        """
        authorizationParam = "{}:{}".format(self._clientID, self._clientSecret).encode()
        header = {"Authorization": "Basic {}".format(b64encode(authorizationParam).decode('utf-8'))}
        body = {"grant_type": "client_credentials"}
        r = requests.post(self.API_ENDPOINTS['token'], data=body, headers=header)
        if r.status_code != 200:
            raise Exception("Invalid client key")
        else:
            responseJSON = r.json()
            token = responseJSON['access_token']
            return token

    def get_track_features(self, audioFeatures, trackIDs):
        """
        Get audio features, as listed in 'audioFeatures', for each track in 'trackIDS'.
        Each feature must be a metric provided by spotify's api.
        In case one of the features is missing for a given track, a 'NaN' value is placed instead.

        This function does not check if the ids provided are valid. Be aware of this fact.

        For more details read: https://developer.spotify.com/web-api/get-several-audio-features/

        Parameters
        ------------
        audioFeatures: list of spotify's features (e.g.  'mode', 'loudness', etc)
        trackIDs: list of strings containing the spotify's id of each track.

        Returns
        -----------
        featuresDataframe: pandas dataframe with all the features in 'audioFeatures' for each track in 'trackIDS'
        """

        featuresDataframe = pd.DataFrame()
        # Depending on whether there is one or more ids, the request's param is different.
        if len(trackIDs) > 1:
            params = '/?ids=' + ','.join(trackIDs)
        else:
            params = '/' + trackIDs[0]
        trackRequest = requests.get(self.API_ENDPOINTS['audio_features'] + params, headers=self._header)
        trackResponse = trackRequest.json()

        # The way the JSON response is formatted also depedends on the number of ids
        if len(trackIDs) > 1:
            for audioFeature in trackResponse['audio_features']:
                # Some tracks do not have any audio feature, thus they are filled with None values
                if audioFeature is None:
                    features = [float('nan')] * len(audioFeatures)
                else:
                    features = [audioFeature.get(feat, float('nan')) for feat in audioFeatures]
                trackFeaturesRow = pd.DataFrame(features)
                trackFeaturesRow = trackFeaturesRow.transpose()
                featuresDataframe = featuresDataframe.append(trackFeaturesRow, ignore_index=True)
        else:
            features = [trackResponse.get(feat, float('nan')) for feat in audioFeatures]
            trackFeaturesRow = pd.DataFrame(features)
            trackFeaturesRow = trackFeaturesRow.transpose()
            featuresDataframe = featuresDataframe.append(trackFeaturesRow, ignore_index=True)

        featuresDataframe.columns = audioFeatures
        return featuresDataframe

    def get_track_info(self, trackName):
        """
        Get a track's title, artist/band and its unique spotify's id for 'trackName'.
        In case 'trackName' is mispelled or it does not exist in spotify, an exception is raised.

        More info about the api request, read: https://developer.spotify.com/web-api/search-item/
        
        Parameters
        ----------
        trackName: string containing the track's title query.

        Returns
        ----------
        trackInfo: a dictionary with track's 'title', 'artist' and 'id' as keys.
        """
        formatedTrackString = re.sub("\s+", '+', trackName.strip())
        trackReq = requests.get(self.API_ENDPOINTS['search_track'],
                             headers=self._header,
                             params={"q": formatedTrackString, "type": "track", 'limit': '1'}
                                )    
        trackResponse = trackReq.json()
        if trackResponse["tracks"]["items"]:
            trackInfo = {'title': trackResponse["tracks"]["items"][0]["name"],
                         'artist': trackResponse["tracks"]["items"][0]["artists"][0]["name"], 
                         'id': trackResponse["tracks"]["items"][0]["id"]
                        }
            return trackInfo
        else:
            raise Exception("Track not found")

    def get_playlists_from_category(self, category, limit=50):
        """
        Return some playlists from 'category' type.
        The 'category' must be a valid named according to the api, otherwise an empty list will be returned.

        By default this function tries to get as many playlists as possibile, which is 50 according to the api's documentation. However, not all categories have that many available, so fewer playlists might be returned.

        More info about the api request, read: https://developer.spotify.com/web-api/get-categorys-playlists/

        Parameters
        ------------
        category: string containing a valid category in spotify (e.g. 'pop', 'indie_alt').
        limit: int representing the number of playlist to get from the category. Default: 50.

        Returns
        -----------
        playlistLists: list of tuples in which the first element of each tuple is the id of the playlist's owner and the second is the playlist's id itself.
        """        
        categoryRequest = requests.get(self.API_ENDPOINTS['category'].format(category_id=category),
                                        headers=self._header,
                                        params={"limit": limit}
                                        )
        categoryResponse = categoryRequest.json()

        try:
            playlistList = [(playlist['owner']['id'], playlist['id']) for playlist in categoryResponse['playlists']['items']]
        except KeyError:
            playlistList = []

        return playlistList


    def get_tracks_from_playlist(self, userID, playlistID, limit=100):
        """
        Return all the tracks' names and ids in a playlist.

        By default this function tries to get as many tracks as possibile, which is 50 according to the api's documentation. However, not all playlists have that many tracks available, so fewer tracks might be returned.

        More info about the api request, read: https://developer.spotify.com/web-api/get-playlists-tracks/

        Parameters
        ------------
        userID: string representing the id of the playlist's owner.
        playlistID: string representing the id of the playlist.
        limit: int representing the number of tracks to get from a playlist. Default: 100.

        Returns
        -------------
        playlistTracks: list of tuples in which the first and second element of each tuple is the name and id of a track, respectively.
        """
        playlistRequest = requests.get(self.API_ENDPOINTS['playlist'].format(user_id=userID, playlist_id=playlistID),
                                        headers=self._header,
                                        params={"limit": limit}
                                        )
        playlistResponse = playlistRequest.json()
        playlistTracks = [(track['track']['name'], track['track']['id']) for track in playlistResponse['items'] if track['track']['id'] is not None]
        return playlistTracks
    
