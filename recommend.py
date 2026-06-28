import pandas as pd
import logging
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("recommend.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("Loading data...")
try:
    music = pd.read_csv('dataset.csv')
    logging.info("Data loaded successfully.")
except Exception as e:
    logging.error("Failed to load dataset: %s", str(e))
    raise e

# Cleaning
music = music.drop_duplicates(subset=['track_name', 'artists'], keep='first', ignore_index=True)
music = music.drop(columns=['Unnamed: 0', 'track_id', 'album_name'])
music = music.dropna(subset=['track_name', 'artists'])

# Remove low quality and irrelevant entries
music = music[music['popularity'] > 0.1]
music = music[~music['track_genre'].isin(['kids', 'study', 'guitar', 'sleep'])]

music = music.reset_index(drop=True)

# Feature engineering
music['explicit'] = music['explicit'].astype(int)

feature_cols = music.select_dtypes(include=['float64', 'int64']).columns.tolist()
feature_cols = [col for col in feature_cols if col != 'explicit']

scaler = MinMaxScaler()
music[feature_cols] = scaler.fit_transform(music[feature_cols])

genre_dummies  = pd.get_dummies(music['track_genre'], prefix='genre') * 0.15
feature_matrix = pd.concat([music[feature_cols], music[['explicit']], genre_dummies], axis=1)

logging.info("Feature matrix ready. Shape: %s", feature_matrix.shape)


def find_song(song):
    return music[music['track_name'].str.lower() == song.strip().lower()]


def recommend(song_idx, n=5):
    logging.info("Recommending for index: %d", song_idx)

    song_info   = music.iloc[song_idx]
    song_vector = feature_matrix.iloc[song_idx].values.reshape(1, -1)
    similarity  = cosine_similarity(song_vector, feature_matrix)

    distances = sorted(enumerate(similarity[0]), key=lambda x: x[1], reverse=True)

    recommendations = []
    for idx, score in distances:
        if idx == song_idx:
            continue
        rec               = music.iloc[idx].to_dict()
        rec['similarity'] = round(score * 100, 2)
        recommendations.append(rec)
        if len(recommendations) == n:
            break

    logging.info("Top %d recommendations ready.", n)
    return song_info, recommendations