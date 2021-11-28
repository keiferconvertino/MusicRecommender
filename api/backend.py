import time
from flask import Flask, request

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

import creds
from model import recommend_listener


columns = ['track_id', 'popularity', 'acousticness', 'danceability', 'liveness','loudness', 'speechiness', 'tempo', 'valence', 'genre', 'artist_name', 'track_name']
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(creds.client_id, creds.client_secret))

app = Flask(__name__, static_folder='../build', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/backend/getRecommendations', methods = ['GET'])
def get_recommendations():
    songName = request.args.get('songName')
    

    category = request.args.get('category')
    if category == "":
        category = 0
    else:
        category = int(category)
    numRecs = request.args.get('numRecs')
    if str(numRecs).isdigit():
        numRecs = int(numRecs)
    else:
        numRecs = 3

    print(songName, category, numRecs)
    tracks = spotify.search(q=songName, type='track')
    id = tracks['tracks']['items'][0]['id']
    name = tracks['tracks']['items'][0]['name']
    artist = tracks['tracks']['items'][0]['artists'][0]['name']
    albumArt = tracks['tracks']['items'][0]['album']['images'][0]['url']
    audioFeatures = spotify.audio_features(tracks=[id])[0]

    print(audioFeatures)
    df = pd.DataFrame([[audioFeatures['id'], 0, audioFeatures['acousticness'], audioFeatures['danceability'], audioFeatures['liveness'], audioFeatures['loudness'], audioFeatures['speechiness'], audioFeatures['tempo'], audioFeatures['valence'], '', artist, name]], columns=columns)
    print(df)
    # model time
    recs = recommend_listener(df, category, numRecs+1)
    
    recs_json = []
    for (idx,rec) in recs.iterrows():
        if rec['track_id'] == audioFeatures['id']:
            continue
        track = spotify.track(rec['track_id'])
        track_json = {
            'name': rec['track_name'],
            'artist': rec['artist_name'],
            'cover': track['album']['images'][0]['url'],
            'url': track['external_urls']['spotify']
        }
        recs_json.append(track_json)
        
    res = {'name': name, 'artist':artist, 'cover':albumArt, 'recommendations' : recs_json}
    print(res)
    return res