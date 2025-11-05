import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import SVD, Dataset, Reader
from difflib import get_close_matches
import ast

class HybridRecommender:
    def __init__(self):
        print("📦 Loading data...")
        movies = pd.read_csv("data/tmdb_5000_movies.csv")
        credits = pd.read_csv("data/tmdb_5000_credits.csv")
        self.movies = movies.merge(credits, on="title")
        self.movies = self.movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
        self._prepare_content_data()
        self._prepare_collab_model()
        print("✅ Model ready!")

    def _prepare_content_data(self):
        def convert(obj):
            return [i['name'] for i in ast.literal_eval(obj)]
        def fetch_director(obj):
            for i in ast.literal_eval(obj):
                if i['job'] == 'Director':
                    return i['name']
            return ''
        def collapse(L):
            return [i.replace(" ", "") for i in L]

        self.movies.dropna(inplace=True)
        self.movies['genres'] = self.movies['genres'].apply(convert)
        self.movies['keywords'] = self.movies['keywords'].apply(convert)
        self.movies['cast'] = self.movies['cast'].apply(lambda x: convert(x)[:3])
        self.movies['crew'] = self.movies['crew'].apply(fetch_director)
        self.movies['genres'] = self.movies['genres'].apply(collapse)
        self.movies['keywords'] = self.movies['keywords'].apply(collapse)
        self.movies['cast'] = self.movies['cast'].apply(collapse)
        self.movies['tags'] = (
            self.movies['overview'].fillna('').astype(str)
            + " " + self.movies['genres'].astype(str)
            + " " + self.movies['keywords'].astype(str)
            + " " + self.movies['cast'].astype(str)
            + " " + self.movies['crew'].astype(str)
        )
        cv = CountVectorizer(max_features=5000, stop_words='english')
        vectors = cv.fit_transform(self.movies['tags']).toarray()
        self.similarity = cosine_similarity(vectors)

    def _prepare_collab_model(self):
        ratings = pd.read_csv('data/ratings.dat', sep='::', engine='python',
                              names=['userId', 'movieId', 'rating', 'timestamp'])
        ratings.drop('timestamp', axis=1, inplace=True)
        reader = Reader(rating_scale=(0.5, 5))
        data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
        trainset = data.build_full_trainset()
        self.svd = SVD()
        self.svd.fit(trainset)

    def recommend(self, movie_title, user_id=10, alpha=0.6):
        titles = self.movies['title'].str.lower().tolist()
        movie_title = movie_title.strip().lower()
        close_matches = get_close_matches(movie_title, titles, n=1, cutoff=0.4)
        if not close_matches:
            return [{"message": "Movie not found"}]

        matched = close_matches[0]
        idx = self.movies[self.movies['title'].str.lower() == matched].index[0]
        sim_scores = list(enumerate(self.similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:21]
        movie_indices = [i[0] for i in sim_scores]
        movie_ids = self.movies.iloc[movie_indices].index.tolist()
        collab_scores = [self.svd.predict(user_id, m).est for m in movie_ids]
        content_scores = np.array([s[1] for s in sim_scores])
        hybrid_scores = alpha * content_scores + (1 - alpha) * np.array(collab_scores)
        top = np.argsort(hybrid_scores)[::-1][:10]
        return self.movies.iloc[[movie_indices[i] for i in top]][['title']].to_dict(orient='records')
