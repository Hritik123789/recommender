import streamlit as st
from recommender_model import HybridRecommender
from tmdb_helper import get_movie_details
import concurrent.futures

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(page_title="CineMatch", page_icon="🎬", layout="wide")

# ----------------------- NAVBAR -----------------------------
def navbar():
    st.markdown("""
    <style>
    .navbar {
        background-color: #141414;
        padding: 15px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        font-family: 'Poppins', sans-serif;
        position: fixed;
        width: 100%;
        top: 0;
        z-index: 100;
        border-bottom: 1px solid #222;
    }
    .brand {
        font-size: 26px;
        font-weight: bold;
        color: #E50914;
    }
    .searchbar {
        display: flex;
        gap: 10px;
        align-items: center;
    }
    .searchbar input {
        padding: 8px 12px;
        border-radius: 5px;
        border: none;
        width: 220px;
    }
    </style>

    <div class="navbar">
        <div class="brand">🎬 CineMatch</div>
        <div class="searchbar">
            <input type="text" id="movieInput" placeholder="Search for a movie...">
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True)

navbar()

# ----------------------- LOAD MODEL --------------------------
@st.cache_resource
def load_model():
    return HybridRecommender()

model = load_model()

# ----------------------- SAFE HELPER --------------------------
def safe_get_movie_info(title: str) -> dict:
    """
    Wraps get_movie_details() safely.
    Ensures the app never crashes even if TMDB returns None or fails.
    """
    try:
        info = get_movie_details(title)
        if not info or not isinstance(info, dict):
            raise ValueError("Invalid or missing data.")
        return info
    except Exception as e:
        print(f"⚠️ TMDB fetch failed for '{title}': {e}")
        # return a placeholder dictionary
        return {
            "title": title,
            "poster": "https://via.placeholder.com/300x450?text=No+Poster",
            "overview": "No information available."
        }

# ----------------------- TRENDING MOVIES ---------------------
TRENDING = [
    "Avengers: Endgame", "Iron Man", "Interstellar", "The Dark Knight",
    "Inception", "Avatar", "Titanic", "Joker", "Black Panther", "The Matrix"
]

st.markdown("## 🍿 Trending Now")

cols = st.columns(5)
for idx, movie in enumerate(TRENDING):
    col = cols[idx % 5]
    with col:
        info = safe_get_movie_info(movie)
        st.image(
            info.get("poster"),
            use_container_width=True,
        )
        st.markdown(
            f"<h5 style='text-align:center'>{info.get('title')}</h5>",
            unsafe_allow_html=True,
        )
        if st.button(f"🎯 Recommend similar to {info.get('title')}", key=f"btn_{idx}"):
            st.session_state["selected_movie"] = info.get("title")

# ----------------------- SEARCH BAR --------------------------
st.markdown("---")
st.markdown("### 🔍 Find Your Next Movie")

search_movie = st.text_input(
    "Enter a movie name:",
    value=st.session_state.get("selected_movie", "")
)

if st.button("Get Recommendations 🎥"):
    if not search_movie.strip():
        st.warning("Please enter or select a movie.")
    else:
        with st.spinner("Fetching recommendations..."):
            try:
                recos = model.recommend(search_movie, user_id=10)
            except Exception as e:
                st.error(f"⚠️ Recommendation error: {e}")
                recos = []

            if not recos:
                st.error("No similar movies found.")
            else:
                enriched = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    future_to_movie = {
                        executor.submit(safe_get_movie_info, r["title"]): r["title"]
                        for r in recos
                    }
                    for future in concurrent.futures.as_completed(future_to_movie):
                        info = future.result()
                        enriched.append(info)

                st.subheader(f"🎬 Because you liked **{search_movie}**")
                cols = st.columns(5)
                for i, m in enumerate(enriched[:10]):
                    c = cols[i % 5]
                    with c:
                        st.image(
                            m.get("poster"),
                            use_container_width=True,
                        )
                        st.markdown(f"**{m.get('title', 'Unknown Title')}**")
                        st.caption(m.get("overview", "No description available."))
