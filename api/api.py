import time
from flask import Flask, request

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import creds


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(creds.client_id, creds.client_secret))

app = Flask(__name__)

@app.route('/getRecommendations', methods = ['GET'])
def get_recommendations():
    songName = request.args.get('songName')
    category = request.args.get('category')

    tracks = spotify.search(q=songName, type='track')
    id = tracks['tracks']['items'][0]['id']
    name = tracks['tracks']['items'][0]['name']
    artist = tracks['tracks']['items'][0]['artists'][0]['name']
    albumArt = tracks['tracks']['items'][0]['album']['images'][0]['url']
    audioFeatures = spotify.audio_features(tracks=[id])

    # model time


    return {'name': name, 'artist':artist, 'cover':albumArt, 'recommendations' : [
        {'name': 'hoopla', 'artist':'woohoo', 'cover': 'https://i.scdn.co/image/ab67616d0000b273cd945b4e3de57edd28481a3f'},
        {'name': 'hoopla', 'artist':'woohoo', 'cover': 'https://i.scdn.co/image/ab67616d0000b273cd945b4e3de57edd28481a3f'}
    ]}