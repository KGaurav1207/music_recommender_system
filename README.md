# 🎵 Content-Based Music Recommender System

This project is a content-based music recommender system built using Python, Scikit-learn, and Streamlit. It recommends songs that are similar to a selected track by analyzing Spotify audio features such as danceability, energy, tempo, valence, and genre.

To make the recommendations more interactive, the application also integrates the Spotify API to display album artwork, preview clips, and direct Spotify links.

🔗 **Live Demo:** Coming Soon

---

## Demo

![Demo](demo.gif)

---

## Features

- Recommend songs based on audio characteristics using **Cosine Similarity**.
- Interactive web application built with **Streamlit**.
- Fetch album artwork, Spotify links, and 30-second previews using the **Spotify API**.
- Feature engineering using normalized audio features and one-hot encoded genres.
- Computes similarity only for the selected song, avoiding the need to store a huge similarity matrix.

---

## Technology Stack

| Category | Tools |
|----------|-------|
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Frontend | Streamlit |
| API | Spotify API, Spotipy |
| Environment | python-dotenv |

---

## Project Structure

```text
music_recommender_system/
│── app.py                 # Streamlit application
│── recommend.py           # Recommendation engine
│── spotify_utils.py       # Spotify API helper functions
│── dataset.csv            # Spotify dataset
│── requirements.txt
│── README.md
│── demo.gif
│── .env                   # Spotify credentials (not uploaded)
```

---

## Dataset

The project uses the Spotify Tracks Dataset containing more than **114,000 songs**.

Each song includes audio features such as:

- Danceability
- Energy
- Loudness
- Tempo
- Valence
- Speechiness
- Acousticness
- Instrumentalness
- Liveness
- Popularity
- Genre

After removing duplicate songs and cleaning the data, the recommendation engine works with approximately **81,000 unique tracks**.

---

## Installation

Clone the repository

```bash
git clone https://github.com/KGaurav1207/music_recommender_system.git

cd music_recommender_system
```

Create a virtual environment

```bash
python3 -m venv venv

source venv/bin/activate
```

Install the required packages

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
SPOTIFY_CLIENT_ID=your_client_id

SPOTIFY_CLIENT_SECRET=your_client_secret
```

Run the application

```bash
streamlit run app.py
```

---

## How It Works

1. The dataset is cleaned by removing duplicate songs and handling missing values.
2. Numerical audio features are normalized using **MinMaxScaler**.
3. Song genres are converted into numerical form using **One-Hot Encoding**.
4. The processed features are combined into a feature matrix representing each song.
5. When a user selects a song, the system computes cosine similarity between the selected song and all other songs.
6. The most similar songs are ranked and displayed along with album artwork, preview audio, and Spotify links.

---

## Challenges Faced

While building this project, I encountered a few practical challenges:

- Computing an 81K × 81K similarity matrix required more than **50 GB of memory**, so I switched to computing cosine similarity only for the selected song.
- Multiple songs in the dataset shared the same title (for example, *Believer*), so artist-based filtering was added to improve recommendation accuracy.
- Balancing audio features and one-hot encoded genres required careful feature engineering to produce meaningful recommendations.

---

## Future Improvements

- Hybrid recommendation system
- Playlist recommendation
- Fuzzy search for song names
- Personalized recommendations
- Collaborative filtering

---

## Author

**Kumar Gaurav Patel**

- GitHub: https://github.com/KGaurav1207
- LinkedIn: https://www.linkedin.com/in/kumar-gaurav-patel-73b149325/