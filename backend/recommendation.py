
import joblib
import numpy as np
from pathlib import Path

# Load the trained Week 5 recommendation model
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "recommender_model.joblib"

model = joblib.load(MODEL_PATH)


def get_recommendations(user_id: int, top_n: int = 5):
    # Get movies watched by this user
    watched_movies = model["user_watched"].get(user_id, set())

    if not watched_movies:
        return []

    # Convert movie IDs into similarity matrix indexes
    watched_indices = [
        model["movie_to_idx"][movie_id]
        for movie_id in watched_movies
        if movie_id in model["movie_to_idx"]
    ]

    if not watched_indices:
        return []

    # Calculate average similarity scores
    scores = model["item_similarity"][watched_indices].mean(axis=0)

    # Exclude movies already watched
    scores[watched_indices] = -1

    # Get top recommended movie indexes
    top_indices = np.argsort(scores)[::-1][:top_n]

    # Convert indexes back to movie IDs
    recommended_ids = [
        int(model["idx_to_movie"][int(index)])
        for index in top_indices
        if scores[index] > -1
    ]

    # Get movie details
    recommendations = model["movies_df"][
        model["movies_df"]["movieId"].isin(recommended_ids)
    ]

    return recommendations[
        ["movieId", "title", "genres"]
    ].to_dict(orient="records")
