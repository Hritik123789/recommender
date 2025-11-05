from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from recommender_model import HybridRecommender
from tmdb_helper import get_movie_details
import concurrent.futures

# ✅ Initialize FastAPI app
app = FastAPI(title="Hybrid Movie Recommender API (CORS Enabled + Timeout Safe)")

# ✅ Add CORS Middleware BEFORE defining routes
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # allow your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load the model once
model = HybridRecommender()

@app.get("/")
def home():
    return {"message": "Hybrid Movie Recommender API is running (with TMDB fallback)"}

@app.get("/recommend")
def recommend(
    movie: str = Query(..., description="Movie title"),
    user_id: int = Query(10, description="User ID for collaborative filtering"),
):
    recommendations = model.recommend(movie, user_id)
    enriched = []

    # 🧠 Use ThreadPoolExecutor to fetch TMDB info concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_movie = {
            executor.submit(get_movie_details, rec.get("title")): rec.get("title")
            for rec in recommendations
        }

        for future in concurrent.futures.as_completed(future_to_movie):
            title = future_to_movie[future]
            try:
                tmdb_data = future.result(timeout=6)
                if tmdb_data:
                    enriched.append(tmdb_data)
                else:
                    enriched.append({
                        "title": title,
                        "poster": None,
                        "overview": None,
                        "rating": None
                    })
            except Exception:
                enriched.append({
                    "title": title,
                    "poster": None,
                    "overview": None,
                    "rating": None
                })

    return {"requested_movie": movie, "recommendations": enriched}
