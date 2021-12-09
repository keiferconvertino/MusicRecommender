import time
from flask import Flask, request
from flask.helpers import send_from_directory

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

import creds
from model import recommend_listener
from artist_model import radar_top_n_song_features, predict_popularity
import mpld3


columns = ['track_id', 'popularity', 'acousticness', 'danceability', 'liveness','loudness', 'speechiness', 'tempo', 'valence', 'genre', 'artist_name', 'track_name']
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(creds.client_id, creds.client_secret))

app = Flask(__name__, static_folder='../build', static_url_path='/')

@app.route('/')
def index():
    print(app.static_folder)
    return send_from_directory(app.static_folder, 'index.html')

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
    recs, recs_gmm = recommend_listener(df, category, numRecs+1)
    
    recs_knn_json = []
    for (idx,rec) in recs.iterrows():
        if rec['track_id'] == audioFeatures['id'] or len(recs_knn_json) == numRecs:
            continue
        track = spotify.track(rec['track_id'])
        track_json = {
            'name': rec['track_name'],
            'artist': rec['artist_name'],
            'cover': track['album']['images'][0]['url'],
            'url': track['external_urls']['spotify']
        }
        recs_knn_json.append(track_json)

    recs_gmm_json = []
    for (idx,rec) in recs_gmm.iterrows():
        if rec['track_id'] == audioFeatures['id'] or len(recs_gmm_json) == numRecs:
            continue
        track = spotify.track(rec['track_id'])
        track_json = {
            'name': rec['track_name'],
            'artist': rec['artist_name'],
            'cover': track['album']['images'][0]['url'],
            'url': track['external_urls']['spotify']
        }
        recs_gmm_json.append(track_json)
        
        
    res = {'name': name, 'artist':artist, 'cover':albumArt, 'recommendations' : {'knn' : recs_knn_json, 'gmm': recs_gmm_json}}
    print(res)
    return res



# @app.route('/backend/getArtistRecommendations', methods = ['GET'])
# def get_artist_recommendations():
#     songName = request.args.get('songName')
#     category = request.args.get('category')
#     if category == "":
#         category = 0
#     else:
#         category = int(category)
#     numRecs = request.args.get('numRecs')
#     if str(numRecs).isdigit():
#         numRecs = int(numRecs)
#     else:
#         numRecs = 3

#     print(songName, category, numRecs)
#     tracks = spotify.search(q=songName, type='track')
#     id = tracks['tracks']['items'][0]['id']
#     name = tracks['tracks']['items'][0]['name']
#     artist = tracks['tracks']['items'][0]['artists'][0]['name']
#     albumArt = tracks['tracks']['items'][0]['album']['images'][0]['url']
#     audioFeatures = spotify.audio_features(tracks=[id])[0]

#     print(audioFeatures)
#     df = pd.DataFrame([[audioFeatures['id'], 0, audioFeatures['acousticness'], audioFeatures['danceability'], audioFeatures['liveness'], audioFeatures['loudness'], audioFeatures['speechiness'], audioFeatures['tempo'], audioFeatures['valence'], '', artist, name]], columns=columns)
#     print(df)

#     # model time
#     popularity = predict_popularity(df)
#     fig = radar_top_n_song_features(df, category, numRecs)

#     html = mpld3.fig_to_html(fig)
#     print(html)
#     res = {'name': name, 'artist':artist, 'cover':albumArt, 'popularity' : popularity}
#     print(res)
#     return res