# Imports
import numpy as np 
import pandas as pd
from scipy import stats
from scipy.sparse import csr_matrix
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import os

CATEGORY_DICT = {0: "All", 1: "Acoustic", 2: "Chill", 3: "Dance", 4: "Happy", 5: "Loud", 6: "A Capella", 7: "Alternative", 8: "Blues", 9: "Classical", 10: "Country", 11: "Dance", 12: "Electronic", 13: "Folk", 14: "Hip-Hop", 15: "Indie", 16: "Jazz", 17: "Movie", 18: "Opera", 19: "Pop", 20: "R&B", 21: "Rap", 22: "Reggae", 23: "Reggaeton", 24: "Rock", 25: "Ska", 26: "Soul", 27: "Soundtrack", 28: "World"}
# All dataset paths
print(os.getcwd())
path_all = "./api/data/SpotifyFeatures_Cleaned.csv" 
path_acoustic = "./api/data/SpotifyFeatures_Cleaned_Acoustic.csv"
path_chill = "./api/data/SpotifyFeatures_Cleaned_Chill.csv"
path_dance = "./api/data/SpotifyFeatures_Cleaned_Dance.csv"
path_happy = "./api/data/SpotifyFeatures_Cleaned_Happy.csv"
path_loud = "./api/data/SpotifyFeatures_Cleaned_Loud.csv"

def get_data(csv_path:str)->pd.DataFrame:
  """
    Return a pd.DataFrame for the csv at csv_path
  """
  df = pd.read_csv(csv_path)
  if "Unnamed: 0" in df.columns:
    df = df.drop(["Unnamed: 0"], axis = 1)
  if "cluster" in df.columns:
    df = df.drop(["cluster"], axis = 1)
  return df

data_all = get_data(path_all)
data_acoustic = get_data(path_acoustic)
data_chill = get_data(path_chill)
data_dance = get_data(path_dance)
data_happy = get_data(path_happy)
data_loud = get_data(path_loud)

def select_data(category:int)->pd.DataFrame:
  """
    Return the data set corresponds to the category number in the CATEGORY_DICT
  """
  if category == 1:
    return data_acoustic
  elif category == 2:
    return data_chill
  elif category == 3:
    return data_dance
  elif category == 4:
    return data_happy
  elif category == 5:
    return data_loud
  elif category > 5 and category < 29:
    genre = CATEGORY_DICT[category]
    return data_all[data_all["genre"] == genre]
  else:
    return data_all

def recommend_listener(input_song:pd.DataFrame, category:int, num_songs_to_rec:int)->pd.DataFrame:
  """
  Inpus: 
    input_song: a pd.DataFrame of listener input song, the order of the columns should be 
                'track_id', 'popularity', 'acousticness', 'danceability', 'liveness',
                'loudness', 'speechiness', 'tempo', 'valence', 'genre', 'artist_name',
                'track_name'
    category: an integer representing the category the listener choose, see what each number 
              corresponds to in the CATEGORY_DICT
    num_songs_to_rec an interger representing the number songs the listener what to be recommended
  """
  # Select the right data set 
  data = select_data(category)

  # Find k
  if num_songs_to_rec > 100:
    print("We can only recommend you 100 songs.")
    k = 100
  else:
    k = num_songs_to_rec
  
  # Min max scale data
  scaler = MinMaxScaler()
  num_data = data.select_dtypes(exclude=['object'])
  num_data = num_data.drop(['popularity'], axis=1)
  scaler = scaler.fit(num_data)
  data = data.drop(num_data.columns, axis=1)
  data[num_data.columns] = scaler.transform(num_data)

  # Min max scale input song
  num_input_song = input_song.select_dtypes(exclude=['object'])
  num_input_song = num_input_song.drop(['popularity'], axis=1)
  input_song = input_song.drop(num_input_song.columns, axis=1)
  input_song[num_input_song.columns] = scaler.transform(num_input_song)

  # KNN modeling 
  knn = NearestNeighbors(n_neighbors = k)
  knn.fit(data.drop(["track_id", "popularity", "genre", "artist_name", "track_name"], axis=1))
  neighbors = knn.kneighbors(input_song.drop(["track_id", "popularity", "genre", "artist_name", "track_name"], axis=1), return_distance=False)

  # Return a dataframe of rec 
  df_rec = data.iloc[neighbors.tolist()[0]]
  return df_rec


