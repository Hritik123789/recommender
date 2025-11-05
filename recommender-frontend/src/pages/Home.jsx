import React from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import RecommendationGrid from "../components/RecommendationGrid";

const API_URL = "http://127.0.0.1:8000/recommend";

const Home = () => {
    const [movies, setMovies] = React.useState([]);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState("");

    const handleSearch = async (query) => {
        setLoading(true);
        setError("");
        setMovies([]);

        try {
            console.log("🔍 Fetching:", `${API_URL}?movie=${query}&user_id=10`);
            const res = await axios.get(API_URL, {
                params: { movie: query, user_id: 10 },
            });

            console.log("✅ Response:", res.data);
            const recos = res.data.recommendations || [];

            if (recos.length === 0) {
                setError("No recommendations found.");
            }

            setMovies(recos);
        } catch (err) {
            console.error("❌ API error:", err);
            setError("Failed to fetch recommendations.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-netflixDark min-h-screen text-white">
            <Navbar onSearch={handleSearch} />

            {/* LOADING */}
            {loading && (
                <p className="text-center text-gray-400 mt-40 text-xl">
                    Loading recommendations...
                </p>
            )}

            {/* ERROR */}
            {!loading && error && (
                <p className="text-center text-red-500 mt-40 text-xl">{error}</p>
            )}

            {/* RECOMMENDATIONS */}
            {!loading && !error && movies.length > 0 && (
                <RecommendationGrid movies={movies} onRecommend={handleSearch} />
            )}

            {/* EMPTY STATE */}
            {!loading && !error && movies.length === 0 && (
                <p className="text-center text-gray-400 mt-40 text-xl">
                    Search for a movie to get recommendations!
                </p>
            )}
        </div>
    );
};

export default Home;
