import requests

TMDB_API_KEY = "2a3784e99a38cb44a993ba6f0f624fad"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def get_movie_details(title):
    try:
        query_url = f"{TMDB_BASE_URL}/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": title}
        response = requests.get(query_url, params=params, timeout=5)  # ⏱ 5s hard timeout

        # If TMDB doesn’t respond in 5 seconds, skip gracefully
        if response.status_code != 200:
            print(f"⚠️ TMDB request failed for {title} - status {response.status_code}")
            return None

        data = response.json()
        if not data.get("results"):
            return None

        movie = data["results"][0]
        return {
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "poster": (
                f"{TMDB_IMAGE_BASE_URL}{movie['poster_path']}"
                if movie.get("poster_path")
                else None
            ),
            "rating": movie.get("vote_average")
        }

    except requests.exceptions.Timeout:
        print(f"⏰ TMDB timeout for {title}, skipping...")
        return None

    except requests.exceptions.RequestException as e:
        print(f"⚠️ TMDB network error for {title}: {e}")
        return None

    except Exception as e:
        print(f"⚠️ TMDB unknown error for {title}: {e}")
        return None
